import os
import time
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIError

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def parse_with_groq(dom_chunks, parse_description, retries=3, delay=10):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = f"""You are an information extraction system.

Extract ONLY the information that matches this request:
{parse_description}

From the following website content:

-----------------------
{chunk}
-----------------------

Rules:
- Return ONLY the extracted text.
- Do NOT repeat the instructions.
- Do NOT explain anything.
- If nothing matches, return an empty string."""

        for attempt in range(1, retries + 1):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=1024,
                )
                result = response.choices[0].message.content.strip()
                print(f"Parsed chunk {i}/{len(dom_chunks)}")
                parsed_results.append(result)
                break

            except RateLimitError as e:
                error_msg = str(e)
                if "tokens per day" in error_msg:
                    parsed_results.append("\n⏳ Daily AI limit reached. Extraction stopped. The free tier resets every 24 hours with 100,000 fresh tokens. Please try again later.")
                    return "\n".join(parsed_results)
                elif attempt < retries:
                    print(f"Rate limit hit. Waiting {delay}s before retry {attempt}/{retries}...")
                    time.sleep(delay)
                else:
                    parsed_results.append("[Rate limit reached — chunk skipped]")

            except APIError as e:
                print(f"API error on chunk {i}: {e}")
                parsed_results.append(f"[API error: {e}]")
                break

            except Exception as e:
                print(f"Unexpected error on chunk {i}: {e}")
                parsed_results.append(f"[Unexpected error: {e}]")
                break

    filtered = [r for r in parsed_results if r and not r.startswith("[")]
    return "\n".join(filtered) if filtered else "Nothing matching your request was found."