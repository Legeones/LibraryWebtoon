import React, { useState, useEffect } from 'react';
import { Job, ProcessingResult, TextRegion } from '@/types';

interface RegionEditorProps {
  job: Job;
}

export default function RegionEditor({ job }: RegionEditorProps) {
  const [regions, setRegions] = useState<TextRegion[]>([]);
  const [selectedRegion, setSelectedRegion] = useState<TextRegion | null>(null);

  useEffect(() => {
    if (job.resultJson) {
      try {
        const result: ProcessingResult = JSON.parse(job.resultJson);
        setRegions(result.regions || []);
      } catch (error) {
        console.error('Failed to parse result JSON:', error);
      }
    }
  }, [job.resultJson]);

  const handleRegionUpdate = (id: string, field: keyof TextRegion, value: any) => {
    setRegions((prev) =>
      prev.map((region) =>
        region.id === id ? { ...region, [field]: value } : region
      )
    );
  };

  if (regions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Text Regions</h2>
        <p className="text-gray-500">No text regions detected yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b">
        <h2 className="text-xl font-semibold">Text Regions</h2>
        <p className="text-sm text-gray-600 mt-1">
          Edit OCR results, translations, and styling for each detected region
        </p>
      </div>

      <div className="divide-y max-h-[600px] overflow-y-auto">
        {regions.map((region) => (
          <div
            key={region.id}
            className={`p-4 cursor-pointer transition-colors ${
              selectedRegion?.id === region.id ? 'bg-blue-50' : 'hover:bg-gray-50'
            }`}
            onClick={() => setSelectedRegion(region)}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-sm font-medium text-gray-900">{region.id}</span>
                  <span className="text-xs text-gray-500">
                    Confidence: {(region.confidence * 100).toFixed(0)}%
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      OCR Text
                    </label>
                    <input
                      type="text"
                      value={region.ocr_text}
                      onChange={(e) =>
                        handleRegionUpdate(region.id, 'ocr_text', e.target.value)
                      }
                      className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Original text..."
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Translation
                    </label>
                    <textarea
                      value={region.translated_text}
                      onChange={(e) =>
                        handleRegionUpdate(region.id, 'translated_text', e.target.value)
                      }
                      rows={2}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Translated text..."
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Font Size
                      </label>
                      <input
                        type="number"
                        value={region.font_size}
                        onChange={(e) =>
                          handleRegionUpdate(region.id, 'font_size', parseInt(e.target.value))
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
                        min="8"
                        max="72"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Alignment
                      </label>
                      <select
                        value={region.alignment}
                        onChange={(e) =>
                          handleRegionUpdate(region.id, 'alignment', e.target.value)
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="left">Left</option>
                        <option value="center">Center</option>
                        <option value="right">Right</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Stroke Width
                      </label>
                      <input
                        type="number"
                        value={region.stroke_width}
                        onChange={(e) =>
                          handleRegionUpdate(region.id, 'stroke_width', parseInt(e.target.value))
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
                        min="0"
                        max="10"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Text Color
                      </label>
                      <input
                        type="color"
                        value={region.text_color}
                        onChange={(e) =>
                          handleRegionUpdate(region.id, 'text_color', e.target.value)
                        }
                        className="w-full h-10 border border-gray-300 rounded-md cursor-pointer"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Stroke Color
                      </label>
                      <input
                        type="color"
                        value={region.stroke_color}
                        onChange={(e) =>
                          handleRegionUpdate(region.id, 'stroke_color', e.target.value)
                        }
                        className="w-full h-10 border border-gray-300 rounded-md cursor-pointer"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 bg-gray-50 border-t">
        <button
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          disabled={regions.length === 0}
          onClick={() => {
            // TODO: Implement re-render functionality
            console.log('Re-render with updated regions:', regions);
            alert('Re-render functionality will be implemented to call the backend API');
          }}
        >
          Re-render with Changes
        </button>
      </div>
    </div>
  );
}
