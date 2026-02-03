import cv2
import numpy as np
from typing import List, Tuple
from app.models.schemas import BoundingBox, Point


class TextDetectionService:
    """Service for detecting text regions in images"""
    
    def detect_text_regions(self, image_path: str) -> List[Tuple[BoundingBox, float]]:
        """
        Detect text regions in an image using OpenCV
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of tuples (BoundingBox, confidence)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply binary threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        height, width = image.shape[:2]
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter out too small or too large regions
            area = w * h
            if area < 100 or area > (width * height * 0.8):
                continue
            
            # Filter out regions that are too wide or too narrow
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio > 20 or aspect_ratio < 0.05:
                continue
            
            bbox = BoundingBox(x=x, y=y, width=w, height=h)
            confidence = min(1.0, area / 10000)  # Mock confidence based on size
            regions.append((bbox, confidence))
        
        return regions
    
    def draw_boxes(self, image_path: str, regions: List[Tuple[BoundingBox, float]], 
                   output_path: str) -> None:
        """
        Draw bounding boxes on image for debugging
        
        Args:
            image_path: Path to original image
            regions: List of detected regions
            output_path: Path to save annotated image
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        for bbox, confidence in regions:
            # Draw rectangle
            cv2.rectangle(
                image,
                (bbox.x, bbox.y),
                (bbox.x + bbox.width, bbox.y + bbox.height),
                (0, 255, 0),
                2
            )
            
            # Add confidence label
            label = f"{confidence:.2f}"
            cv2.putText(
                image,
                label,
                (bbox.x, bbox.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
        
        cv2.imwrite(output_path, image)
