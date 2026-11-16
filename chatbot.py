import os
from dotenv import load_dotenv
from groq import Groq, RateLimitError

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat_with_data(question, scraped_data, chat_history=[]):

    context_parts = []
    total_chars = 0
    max_chars = 6000

    for item in scraped_data:
        content = item["content"]
        if total_chars + len(content) > max_chars:
            remaining = max_chars - total_chars
            if remaining > 200:
                context_parts.append(f"Source: {item['url']}\nContent: {content[:remaining]}")
            break
        context_parts.append(f"Source: {item['url']}\nContent: {content}")
        total_chars += len(content)

    context = "\n\n".join(context_parts)

    history_text = ""
    if chat_history:
        last_6 = chat_history[-6:]
        history_text = "\n".join([
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in last_6
        ])

    prompt = f"""You are a helpful assistant that answers questions based only on the scraped website data provided below.

Here is the scraped data:
-----------------------
{context}
-----------------------

{"Previous conversation:" if history_text else ""}
{history_text}

Current question: {question}

Rules:
- Answer ONLY using the data provided above.
- Use the previous conversation to understand follow up questions.
- If someone asks "what about X" or "and X" use the previous context to understand what they mean.
- If the answer is not in the data say "I could not find that in your scraped data."
- Be clear and concise.
- If listing items use a numbered list.
- Never make up information that is not in the scraped data.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    
    except RateLimitError as e:
        error_msg = str(e)
        if "17m" in error_msg or "18m" in error_msg:
            return "⏳ Daily AI limit reached. The system resets in about 18 minutes. Please try again then, or come back tomorrow for a fresh 100,000 tokens."
        elif "tokens per day" in error_msg:
            return "⏳ Daily AI limit reached. The free tier gives 100,000 tokens per day and resets every 24 hours. Please try again later."
        else:
            return "⏳ Rate limit reached. Please wait a few moments and try again."
    
    except Exception as e:
        return f"❌ An error occurred: {str(e)}"