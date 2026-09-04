import ResumeList from './components/ResumeList';

export default function ResumesPage() {
  return (
    <div className="px-4 sm:px-0">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Resumes</h1>
        <p className="text-sm text-gray-500 mt-1">
          Upload and manage your resume versions. Each resume can be analyzed against multiple job descriptions.
        </p>
      </div>
      <ResumeList />
    </div>
  );
}
