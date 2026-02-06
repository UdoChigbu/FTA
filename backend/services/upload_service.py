import os
from supabase import create_client, Client
import uuid
from dotenv import load_dotenv
from backend.services.csv_service import csv_identify_merchants_costs

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
bucket_name = "csv_file_uploads"

def upload_file_to_cloud(file):
    
    file_id = str(uuid.uuid4())
    file_name = file.filename
    name, extension= os.path.splitext(file_name)
    file_path = f"{name}_{file_id}{extension}"
    file_data=file.read()
    supabase.storage.from_(bucket_name).upload(file_path, file_data)
    csv_identify_merchants_costs(file_data)
   