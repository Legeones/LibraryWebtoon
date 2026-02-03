import cv2
import numpy as np
from typing import List, Tuple
from paddleocr import PaddleOCR
from app.models.schemas import BoundingBox, Point


class TextDetectionService:
    """Service for detecting text regions in images using PaddleOCR"""
    
    def __init__(self):
        # Initialize PaddleOCR with detection only
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en',  # Language doesn't matter for detection only
            det=True,    # Enable detection
            rec=False,   # Disable recognition (we'll do that separately)
            show_log=False
        )
    
    def detect_text_regions(self, image_path: str) -> List[Tuple[BoundingBox, float]]:
        """
        Detect text regions in an image using PaddleOCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of tuples (BoundingBox, confidence)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Use PaddleOCR for detection
        result = self.ocr.ocr(image_path, det=True, rec=False, cls=False)
        
        regions = []
        
        if result and result[0]:
            for detection in result[0]:
                # PaddleOCR returns boxes as [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                box = detection[0] if isinstance(detection, (list, tuple)) else detection
                
                # Convert polygon to bounding box
                points = np.array(box)
                x_min = int(np.min(points[:, 0]))
                y_min = int(np.min(points[:, 1]))
                x_max = int(np.max(points[:, 0]))
                y_max = int(np.max(points[:, 1]))
                
                width = x_max - x_min
                height = y_max - y_min
                
                # Filter out too small regions
                if width < 10 or height < 10:
                    continue
                
                bbox = BoundingBox(x=x_min, y=y_min, width=width, height=height)
                # PaddleOCR detection confidence is high by default
                confidence = 0.95
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
