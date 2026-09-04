import api from '../../lib/axios';
import { ResumeListItem, ResumeDetail } from './types';

export const getResumes = async (): Promise<ResumeListItem[]> => {
  const response = await api.get('/resumes/');
  return response.data;
};

export const getResume = async (id: number): Promise<ResumeDetail> => {
  const response = await api.get(`/resumes/${id}/`);
  return response.data;
};

export const uploadResume = async (formData: FormData, onUploadProgress?: (progressEvent: any) => void): Promise<ResumeDetail> => {
  const response = await api.post('/resumes/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  });
  return response.data;
};

export const updateResume = async ({ id, name }: { id: number; name: string }): Promise<ResumeDetail> => {
  const response = await api.patch(`/resumes/${id}/`, { name });
  return response.data;
};

export const deleteResume = async (id: number): Promise<void> => {
  await api.delete(`/resumes/${id}/`);
};
