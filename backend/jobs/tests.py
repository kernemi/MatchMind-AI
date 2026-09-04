"""
Tests for Jobs app
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Job
from users.models import User


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def user_a(db):
    return User.objects.create_user(
        email='usera@example.com',
        password='TestPass123!',
        first_name='User',
        last_name='A',
    )


@pytest.fixture
def user_b(db):
    return User.objects.create_user(
        email='userb@example.com',
        password='TestPass123!',
        first_name='User',
        last_name='B',
    )


@pytest.fixture
def auth_client_a(api_client, user_a):
    refresh = RefreshToken.for_user(user_a)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def auth_client_b(api_client, user_b):
    refresh = RefreshToken.for_user(user_b)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def job_data():
    return {
        'title': 'Backend Engineer',
        'company': 'Acme Corp',
        'description': 'We need a Django developer with 3+ years of experience.',
        'url': 'https://acme.com/jobs/backend',
        'status': 'saved',
        'notes': 'Referred by a friend.',
    }


@pytest.fixture
def create_job(user_a):
    def _create(**kwargs):
        defaults = {
            'user': user_a,
            'title': 'Software Engineer',
            'company': 'TestCo',
            'description': 'Build cool things.',
            'status': 'saved',
        }
        defaults.update(kwargs)
        return Job.objects.create(**defaults)
    return _create


# ---------------------------------------------------------------------------
# CRUD Tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestJobCreate:

    def test_create_job_success(self, auth_client_a, job_data):
        url = reverse('jobs:job-list')
        response = auth_client_a.post(url, job_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == job_data['title']
        assert response.data['company'] == job_data['company']
        assert response.data['status'] == 'saved'
        assert Job.objects.filter(title=job_data['title']).exists()

    def test_create_job_requires_auth(self, api_client, job_data):
        url = reverse('jobs:job-list')
        response = api_client.post(url, job_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_missing_required_fields(self, auth_client_a):
        url = reverse('jobs:job-list')
        response = auth_client_a.post(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data
        assert 'company' in response.data
        assert 'description' in response.data

    def test_create_job_invalid_url(self, auth_client_a, job_data):
        job_data['url'] = 'not-a-url'
        url = reverse('jobs:job-list')
        response = auth_client_a.post(url, job_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'url' in response.data

    def test_create_job_invalid_status(self, auth_client_a, job_data):
        job_data['status'] = 'unknown'
        url = reverse('jobs:job-list')
        response = auth_client_a.post(url, job_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'status' in response.data

    def test_create_job_without_url(self, auth_client_a, job_data):
        """URL is optional"""
        job_data.pop('url')
        url = reverse('jobs:job-list')
        response = auth_client_a.post(url, job_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestJobList:

    def test_list_returns_only_own_jobs(self, auth_client_a, auth_client_b, create_job, user_b):
        create_job()  # belongs to user_a
        Job.objects.create(
            user=user_b,
            title='Other Job',
            company='Other Co',
            description='Other description',
            status='saved',
        )

        url = reverse('jobs:job-list')
        response = auth_client_a.get(url)

        assert response.status_code == status.HTTP_200_OK
        ids = [j['id'] for j in response.data['results']]
        # user_a should only see their own job
        for job_id in ids:
            assert Job.objects.get(id=job_id).user.email == 'usera@example.com'

    def test_filter_by_status(self, auth_client_a, create_job):
        create_job(status='saved')
        create_job(status='applied', title='Applied Job')
        create_job(status='interviewing', title='Interview Job')

        url = reverse('jobs:job-list')
        response = auth_client_a.get(url, {'status': 'applied'})

        assert response.status_code == status.HTTP_200_OK
        assert all(j['status'] == 'applied' for j in response.data['results'])

    def test_search_by_title(self, auth_client_a, create_job):
        create_job(title='Django Developer')
        create_job(title='React Engineer')

        url = reverse('jobs:job-list')
        response = auth_client_a.get(url, {'search': 'Django'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert 'Django' in response.data['results'][0]['title']

    def test_search_by_company(self, auth_client_a, create_job):
        create_job(company='Google')
        create_job(company='Amazon')

        url = reverse('jobs:job-list')
        response = auth_client_a.get(url, {'search': 'Google'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['company'] == 'Google'


@pytest.mark.django_db
class TestJobDetail:

    def test_get_own_job(self, auth_client_a, create_job):
        job = create_job()
        url = reverse('jobs:job-detail', args=[job.id])
        response = auth_client_a.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == job.id
        assert response.data['title'] == job.title

    def test_cannot_get_other_users_job(self, auth_client_a, user_b):
        other_job = Job.objects.create(
            user=user_b,
            title='Private Job',
            company='Private Co',
            description='Not yours.',
            status='saved',
        )
        url = reverse('jobs:job-detail', args=[other_job.id])
        response = auth_client_a.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestJobUpdate:

    def test_update_status(self, auth_client_a, create_job):
        job = create_job(status='saved')
        url = reverse('jobs:job-detail', args=[job.id])
        response = auth_client_a.patch(url, {'status': 'applied'}, format='json')

        assert response.status_code == status.HTTP_200_OK
        job.refresh_from_db()
        assert job.status == 'applied'

    def test_update_notes(self, auth_client_a, create_job):
        job = create_job()
        url = reverse('jobs:job-detail', args=[job.id])
        response = auth_client_a.patch(url, {'notes': 'Great opportunity!'}, format='json')

        assert response.status_code == status.HTTP_200_OK
        job.refresh_from_db()
        assert job.notes == 'Great opportunity!'

    def test_full_update(self, auth_client_a, create_job, job_data):
        job = create_job()
        url = reverse('jobs:job-detail', args=[job.id])
        response = auth_client_a.put(url, job_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == job_data['title']

    def test_cannot_update_other_users_job(self, auth_client_a, user_b):
        other_job = Job.objects.create(
            user=user_b,
            title='Private',
            company='Co',
            description='desc',
            status='saved',
        )
        url = reverse('jobs:job-detail', args=[other_job.id])
        response = auth_client_a.patch(url, {'status': 'applied'}, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestJobDelete:

    def test_delete_own_job(self, auth_client_a, create_job):
        job = create_job()
        url = reverse('jobs:job-detail', args=[job.id])
        response = auth_client_a.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Job.objects.filter(id=job.id).exists()

    def test_cannot_delete_other_users_job(self, auth_client_a, user_b):
        other_job = Job.objects.create(
            user=user_b,
            title='Private',
            company='Co',
            description='desc',
            status='saved',
        )
        url = reverse('jobs:job-detail', args=[other_job.id])
        response = auth_client_a.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestJobModel:

    def test_job_str(self, user_a):
        job = Job(user=user_a, title='SWE', company='Google')
        assert str(job) == 'SWE at Google'

    def test_default_status_is_saved(self, user_a):
        job = Job.objects.create(
            user=user_a,
            title='Test',
            company='TestCo',
            description='desc',
        )
        assert job.status == 'saved'

    def test_analysis_count_property(self, user_a):
        job = Job.objects.create(
            user=user_a,
            title='Test',
            company='TestCo',
            description='desc',
        )
        assert job.analysis_count == 0
