import { useState, useRef, useCallback } from 'react';

interface ResumeUploadProps {
  onUpload: (formData: FormData, onProgress: (pct: number) => void) => Promise<void>;
  isUploading: boolean;
}

const MAX_SIZE = 5 * 1024 * 1024; // 5MB

export default function ResumeUpload({ onUpload, isUploading }: ResumeUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resumeName, setResumeName] = useState('');
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string => {
    if (file.type !== 'application/pdf') return 'Only PDF files are accepted.';
    if (file.size > MAX_SIZE) return 'File size must be under 5MB.';
    return '';
  };

  const handleFileSelect = (file: File) => {
    const err = validateFile(file);
    if (err) {
      setError(err);
      setSelectedFile(null);
      return;
    }
    setError('');
    setSelectedFile(file);
    // Pre-fill name from filename (strip .pdf extension)
    if (!resumeName) {
      setResumeName(file.name.replace(/\.pdf$/i, ''));
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  }, [resumeName]);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFileSelect(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    const name = resumeName.trim() || selectedFile.name.replace(/\.pdf$/i, '');
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('name', name);

    setUploadProgress(0);
    await onUpload(formData, (pct) => setUploadProgress(pct));

    // Reset form on success
    setSelectedFile(null);
    setResumeName('');
    setUploadProgress(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Resume</h2>
      <form onSubmit={handleSubmit} className="space-y-4">

        {/* Drop Zone */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={() => setIsDragging(false)}
          onClick={() => fileInputRef.current?.click()}
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors duration-200
            ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'}
            ${selectedFile ? 'border-green-400 bg-green-50' : ''}
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            className="hidden"
            onChange={handleInputChange}
          />

          {selectedFile ? (
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-sm font-medium text-green-700">{selectedFile.name}</p>
              <p className="text-xs text-green-600">
                {(selectedFile.size / 1024).toFixed(1)} KB — click to change
              </p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p className="text-sm font-medium text-gray-700">
                Drag & drop your PDF here, or <span className="text-blue-600">browse</span>
              </p>
              <p className="text-xs text-gray-400">PDF only · Max 5MB</p>
            </div>
          )}
        </div>

        {/* Error */}
        {error && (
          <p className="text-sm text-red-600 flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {error}
          </p>
        )}

        {/* Name Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Resume Name <span className="text-gray-400">(optional)</span>
          </label>
          <input
            type="text"
            value={resumeName}
            onChange={(e) => setResumeName(e.target.value)}
            placeholder="e.g. Software Engineer Resume"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Progress Bar */}
        {isUploading && (
          <div className="space-y-1">
            <div className="flex justify-between text-xs text-gray-500">
              <span>Uploading...</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={!selectedFile || isUploading}
          className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
        >
          {isUploading ? (
            <>
              <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Uploading...
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload Resume
            </>
          )}
        </button>
      </form>
    </div>
  );
}
