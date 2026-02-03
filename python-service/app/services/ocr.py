import cv2
import numpy as np
from paddleocr import PaddleOCR
from typing import Tuple


class OCRService:
    """Service for performing OCR on text regions using PaddleOCR"""
    
    def __init__(self):
        # Initialize PaddleOCR with recognition
        # We'll create language-specific instances as needed
        self.ocr_models = {}
    
    def _get_ocr_model(self, language: str):
        """Get or create PaddleOCR model for specific language"""
        if language not in self.ocr_models:
            self.ocr_models[language] = PaddleOCR(
                use_angle_cls=True,
                lang=language,
                det=False,  # Disable detection (we already have regions)
                rec=True,   # Enable recognition
                show_log=False
            )
        return self.ocr_models[language]
    
    def extract_text(self, image_path: str, x: int, y: int, 
                    width: int, height: int, language: str = "japan") -> Tuple[str, float]:
        """
        Extract text from a specific region of an image using PaddleOCR
        
        Args:
            image_path: Path to the image
            x, y: Top-left coordinates of region
            width, height: Dimensions of region
            language: PaddleOCR language code (japan, en, korean, chinese, etc.)
            
        Returns:
            Tuple of (extracted_text, confidence)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Extract region
        region = image[y:y+height, x:x+width]
        
        if region.size == 0:
            return "", 0.0
        
        # Get OCR model for the language
        ocr = self._get_ocr_model(language)
        
        try:
            # Perform OCR on the region
            # PaddleOCR expects the image array directly
            result = ocr.ocr(region, det=False, rec=True, cls=True)
            
            if not result or not result[0]:
                return "", 0.0
            
            # Extract text and confidence
            text_parts = []
            confidences = []
            
            for line in result[0]:
                if isinstance(line, (list, tuple)) and len(line) >= 2:
                    text = line[1][0] if isinstance(line[1], (list, tuple)) else str(line[1])
                    conf = line[1][1] if isinstance(line[1], (list, tuple)) and len(line[1]) > 1 else 0.9
                    
                    text_parts.append(text)
                    confidences.append(conf)
            
            extracted_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return extracted_text, avg_confidence
            
        except Exception as e:
            print(f"OCR error: {e}")
            return "", 0.0
