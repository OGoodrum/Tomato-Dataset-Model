import os                                                                                                               
import time                                                                                                             
import argparse                                                                                                         
import cv2                                                                                                              
import torch                                                                                                            
from ultralytics import YOLO                                                                                            
                                                                                                                            
def parse_args():                                                                                                       
    parser = argparse.ArgumentParser(description="YOLO Webcam Inference")                                               
    parser.add_argument(                                                                                                
        "--model",                                                                                                      
        type=str,                                                                                                       
        default="./CVResults/content/runs/detect/train/weights/last.pt",                                                
        help="Path to YOLO model weights (.pt file)"                                                                    
    )                                                                                                                   
    parser.add_argument(                                                                                                
        "--source",                                                                                                     
        type=int,                                                                                                       
        default=0,                                                                                                      
        help="Webcam source index (default: 0)"                                                                         
    )                                                                                                                   
    parser.add_argument(                                                                                                
        "--conf",                                                                                                       
        type=float,                                                                                                     
        default=0.5,                                                                                                    
        help="Confidence threshold (default: 0.5)"                                                                      
    )                                                                                                                   
    return parser.parse_args()                                                                                          
                                                                                                                            
def main():                                                                                                             
    args = parse_args()                                                                                                 
                                                                                                                            
    # 1. Gracefully check if model exists                                                                               
    if not os.path.exists(args.model):                                                                                  
        print(f"Error: Model weights not found at '{args.model}'")                                                      
        print("Please check the path or verify your training output.")                                                  
        return                                                                                                          
                                                                                                                            
    print(f"Loading YOLO model from {args.model}...")                                                                   
    model = YOLO(args.model)                                                                                            
                                                                                                                            
    # Automatically detect best hardware accelerator                                                                    
    device = "cuda" if torch.cuda.is_available() else "cpu"                                                             
    print(f"Using execution device: {device}")                                                                          
                                                                                                                            
    # 2. Safe webcam initialization                                                                                     
    print(f"Opening webcam source {args.source}...")                                                                    
    cap = cv2.VideoCapture(args.source)                                                                                 
                                                                                                                            
    if not cap.isOpened():                                                                                              
        print(f"Error: Could not open webcam source {args.source}.")                                                    
        return                                                                                                          
                                                                                                                            
    # Track time for FPS overlays                                                                                       
    prev_time = 0                                                                                                       
                                                                                                                        
    print("Starting inference. Press 'q' or close the window to exit.")                                                 
    while True:                                                                                                         
        # 3. Safe frame retrieval                                                                                       
        ret, frame = cap.read()                                                                                         
        if not ret or frame is None:                                                                                    
            print("Error: Failed to read frame from webcam.")                                                           
            break                                                                                                       
                                                                                                                        
        # 4. Optimize inference with conf threshold and verbose=False                                                   
        results = model.predict(frame, conf=args.conf, device=device, verbose=False)[0]                                 
                                                                                                                        
        # Draw bounding boxes and labels                                                                                
        for result in results.boxes.data.tolist():                                                                      
            if len(result) >= 6:                                                                                        
                x1, y1, x2, y2, conf, cls = result[:6]                                                                  
                cls = int(cls)                                                                                          
                label = f"{model.names[cls]} {conf:.2f}"                                                                
                                                                                                                        
                # Draw bounding box and label text                                                                      
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)                            
                cv2.putText(                                                                                            
                    frame,                                                                                              
                    label,                                                                                              
                    (int(x1), int(y1) - 10),                                                                            
                    cv2.FONT_HERSHEY_SIMPLEX,                                                                           
                    0.5,                                                                                                
                    (255, 0, 0),                                                                                        
                    2                                                                                                   
                )                                                                                                       
                                                                                                                        
        # 5. FPS metric overlay                                                                                         
        curr_time = time.time()                                                                                         
        fps = 1.0 / (curr_time - prev_time) if prev_time > 0 else 0.0                                                   
        prev_time = curr_time                                                                                           
        cv2.putText(                                                                                                    
            frame,                                                                                                      
            f"FPS: {fps:.1f}",                                                                                          
            (20, 40),                                                                                                   
            cv2.FONT_HERSHEY_SIMPLEX,                                                                                   
            0.7,                                                                                                        
            (0, 255, 0),                                                                                                
            2                                                                                                           
        )                                                                                                               
                                                                                                                        
        # Render window                                                                                                 
        window_name = "Tomato Detection - Webcam"                                                                       
        cv2.imshow(window_name, frame)                                                                                  
                                                                                                                        
        # Exit keyboard shortcut                                                                                        
        if cv2.waitKey(1) & 0xFF == ord("q"):                                                                           
            break                                                                                                       
                                                                                                                        
        # Exit if the GUI window is closed manually                                                                     
        try:                                                                                                            
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:                                            
                break                                                                                                   
        except cv2.error:                                                                                               
            break                                                                                                       
                                                                                                                        
    # Clean up resources                                                                                                
    cap.release()                                                                                                       
    cv2.destroyAllWindows()                                                                                             
    print("Resources released. WebCamVision session closed.")                                                           
                                                                                                                        
if __name__ == "__main__":                                                                                              
        main()