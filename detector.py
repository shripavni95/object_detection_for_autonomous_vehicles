import cv2
import torch
import numpy as np

class ObjectDetector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    def detect_image(self, image_path):
        results = self.model(image_path)
        img = cv2.imread(image_path)
        detections = results.pandas().xyxy[0]

        for _, row in detections.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = f"{row['name']} {row['confidence']:.2f}"

            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Get text size and set position
            font_scale = 0.5
            thickness = 1
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            text_x, text_y = x1, y1 - 10  # Position text above bounding box

            # Background rectangle for text
            overlay = img.copy()
            cv2.rectangle(overlay, (text_x, text_y - text_size[1] - 4), (text_x + text_size[0] + 6, text_y + 4), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

            # Put text label
            cv2.putText(img, label, (text_x + 3, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

        return img
