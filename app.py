import time
import os
import threading
import logging
from datetime import datetime

import cv2
from ultralytics import YOLO

from flask import Flask, Response, render_template                                                                     
import sentry_sdk

from supabase import create_client, Client
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Sentry for error tracking
sentry_sdk.init(
    dsn="https://e80b87c7a6d9121f37069f69b2f53329@o4511668378992640.ingest.us.sentry.io/4511668425785344",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_logs=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profile_session_sample_rate to 1.0 to profile 100%
    # of profile sessions.
    profile_session_sample_rate=1.0,
)

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("CLOUDFLARE_R2_ENDPOINT"),
    aws_access_key_id=os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
)

BUCKET_NAME = os.getenv("CLOUDFLARE_BUCKET_NAME")
                                                                                                                                            
app = Flask(__name__)                                                                                                                    
                                                                                                                                            
# Load the optimized model (NCNN format is highly recommended for RPi)                                                                      
MODEL_PATH = "./CVResults/content/runs/detect/train/weights/last_ncnn_model"  # Path to your exported NCNN model directory                                                                
if not os.path.exists(MODEL_PATH):                                                                                                          
    # Fallback to PT file if NCNN is not exported yet                                                                                       
    MODEL_PATH = "./CVResults/content/runs/detect/train/weights/last.pt"                                                                                                                  
                                                                                                                                            
print(f"Loading model: {MODEL_PATH}...")                                                                                                    
model = YOLO(MODEL_PATH)                                                                                                                    
                                                                                                                                            
# Initialize webcam                                                                                                                         
cap = cv2.VideoCapture(0)                                                                                                                   
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolutions improve performance                                                             
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize Supabase Client                                                                
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Ensure this is set in your .env file
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")                                             
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define your device ID (must match what is registered in the 'devices' table)                        
DEVICE_ID = os.getenv("DEVICE_ID", 1)  # Default to "1" if not set in .env

LOG_INTERVAL = 30 # Log to the database every 10 minutes (600 seconds)

def background_db_logger():                                                                           
    print("[DB Logger] Started background logger thread.")                                                                                
                                                                                                        
    while True:                                                                                       
        time.sleep(LOG_INTERVAL)                                                                      
                                                                                                        
        # 1. Grab a frame from the running camera                                                     
        success, frame = cap.read()                                                                   
        if not success or frame is None:                                                              
            continue                                                                                  
                                                                                                        
        # 2. Run inference                                                                            
        results = model.predict(frame, conf=0.5, verbose=False)                                       
        for r in results:                                                                             
            # Get counts                                                                              
            total = len(r.boxes)                                                                      
            # Assuming class 0 = ripe, 1 = unripe, 2 = diseased (change based on your model.names)    
            classes = r.boxes.cls.tolist()                                                            
                                                               
            #TODO: Adjust class indices based on your model's class mapping                       

            # 3. Save the annotated frame locally                                                     
            annotated_frame = r.plot()                                                                
            cv2.imwrite("temp_snapshot.jpg", annotated_frame)                                         
                                                                                                        
            # 4. Upload snapshot to storage bucket and get public URL                                 
            # (See previous steps for Cloudflare R2 / Supabase Storage upload)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            s3.upload_file(
                Filename="temp_snapshot.jpg",
                Bucket=BUCKET_NAME,
                Key=f"{timestamp}_snapshot_device_{DEVICE_ID}.jpg",
            )
            print("[DB Logger] Upload successful!")
                       
            public_image_url = "https://your-storage-bucket.com/snapshot.jpg"                         
                                                                                                        
            # 5. Insert to Supabase DB                                                                
            log_detection(public_image_url, total)

def log_detection(image_url, total=0, ripe=0, unripe=0, diseased=0):                                          
    try:                                                                                              
        # Optional: Get Pi CPU temperature                                                            
        cpu_temp = None

        try:                                                                                          
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:                             
                cpu_temp = round(int(f.read()) / 1000.0, 1)                                           
        except Exception:                                                                             
            pass  # Fallback if not running on Pi                                                     
                                                                                                        
        data = {                                                                                      
            "device_id": DEVICE_ID,                                                                   
            "image_url": image_url,                                                                   
            "total_count": total,                                                                     
            "ripe_count": ripe,                                                                       
            "unripe_count": unripe,                                                                   
            "diseased_count": diseased,                                                               
            "cpu_temp": cpu_temp                                                                      
        }                                                                                             
                                                                                                        
        # Insert row into Supabase                                                                    
        response = supabase.table("tomato_detections").insert(data).execute()                         
        print(f"[DB] Logged detection to Supabase: {total} tomatoes found.")                          
        return response.data                                                                          
    except Exception as e:                                                                            
        print(f"[DB] Error logging to Supabase: {e}")                                                 
        return None
                                                                                                                                            
def generate_frames():                                                                                                                      
    print("[DEBUG] Started generate_frames generator...")                                                                                   
    if not cap.isOpened():                                                                                                                  
        print("[DEBUG] Error: Camera is not open!")                                                                                         
        return                                                                                                                              
                                                                                                                                            
    while True:                                                                                                                             
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
                                                                                                                                                                                                                                                                             
                                                                                                                                            
@app.route('/')                                                                                                                             
def index():                                                                                                                                
    """Video streaming home page."""                                                                                                        
    return render_template('index.html')                                                                                               
                                                                                                                                            
@app.route('/video_feed')                                                                                                                   
def video_feed():                                                                                                                           
    """Video streaming route. Put this in the src attribute of an img tag."""                                                               
    return Response(generate_frames(),                                                                                                      
                    mimetype='multipart/x-mixed-replace; boundary=frame')                                                                   
                                                                                                                                            
if __name__ == '__main__':                                                                                                                  
    # Start the background logger thread
    logger_thread = threading.Thread(target=background_db_logger, daemon=True)                                                                  
    logger_thread.start()

    # RPi default port is 5000. Host 0.0.0.0 listens to all local IPs
    app.run(host='0.0.0.0', port=5000, threaded=True)
