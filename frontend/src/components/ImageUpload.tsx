import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { jobApi } from '@/lib/api';
import { Job } from '@/types';

interface ImageUploadProps {
  onJobCreated: (job: Job) => void;
}

export default function ImageUpload({ onJobCreated }: ImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploading(true);
    setError(null);

    try {
      const job = await jobApi.createJob(file, {
        sourceLanguage: 'ja',
        targetLanguage: 'en',
      });
      onJobCreated(job);
    } catch (err) {
      setError('Failed to upload and process image');
      console.error(err);
    } finally {
      setUploading(false);
    }
  }, [onJobCreated]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp'],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          {uploading ? (
            <p className="text-gray-600">Processing...</p>
          ) : isDragActive ? (
            <p className="text-blue-600">Drop the panel image here</p>
          ) : (
            <div>
              <p className="text-gray-600">Drag and drop a panel image, or click to select</p>
              <p className="text-sm text-gray-500 mt-2">PNG, JPG, JPEG, or WEBP</p>
            </div>
          )}
        </div>
      </div>
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}
    </div>
  );
}
