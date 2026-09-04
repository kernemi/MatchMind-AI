import { useQuery } from '@tanstack/react-query';
import { getResume } from '../api';

interface ResumeDetailProps {
  resumeId: number;
  onClose: () => void;
}

export default function ResumeDetail({ resumeId, onClose }: ResumeDetailProps) {
  const { data: resume, isLoading } = useQuery({
    queryKey: ['resume', resumeId],
    queryFn: () => getResume(resumeId),
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col">

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">
            {isLoading ? 'Loading...' : resume?.name}
          </h2>
          <button
            onClick={onClose}
            className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-5">
          {isLoading ? (
            <div className="flex justify-center py-10">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
            </div>
          ) : resume ? (
            <>
              {/* Skills */}
              {resume.extracted_skills?.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Extracted Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {resume.extracted_skills.map((skill) => (
                      <span
                        key={skill}
                        className="px-2.5 py-1 bg-blue-50 text-blue-700 text-xs font-medium rounded-full border border-blue-100"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Extracted Text */}
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Extracted Text</h3>
                {resume.extracted_text ? (
                  <pre className="text-xs text-gray-600 bg-gray-50 border border-gray-200 rounded-lg p-4 whitespace-pre-wrap font-sans leading-relaxed max-h-72 overflow-y-auto">
                    {resume.extracted_text}
                  </pre>
                ) : (
                  <p className="text-sm text-gray-400 italic">No text extracted yet.</p>
                )}
              </div>
            </>
          ) : null}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t">
          <button
            onClick={onClose}
            className="w-full py-2 px-4 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
