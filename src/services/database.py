from supabase import create_client, Client
from src.config import Config

_supabase_client = None

def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY must be set.")
        
        _supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    
    return _supabase_client

def log_detection(image_url, total=0, ripe=0, unripe=0, image_key=None, early_blight=0, healthy=0, late_blight=0, leaf_miner=0, leaf_mold=0, mosaic_virus=0, septoria=0, spider_mites=0, yellow_leaf_curl_virus=0):                                          
    try:                                                                                              
        # Optional: Get Pi CPU temperature                                                            
        cpu_temp = None

        try:                                                                                          
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:                             
                cpu_temp = round(int(f.read()) / 1000.0, 1)                                           
        except Exception:                                                                             
            pass  # Fallback if not running on Pi                                                     
                                                                                                        
        data = {                                                                                      
            "device_id": Config.DEVICE_ID,                                                                   
            "image_url": image_url,                                                                   
            "total_count": total,                                                                     
            "ripe_count": ripe,                                                                       
            "unripe_count": unripe,                                                               
            "cpu_temp": cpu_temp,
            "image_key": image_key,
            "early_blight": early_blight,
            "healthy": healthy,
            "late_blight": late_blight,
            "leaf_miner": leaf_miner,
            "leaf_mold": leaf_mold,
            "mosaic_virus": mosaic_virus,
            "septoria": septoria,
            "spider_mites": spider_mites,
            "yellow_leaf_curl_virus": yellow_leaf_curl_virus
        }                                                                                             
                                                                                                        
        # Insert row into Supabase
        client = get_supabase_client()                                                                   
        response = client.table("tomato_detections").insert(data).execute()                         
        print(f"[DB] Logged detection to Supabase: {total} tomatoe leaves found.")                          
        return response.data                                                                          
    except Exception as e:                                                                            
        print(f"[DB] Error logging to Supabase: {e}")                                                 
        return None