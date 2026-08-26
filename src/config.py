import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
    DEVICE_TYPE = os.getenv("DEVICE_TYPE", "pi")
    CAMERA_COUNT = int(os.getenv("CAMERA_COUNT", "1"))

    # Sentry Configuration
    SENTRY_DSN = os.getenv("SENTRY_DSN")

    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

    # Cloudflare R2 / S3 Configuration
    CLOUDFLARE_R2_ENDPOINT = os.getenv("CLOUDFLARE_R2_ENDPOINT")
    CLOUDFLARE_R2_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
    CLOUDFLARE_R2_SECRET_ACCESS_KEY = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
    CLOUDFLARE_BUCKET_NAME = os.getenv("CLOUDFLARE_BUCKET_NAME")

    # Device & Logger Configuration
    DEVICE_ID = int(os.getenv("DEVICE_ID", "1"))
    LOG_INTERVAL = 30  # seconds
    LOG_DATABASE = os.getenv("LOG_DATABASE", "False").lower() in ("true", "1", "t")

    # Model Configuration
    MODEL_PATH = "./CVResults/content/runs/detect/train/weights/last_ncnn_model"
    FALLBACK_MODEL_PATH = "./CVResults/content/runs/detect/train/weights/last.pt"
