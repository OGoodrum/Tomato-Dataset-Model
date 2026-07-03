  No, you do not have to use AWS. While AWS is the industry standard for enterprise applications, it has a steep learning   
  curve and can become expensive quickly (especially with video storage and streaming costs).                               
                                                                                                                            
  For a hobbyist or small-to-medium project, you can build this with a much simpler, modern, and mostly free/low-cost stack.
                                                                                                                            
  Here is how you can architecture this system, the tools you can use, and how the data flows.                              
  ──────                                                                                                                    
  ### The Recommended Stack (Easier & Low Cost)                                                                             
                                                                                                                            
  Instead of AWS, you can use modern "as-a-Service" platforms that have generous free tiers:                                
                                                                                                                            
  1. Website Frontend: Vercel or Netlify (Free)                                                                             
      • Hosts your user interface (built with React, Next.js, or plain HTML/JS).                                            
  2. Database: Supabase (Free Tier)                                                                                         
      • A cloud PostgreSQL database. This is where you store your insights (e.g.,  "2026-07-01 12:00:00 - Detected 3 Ripe   
      Tomatoes, Confidence 88%" ). It also handles user login/authentication.                                               
  3. Video Storage: Cloudflare R2 (Free up to 10GB)                                                                         
      • This is an alternative to AWS S3. The major advantage of Cloudflare R2 is zero bandwidth/egress fees—meaning you    
      won't get charged when people watch your stored videos.                                                               
  4. Backend Server: Render or Railway (~$5/month or Free)                                                                  
      • A hosting service where you run a Python (Flask/FastAPI) or Node.js backend. This backend acts as a bridge: it      
      receives video clips and data from the Raspberry Pi and saves them to your database and storage.                      
                                                                                                                            
  ──────                                                                                                                    
  ### How the Data Flows (Pi ➡️ Cloud ➡️ Website)                                                                           

  ```mermaid
  graph TD
      subgraph Edge ["Raspberry Pi"]
          Camera[Webcam] --> Inference["YOLO Detection"]
          LocalStorage[("Local SSD/SD")]
          Inference -->|Save clip locally| LocalStorage
      end

      subgraph CloudServices ["Cloud Infrastructure"]
          CloudStorage["Cloudflare R2 Storage"]
          CloudBackend["Render/Railway API"]
          DB[("Supabase DB")]
          CloudBackend -->|Save metadata| DB
      end

      subgraph User ["Web Browser"]
          Website["Vercel Frontend"]
      end

      %% Cross-subgraph connections
      Inference -->|Upload video file| CloudStorage
      Inference -->|HTTP POST JSON data| CloudBackend
      Website -->|Fetch charts & logs| DB
      Website -->|Request video playback| CloudStorage
  ```


  #### 1. On the Raspberry Pi:                                                                                              
                                                                                                                            
  • Instead of streaming raw video 24/7 (which uses massive bandwidth), your Pi runs detection locally.                     
  • When it detects an event (e.g., a tomato turning ripe, or a pest detected), it:                                         
      1. Records a 10-second MP4 clip.                                                                                      
      2. Uploads the MP4 clip directly to Cloudflare R2 via an API call.                                                    
      3. Sends a JSON payload to your Backend API containing the event data (timestamp, class name, confidence, and the link
      to the uploaded video).                                                                                               
                                                                                                                            
                                                                                                                            
  #### 2. In the Cloud:                                                                                                     
                                                                                                                            
  • Your backend receives the JSON payload and saves the text data into the Supabase Database.                              
                                                                                                                            
  #### 3. On the Website:                                                                                                   
                                                                                                                            
  • When a user visits your website, the frontend queries Supabase to show historical charts (e.g., "Tomato growth over the 
  last 30 days") and a list of past video clips.                                                                            
  • If the user clicks "Play" on a video, the video streams directly from Cloudflare R2.                                    
  ──────                                                                                                                    
  ### If you did want to use AWS:                                                                                           
                                                                                                                            
  If you want to learn AWS for resume-building or enterprise scaling, the setup would look like this:                       
                                                                                                                            
  • Storage: Amazon S3 (to store video clips).                                                                              
  • Database: Amazon RDS PostgreSQL or DynamoDB (to store insights/metadata).                                               
  • Backend Server: Amazon EC2 (a virtual server) or AWS App Runner to host your backend code.                              
  • Authentication: Amazon Cognito (for user logins).                                                                       
  ──────                                                                                                                    
  ### How to get started step-by-step:                                                                                      
                                                                                                                            
  1. Keep it local first: Modify your current Pi script to save a short video clip locally on the Pi whenever YOLO detects a
  tomato.                                                                                                                   
  2. Set up Supabase: Create a free account on Supabase https://supabase.com and create a table called  detections          
  (columns:  id ,  timestamp ,  label ,  confidence ,  video_url ).                                                         
  3. Connect Pi to Supabase: Write a quick Python script on the Pi using the  supabase-py  library to insert a row into your
  table every time a tomato is detected.                                                                                    
  4. Build the Frontend: Create a simple website hosted on Vercel that reads from that Supabase table and displays the data 
  on a dashboard.  