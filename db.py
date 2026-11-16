import os
from dotenv import load_dotenv
from supabase import create_client
import hashlib

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def sign_up(name, email, password):
    try:
        existing = supabase.table("users").select("*").eq("email", email).execute()
        if existing.data:
            return False, "Email already registered"
        
        supabase.table("users").insert({
            "full_name": name,
            "email": email,
            "password": hash_password(password)
        }).execute()
        return True, "Account created successfully"
    
    except Exception as e:
        return False, str(e)


def sign_in(email, password):
    try:
        # First check if email exists
        user_check = supabase.table("users").select("*").eq("email", email).execute()
        
        if not user_check.data:
            return False, "email_not_found"
        
        # Email exists, now check password
        result = supabase.table("users").select("*").eq("email", email).eq("password", hash_password(password)).execute()
        
        if result.data:
            return True, result.data[0]
        else:
            return False, "wrong_password"
    
    except Exception as e:
        return False, str(e)


def save_scrape(user_id, url):
    try:
        result = supabase.table("scrapes").insert({
            "user_id": user_id,
            "url": url
        }).execute()
        return result.data[0]["id"]
    
    except Exception as e:
        print(f"Error saving scrape: {e}")
        return None


def save_result(scrape_id, prompt, extracted_text):
    try:
        supabase.table("results").insert({
            "scrape_id": scrape_id,
            "prompt": prompt,
            "extracted_text": extracted_text
        }).execute()
    
    except Exception as e:
        print(f"Error saving result: {e}")


def get_user_history(user_id):
    try:
        scrapes = supabase.table("scrapes").select("*").eq("user_id", user_id).order("scraped_at", desc=True).execute()
        return scrapes.data
    
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []


def get_scrape_results(scrape_id):
    try:
        results = supabase.table("results").select("*").eq("scrape_id", scrape_id).execute()
        return results.data
    
    except Exception as e:
        print(f"Error fetching results: {e}")
        return []

def change_password(user_id, old_password, new_password):
    try:
        result = supabase.table("users").select("*").eq("id", user_id).eq("password", hash_password(old_password)).execute()
        if not result.data:
            return False, "Current password is incorrect"
        
        supabase.table("users").update({
            "password": hash_password(new_password)
        }).eq("id", user_id).execute()
        
        return True, "Password changed successfully"
    
    except Exception as e:
        return False, str(e)


def update_profile(user_id, full_name, bio):
    try:
        supabase.table("users").update({
            "full_name": full_name,
            "bio": bio
        }).eq("id", user_id).execute()
        return True, "Profile updated successfully"
    
    except Exception as e:
        return False, str(e)


def get_user_stats(user_id):
    try:
        scrapes = supabase.table("scrapes").select("*").eq("user_id", user_id).execute()
        total_scrapes = len(scrapes.data)

        total_results = 0
        for scrape in scrapes.data:
            results = supabase.table("results").select("*").eq("scrape_id", scrape["id"]).execute()
            total_results += len(results.data)

        return {
            "total_scrapes": total_scrapes,
            "total_results": total_results
        }
    
    except Exception as e:
        return {"total_scrapes": 0, "total_results": 0}        

def get_all_scraped_content(user_id):
    try:
        scraped_data = []
        scrapes = supabase.table("scrapes").select("*").eq("user_id", user_id).execute()
        
        for scrape in scrapes.data:
            results = supabase.table("results").select("*").eq("scrape_id", scrape["id"]).execute()
            for r in results.data:
                scraped_data.append({
                    "url": scrape["url"],
                    "content": r["extracted_text"]
                })
        
        return scraped_data
    
    except Exception as e:
        print(f"Error fetching scraped content: {e}")
        return []        