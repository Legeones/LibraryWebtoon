import cv2
import pytesseract
from typing import Tuple


class OCRService:
    """Service for performing OCR on text regions"""
    
    def __init__(self):
        # Configure tesseract (can be customized via environment variables)
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        pass
    
    def extract_text(self, image_path: str, x: int, y: int, 
                    width: int, height: int, language: str = "jpn") -> Tuple[str, float]:
        """
        Extract text from a specific region of an image
        
        Args:
            image_path: Path to the image
            x, y: Top-left coordinates of region
            width, height: Dimensions of region
            language: Tesseract language code (jpn, eng, etc.)
            
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
        
        # Convert to grayscale
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to improve OCR accuracy
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Perform OCR with detailed data
        try:
            data = pytesseract.image_to_data(
                binary,
                lang=language,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate average confidence
            text_parts = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if conf > 0:  # Valid detection
                    text = data['text'][i].strip()
                    if text:
                        text_parts.append(text)
                        confidences.append(conf)
            
            extracted_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return extracted_text, avg_confidence / 100.0  # Normalize to 0-1
            
        except Exception as e:
            print(f"OCR error: {e}")
            return "", 0.0
