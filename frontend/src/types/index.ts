export interface TextRegion {
  id: string;
  bbox: BoundingBox;
  polygon?: Point[];
  confidence: number;
  orientation: number;
  ocr_text: string;
  ocr_confidence: number;
  translated_text: string;
  font_size: number;
  font_family: string;
  alignment: 'left' | 'center' | 'right';
  stroke_width: number;
  stroke_color: string;
  text_color: string;
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Point {
  x: number;
  y: number;
}

export interface Job {
  id: string;
  status: 'QUEUED' | 'PROCESSING' | 'DONE' | 'FAILED';
  originalImagePath?: string;
  debugBoxesImagePath?: string;
  maskImagePath?: string;
  cleanImagePath?: string;
  finalImagePath?: string;
  resultJson?: string;
  processingTime?: number;
  errorMessage?: string;
  createdAt: string;
  completedAt?: string;
  version: number;
}

export interface ProcessingResult {
  job_id: string;
  status: string;
  regions: TextRegion[];
  original_image_path?: string;
  debug_boxes_image_path?: string;
  mask_image_path?: string;
  clean_image_path?: string;
  final_image_path?: string;
  processing_time: number;
  error_message?: string;
  metadata: Record<string, any>;
}
