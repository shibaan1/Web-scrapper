import re
from db import (
    sign_up, sign_in, save_scrape, save_result,
    get_user_history, get_scrape_results,
    change_password as db_change_password,
    update_profile as db_update_profile,
    get_user_stats, get_all_scraped_content
)
from scrape import (
    scrape_website, extract_body_content,
    clean_body_content, split_dom_content
)
from parse import parse_with_groq
from chatbot import chat_with_data


class ViewModel:

    # ---------- AUTH ---------- #

    def login(self, email, password):
        if not email or not password:
            return False, "Please fill in both fields"

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Invalid email format"

        success, result = sign_in(email, password)

        if success:
            return True, result

        if result == "email_not_found":
            return False, "Email not registered"
        elif result == "wrong_password":
            return False, "Incorrect password"

        return False, result


    def register(self, name, email, password, confirm_password):
        if not name or not email or not password or not confirm_password:
            return False, "Please fill in all fields"

        if password != confirm_password:
            return False, "Passwords do not match"

        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Invalid email format"

        return sign_up(name, email, password)


    # ---------- SCRAPING ---------- #

    def scrape_site(self, user_id, url):
        if not url.strip():
            return False, "Please enter a URL"

        if not url.startswith("http"):
            return False, "URL must start with http:// or https://"

        try:
            raw_html = scrape_website(url)
            body = extract_body_content(raw_html)
            cleaned = clean_body_content(body)

            scrape_id = save_scrape(user_id, url)
            if not scrape_id:
                return False, "Failed to save scrape to database."

            return True, {
                "scrape_id": scrape_id,
                "url": url,
                "content": cleaned
            }

        except Exception as e:
            return False, str(e)


    def extract_data(self, scrape_id, dom_content, prompt):
        if not prompt.strip():
            return False, "Please describe what to extract"

        chunks = split_dom_content(dom_content)
        result = parse_with_groq(chunks, prompt)

        save_result(scrape_id, prompt, result)

        return True, result


    # ---------- CHAT ---------- #

    def chat(self, question, data, history):
        if not question.strip():
            return False, "Question cannot be empty"

        try:
            answer = chat_with_data(question, data, history)
            return True, answer
        except Exception as e:
            return False, str(e)


    # ---------- HISTORY ---------- #

    def get_history(self, user_id):
        return get_user_history(user_id)

    def get_results(self, scrape_id):
        return get_scrape_results(scrape_id)


    # ---------- PROFILE ---------- #

    def update_profile(self, user_id, full_name, bio):
        return db_update_profile(user_id, full_name, bio)

    def change_password(self, user_id, old_password, new_password, confirm_password):
        if not old_password or not new_password or not confirm_password:
            return False, "Please fill in all fields"

        if new_password != confirm_password:
            return False, "Passwords do not match"

        if len(new_password) < 6:
            return False, "Password must be at least 6 characters"

        return db_change_password(user_id, old_password, new_password)

    def get_stats(self, user_id):
        return get_user_stats(user_id)

    def get_all_content(self, user_id):
        return get_all_scraped_content(user_id)
