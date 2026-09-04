import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { getResumes, uploadResume, updateResume, deleteResume } from '../api';
import ResumeUpload from './ResumeUpload';
import ResumeCard from './ResumeCard';
import ResumeDetail from './ResumeDetail';

export default function ResumeList() {
  const [viewingId, setViewingId] = useState<number | null>(null);
  const queryClient = useQueryClient();

  const { data: resumes = [], isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: getResumes,
  });

  const uploadMutation = useMutation({
    mutationFn: ({ formData, onProgress }: { formData: FormData; onProgress: (pct: number) => void }) =>
      uploadResume(formData, (e) => {
        if (e.total) onProgress(Math.round((e.loaded / e.total) * 100));
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
      toast.success('Resume uploaded successfully!');
    },
    onError: (error: any) => {
      const msg = error?.response?.data?.detail || error?.response?.data?.file?.[0] || 'Upload failed. Please try again.';
      toast.error(msg);
    },
  });

  const renameMutation = useMutation({
    mutationFn: updateResume,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
      toast.success('Resume renamed.');
    },
    onError: () => toast.error('Failed to rename resume.'),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteResume,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
      toast.success('Resume deleted.');
    },
    onError: () => toast.error('Failed to delete resume.'),
  });

  const handleUpload = async (formData: FormData, onProgress: (pct: number) => void) => {
    await uploadMutation.mutateAsync({ formData, onProgress });
  };

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <ResumeUpload onUpload={handleUpload} isUploading={uploadMutation.isPending} />

      {/* List Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            My Resumes
            {resumes.length > 0 && (
              <span className="ml-2 text-sm font-normal text-gray-500">
                ({resumes.length})
              </span>
            )}
          </h2>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-lg border border-gray-200 p-5 animate-pulse">
                <div className="flex gap-3">
                  <div className="w-10 h-10 bg-gray-200 rounded-lg" />
                  <div className="flex-1 space-y-2">
                    <div className="h-4 bg-gray-200 rounded w-3/4" />
                    <div className="h-3 bg-gray-200 rounded w-1/2" />
                  </div>
                </div>
                <div className="mt-4 h-8 bg-gray-100 rounded-lg" />
              </div>
            ))}
          </div>
        ) : resumes.length === 0 ? (
          // Empty state
          <div className="bg-white rounded-lg border-2 border-dashed border-gray-200 p-12 text-center">
            <div className="mx-auto w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-base font-medium text-gray-700 mb-1">No resumes yet</h3>
            <p className="text-sm text-gray-400">Upload your first resume above to get started.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {resumes.map((resume) => (
              <ResumeCard
                key={resume.id}
                resume={resume}
                onView={(id) => setViewingId(id)}
                onRename={(id, name) => renameMutation.mutate({ id, name })}
                onDelete={(id) => deleteMutation.mutate(id)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Detail Modal */}
      {viewingId !== null && (
        <ResumeDetail
          resumeId={viewingId}
          onClose={() => setViewingId(null)}
        />
      )}
    </div>
  );
}
