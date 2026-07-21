import os
import time
from datetime import datetime
import threading

import cv2
from ultralytics import YOLO

from src.config import Config
from src.services.database import log_detection
from src.services.storage import upload_file

_model = None
_camera = None
_camera_lock = threading.Lock()

def get_yolo_model() -> YOLO:
    global _model
    if _model is None:
        path = Config.MODEL_PATH if os.path.exists(Config.MODEL_PATH) else Config.FALLBACK_MODEL_PATH
        print(f"[Model] Loading model: {path}...")
        _model = YOLO(path)
    return _model

def get_camera() -> cv2.VideoCapture:
    global _camera
    if _camera is None:
        print("[Camera] Initializing camera...")
        # Initialize webcam                                                                                                                         
        _camera = cv2.VideoCapture(0)                                                                                                                   
        _camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolutions improve performance                                                             
        _camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return _camera

def generate_frames():
    cap = get_camera()
    model = get_yolo_model()

    print("[DEBUG] Started generate_frames generator...")                                                                                   
    if not cap.isOpened():                                                                                                                  
        print("[DEBUG] Error: Camera is not open!")                                                                                         
        return                                                                                                                     
                                                                                                                                            
    while True:
        with _camera_lock:                                                                                                                            
            success, frame = cap.read()                                                                                                         
        if not success:                                                                                                                     
            print("[DEBUG] Error: Failed to read frame from camera.")                                                                       
            break                                                                                                                           
                                                                                                                                            
        # Run inference (stream=True optimizes memory; conf=0.5 filters early)                                                              
        try:                                                                                                                                
            results = model.predict(frame, conf=0.5, verbose=False, stream=True)                                                            
            for r in results:                                                                                                               
                # Render bounding boxes and labels directly onto the frame                                                                  
                frame = r.plot()                                                                                                            
        except Exception as e:                                                                                                              
            print(f"[DEBUG] Model inference failed: {e}")                                                                                   
            break                                                                                                                           
                                                                                                                                            
        # Encode the frame in JPEG format                                                                                                   
        ret, buffer = cv2.imencode('.jpg', frame)                                                                                           
        if not ret:                                                                                                                         
            print("[DEBUG] Error: Failed to encode frame to JPEG.")                                                                         
            continue                                                                                                                        
                                                                                                                                            
        frame_bytes = buffer.tobytes()                                                                                                      
                                                                                                                                            
        # Yield the image block using multipart/x-mixed-replace mimetype                                                                    
        yield (b'--frame\r\n'                                                                                                               
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

