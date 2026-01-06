import os
from supabase import create_client, Client
import uuid
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
bucket_name = "uploads"

def upload_file_to_cloud(file):
    file_id = str(uuid.uuid4())
    file_name = file.filename
    name, extension= os.path.splitext(file_name)
    file_path = f"{bucket_name}/{file_id}{extension}"
    