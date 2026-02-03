from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"


class Point(BaseModel):
    x: int
    y: int


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class TextRegion(BaseModel):
    id: str
    bbox: BoundingBox
    polygon: Optional[List[Point]] = None
    confidence: float = Field(ge=0.0, le=1.0)
    orientation: float = 0.0
    ocr_text: str = ""
    ocr_confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    translated_text: str = ""
    font_size: int = 12
    font_family: str = "Arial"
    alignment: str = "left"  # left, center, right
    stroke_width: int = 0
    stroke_color: str = "#000000"
    text_color: str = "#000000"


class ProcessingOptions(BaseModel):
    source_language: str = "ja"
    target_language: str = "en"
    ocr_engine: str = "paddleocr"  # paddleocr
    translation_engine: str = "mock"  # mock, deepl, google (future)
    inpaint_method: str = "telea"  # telea, ns (OpenCV methods)
    detect_text: bool = True
    perform_ocr: bool = True
    perform_translation: bool = True
    perform_inpainting: bool = True
    perform_typesetting: bool = True


class ProcessingResult(BaseModel):
    job_id: str
    status: JobStatus
    regions: List[TextRegion] = []
    original_image_path: Optional[str] = None
    debug_boxes_image_path: Optional[str] = None
    mask_image_path: Optional[str] = None
    clean_image_path: Optional[str] = None
    final_image_path: Optional[str] = None
    processing_time: float = 0.0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = {}


class RerenderRequest(BaseModel):
    job_id: str
    regions: List[TextRegion]
    clean_image_path: str


class ProcessRequest(BaseModel):
    job_id: str
    options: ProcessingOptions = ProcessingOptions()
