import os
import threading
import time
from datetime import datetime
import logging

import cv2
from ultralytics import YOLO

from src.config import Config
from src.services.database import log_detection
from src.services.storage import upload_file

logger = logging.getLogger(__name__)

_model = None
_camera: cv2.VideoCapture = None
_camera_lock = threading.Lock()


def get_yolo_model() -> YOLO:
    global _model
    if _model is None:
        path = Config.MODEL_PATH if os.path.exists(Config.MODEL_PATH) else Config.FALLBACK_MODEL_PATH
        logger.info(f"[Model] Loading model: {path}...")
        _model = YOLO(path)
    return _model


def get_camera() -> cv2.VideoCapture:
    global _camera
    if _camera is None:
        logger.info("[Camera] Initializing camera...")
        # Initialize webcam                                                                                                                         
        _camera = cv2.VideoCapture(0)                                                                                                                   
        _camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolutions improve performance                                                             
        _camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return _camera


def generate_frames():
    cap = get_camera()
    model = get_yolo_model()

    logger.debug("[DEBUG] Started generate_frames generator...")
    if not cap.isOpened():
        logger.error("[DEBUG] Error: Camera is not open!")
        return

    while True:
        with _camera_lock:
            success, frame = cap.read()
        if not success:
            logger.error("[DEBUG] Error: Failed to read frame from camera.")
            break

        # Run inference (stream=True optimizes memory; conf=0.5 filters early)
        try:
            results = model.predict(frame, conf=0.5, verbose=False, stream=True)
            for r in results:
                # Render bounding boxes and labels directly onto the frame
                frame = r.plot()
        except Exception as e:
            logger.warning(f"[DEBUG] Model inference failed: {e}")
            break

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            logger.error("[DEBUG] Error: Failed to encode frame to JPEG.")
            continue

        frame_bytes = buffer.tobytes()

        # Yield the image block using multipart/x-mixed-replace mimetype
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def background_db_logger():
    logger.info("[DB Logger] Started background logger thread")
    cap = get_camera()
    model = get_yolo_model()

    while True:
        time.sleep(Config.LOG_INTERVAL)

        with _camera_lock:
            success, frame = cap.read()
        if not success or frame is None:
            continue

        try:
            results = model.predict(frame, conf=0.5, verbose=False)

            for r in results:
                # Get counts
                total = len(r.boxes)
                # Assuming class 0 = ripe, 1 = unripe, 2 = diseased (change based on your model.names)
                classes = r.boxes.cls.tolist()
                logger.info(f"[DB Logger] Detected {total} objects: {classes}")

                # 3. Save the annotated frame locally
                annotated_frame = r.plot()
                temp_filename = "temp_snapshot.jpg"
                cv2.imwrite(temp_filename, annotated_frame)

                # 4. Upload snapshot to storage bucket and get public URL
                # (See previous steps for Cloudflare R2 / Supabase Storage upload)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_key = f"device_{Config.DEVICE_ID}/{timestamp}_snapshot.jpg"

                upload_file(temp_filename, image_key)

                logger.info("[DB Logger] Upload successful!")

                public_image_url = f"https://pub-61e76408148846dfb873bd72b8b24454.r2.dev/{image_key}"

                # 5. Insert to Supabase DB                                                                
                log_detection(image_url=public_image_url,
                            total=total,
                            image_key=f"device_{Config.DEVICE_ID}/{timestamp}_snapshot.jpg",
                            early_blight=classes.count(0),
                            healthy=classes.count(1),
                            late_blight=classes.count(2),
                            leaf_miner=classes.count(3),
                            leaf_mold=classes.count(4),
                            mosaic_virus=classes.count(5),
                            septoria=classes.count(6),
                            spider_mites=classes.count(7),
                            yellow_leaf_curl_virus=classes.count(8))
        except Exception as e:
            logger.error(f"[DB Logger] Error running inference/upload: {e}")


_logger_started = False
def start_background_logger():
    global _logger_started
    if not _logger_started:
        thread = threading.Thread(target=background_db_logger, daemon=True)
        thread.start()
        _logger_started = True
        logger.info("[DB Logger] Spawned background thread.")
