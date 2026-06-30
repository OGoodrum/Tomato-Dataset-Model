import os                                                                                                                                   
import cv2                                                                                                                                  
from flask import Flask, Response, render_template_string                                                                      
from ultralytics import YOLO                                                                                                                
                                                                                                                                            
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
                                                                                                                                            
def generate_frames():                                                                                                                      
    while True:                                                                                                                             
        success, frame = cap.read()                                                                                                         
        if not success:                                                                                                                     
            break                                                                                                                           
                                                                                                                                            
        # Run inference (stream=True optimizes memory; conf=0.5 filters early)                                                              
        results = model.predict(frame, conf=0.5, verbose=False, stream=True)                                                                
                                                                                                                                            
        for r in results:                                                                                                                   
            # Render bounding boxes and labels directly onto the frame                                                                      
            frame = r.plot()                                                                                                                
                                                                                                                                            
        # Encode the frame in JPEG format                                                                                                   
        ret, buffer = cv2.imencode('.jpg', frame)                                                                                           
        if not ret:                                                                                                                         
            continue                                                                                                                        
                                                                                                                                            
        frame_bytes = buffer.tobytes()                                                                                                      
                                                                                                                                            
        # Yield the image block using multipart/x-mixed-replace mimetype                                                                    
        yield (b'--frame\r\n'                                                                                                               
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')                                                                 
                                                                                                                                            
# Simple HTML Template to view the stream                                                                                                   
INDEX_HTML = """                                                                                                                            
<!DOCTYPE html>                                                                                                                             
<html>                                                                                                                                      
<head>                                                                                                                                      
    <title>YOLOv8 Tomato Detection Stream</title>                                                                                           
    <style>                                                                                                                                 
        body {                                                                                                                              
            font-family: Arial, sans-serif;                                                                                                 
            background: #121212;                                                                                                            
            color: #ffffff;                                                                                                                 
            text-align: center;                                                                                                             
            padding: 20px;                                                                                                                  
        }                                                                                                                                   
        h1 { color: #ff5722; }                                                                                                              
        .stream-container {                                                                                                                 
            margin: 20px auto;                                                                                                              
            border: 5px solid #ff5722;                                                                                                      
            border-radius: 10px;                                                                                                            
            display: inline-block;                                                                                                          
            overflow: hidden;                                                                                                               
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);                                                                                         
        }                                                                                                                                   
        img { display: block; max-width: 100%; height: auto; }                                                                              
    </style>                                                                                                                                
</head>                                                                                                                                     
<body>                                                                                                                                      
    <h1>Live Tomato Detection Stream</h1>                                                                                                   
    <p>Streaming from Raspberry Pi</p>                                                                                                      
    <div class="stream-container">                                                                                                          
        <img src="/video_feed" width="640" height="480" />                                                                                  
    </div>                                                                                                                                  
</body>                                                                                                                                     
</html>                                                                                                                                     
"""                                                                                                                                         
                                                                                                                                            
@app.route('/')                                                                                                                             
def index():                                                                                                                                
    """Video streaming home page."""                                                                                                        
    return render_template_string(INDEX_HTML)                                                                                               
                                                                                                                                            
@app.route('/video_feed')                                                                                                                   
def video_feed():                                                                                                                           
    """Video streaming route. Put this in the src attribute of an img tag."""                                                               
    return Response(generate_frames(),                                                                                                      
                    mimetype='multipart/x-mixed-replace; boundary=frame')                                                                   
                                                                                                                                            
if __name__ == '__main__':                                                                                                                  
    # RPi default port is 5000. Host 0.0.0.0 listens to all local IPs.                                                                      
    app.run(host='0.0.0.0', port=5000, threaded=True)
