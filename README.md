# AI Web Scraper & Chatbot

A Streamlit web application that scrapes website content using Selenium and BeautifulSoup, stores data in Supabase, and uses the Groq API to parse and chat with the extracted data.

## Prerequisites

- **Python 3.9+** installed on your machine
- **Google Chrome** browser installed (required for Selenium headless scraping)
- **Groq API Key** and **Supabase Project URL & Key**

## Required Libraries

All dependencies are listed in `requirements.txt`:

- `streamlit` – Frontend web UI
- `selenium` – Headless Chrome browser automation for scraping
- `beautifulsoup4`, `lxml`, `html5lib` – HTML parsing and DOM cleaning
- `groq` – LLM integration for parsing and chatting with scraped content
- `supabase` – Database client for storing and retrieving scraped data
- `python-dotenv` – Environment variable management

## Installation & Setup Process

### 1. Clone the Repository
```bash
git clone [https://github.com/shibaan1/Web-scrapper.git](https://github.com/shibaan1/Web-scrapper.git)
cd Web-scrapper
