import React, { useState } from 'react';
import { Job } from '@/types';
import { jobApi } from '@/lib/api';

interface ImageViewerProps {
  job: Job;
}

type ImageType = 'original' | 'debug' | 'mask' | 'clean' | 'final';

export default function ImageViewer({ job }: ImageViewerProps) {
  const [selectedType, setSelectedType] = useState<ImageType>('original');

  const imageTypes: { type: ImageType; label: string; available: boolean }[] = [
    { type: 'original', label: 'Original', available: !!job.originalImagePath },
    { type: 'debug', label: 'Detected Boxes', available: !!job.debugBoxesImagePath },
    { type: 'mask', label: 'Mask', available: !!job.maskImagePath },
    { type: 'clean', label: 'Clean', available: !!job.cleanImagePath },
    { type: 'final', label: 'Final', available: !!job.finalImagePath },
  ];

  const availableTypes = imageTypes.filter((t) => t.available);

  if (availableTypes.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-500">No images available yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="border-b">
        <div className="flex space-x-1 p-2">
          {availableTypes.map(({ type, label }) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`
                px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${
                  selectedType === type
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }
              `}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="p-6">
        <div className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden">
          <img
            src={jobApi.getJobImage(job.id, selectedType)}
            alt={`${selectedType} view`}
            className="w-full h-full object-contain"
            onError={(e) => {
              console.error('Failed to load image:', selectedType);
              e.currentTarget.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect width="400" height="300" fill="%23f3f4f6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" fill="%239ca3af"%3EImage not available%3C/text%3E%3C/svg%3E';
            }}
          />
        </div>

        <div className="mt-4 text-sm text-gray-600">
          <p className="font-medium mb-2">View Description:</p>
          <ul className="space-y-1">
            {selectedType === 'original' && <li>• Original uploaded panel image</li>}
            {selectedType === 'debug' && <li>• Detected text regions with bounding boxes</li>}
            {selectedType === 'mask' && <li>• Binary mask showing text areas to clean</li>}
            {selectedType === 'clean' && <li>• Image with text removed via inpainting</li>}
            {selectedType === 'final' && <li>• Final result with translated text rendered</li>}
          </ul>
        </div>
      </div>
    </div>
  );
}
