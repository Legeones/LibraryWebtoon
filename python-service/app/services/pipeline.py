import os
import time
import uuid
from pathlib import Path
from typing import List, Tuple
from app.models.schemas import (
    ProcessingResult, ProcessingOptions, TextRegion, BoundingBox,
    JobStatus
)
from app.services.text_detection import TextDetectionService
from app.services.ocr import OCRService
from app.services.translation import TranslationService
from app.services.inpainting import InpaintingService
from app.services.typesetting import TypesettingService


class ProcessingPipeline:
    """Main processing pipeline orchestrating all services"""
    
    def __init__(self, storage_path: str = "/tmp/webtoon-processing"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.text_detector = TextDetectionService()
        self.ocr_service = OCRService()
        self.translation_service = TranslationService()
        self.inpainting_service = InpaintingService()
        self.typesetting_service = TypesettingService()
    
    async def process_image(self, image_path: str, job_id: str, 
                           options: ProcessingOptions) -> ProcessingResult:
        """
        Complete processing pipeline for a panel image
        
        Args:
            image_path: Path to input image
            job_id: Unique job identifier
            options: Processing options
            
        Returns:
            ProcessingResult with all outputs
        """
        start_time = time.time()
        result = ProcessingResult(job_id=job_id, status=JobStatus.PROCESSING)
        
        try:
            # Create job directory
            job_dir = self.storage_path / job_id
            job_dir.mkdir(exist_ok=True)
            
            result.original_image_path = str(job_dir / "original.png")
            result.debug_boxes_image_path = str(job_dir / "debug_boxes.png")
            result.mask_image_path = str(job_dir / "mask.png")
            result.clean_image_path = str(job_dir / "clean.png")
            result.final_image_path = str(job_dir / "final.png")
            
            # Copy original image
            import shutil
            shutil.copy(image_path, result.original_image_path)
            
            # Step 1: Text Detection
            if options.detect_text:
                detected_regions = self.text_detector.detect_text_regions(
                    result.original_image_path
                )
                
                # Draw debug boxes
                self.text_detector.draw_boxes(
                    result.original_image_path,
                    detected_regions,
                    result.debug_boxes_image_path
                )
                
                # Convert to TextRegion objects
                regions = []
                for i, (bbox, confidence) in enumerate(detected_regions):
                    region = TextRegion(
                        id=f"region_{i}",
                        bbox=bbox,
                        confidence=confidence
                    )
                    regions.append(region)
                
                result.regions = regions
            
            # Step 2: OCR
            if options.perform_ocr and result.regions:
                for region in result.regions:
                    text, ocr_conf = self.ocr_service.extract_text(
                        result.original_image_path,
                        region.bbox.x,
                        region.bbox.y,
                        region.bbox.width,
                        region.bbox.height,
                        language=self._map_language_code(options.source_language)
                    )
                    region.ocr_text = text
                    region.ocr_confidence = ocr_conf
            
            # Step 3: Translation
            if options.perform_translation and result.regions:
                for region in result.regions:
                    if region.ocr_text:
                        translated = await self.translation_service.translate(
                            region.ocr_text,
                            options.source_language,
                            options.target_language,
                            options.translation_engine
                        )
                        region.translated_text = translated
            
            # Step 4: Inpainting
            if options.perform_inpainting and result.regions:
                # Create mask
                self.inpainting_service.create_mask(
                    result.original_image_path,
                    result.regions,
                    result.mask_image_path
                )
                
                # Perform inpainting
                self.inpainting_service.inpaint_image(
                    result.original_image_path,
                    result.mask_image_path,
                    result.clean_image_path,
                    options.inpaint_method
                )
            else:
                # Copy original as clean if no inpainting
                import shutil
                shutil.copy(result.original_image_path, result.clean_image_path)
            
            # Step 5: Typesetting
            if options.perform_typesetting and result.regions:
                self.typesetting_service.render_text(
                    result.clean_image_path,
                    result.regions,
                    result.final_image_path
                )
            else:
                # Copy clean as final if no typesetting
                import shutil
                shutil.copy(result.clean_image_path, result.final_image_path)
            
            result.status = JobStatus.DONE
            result.processing_time = time.time() - start_time
            
        except Exception as e:
            result.status = JobStatus.FAILED
            result.error_message = str(e)
            result.processing_time = time.time() - start_time
        
        return result
    
    async def rerender(self, clean_image_path: str, regions: List[TextRegion],
                      job_id: str) -> str:
        """
        Re-render text on clean image without full pipeline
        
        Args:
            clean_image_path: Path to cleaned image
            regions: Updated text regions
            job_id: Job identifier
            
        Returns:
            Path to new final image
        """
        job_dir = self.storage_path / job_id
        job_dir.mkdir(exist_ok=True)
        
        output_path = str(job_dir / f"final_{int(time.time())}.png")
        
        self.typesetting_service.render_text(
            clean_image_path,
            regions,
            output_path
        )
        
        return output_path
    
    def _map_language_code(self, lang_code: str) -> str:
        """Map ISO language codes to PaddleOCR language codes"""
        mapping = {
            "ja": "japan",
            "en": "en",
            "ko": "korean",
            "zh": "ch",
            "fr": "french",
            "de": "german",
            "es": "spanish",
        }
        return mapping.get(lang_code, "en")
