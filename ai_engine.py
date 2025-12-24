import os
import json
from dotenv import load_dotenv
from google import genai
from mcp_context import PROJECT_MCP

load_dotenv(dotenv_path=".env")


def safe_json_load(text):
    """
    Self-healing JSON loader.
    Ensures valid JSON array.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        text = text.strip()
        start = text.find("[")
        end = text.rfind("]") + 1
        return json.loads(text[start:end])


def enforce_schema(data, allowed_fields):
    """
    Ensures:
    - Only allowed fields exist
    - Missing fields are set to null
    """
    clean_data = []

    for item in data:
        cleaned_item = {}
        for field in allowed_fields:
            cleaned_item[field] = item.get(field, None)
        clean_data.append(cleaned_item)

    return clean_data


def gemini_extract(raw_text, user_fields):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
{PROJECT_MCP}

TASK:
Extract ONLY the following fields:
{', '.join(user_fields)}

IMPORTANT:
- Add confidence_score
- Do NOT add any other fields

WEBSITE CONTENT:
{raw_text[:4000]}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    data = safe_json_load(response.text)

    allowed_fields = user_fields + ["confidence_score"]
    return enforce_schema(data, allowed_fields)
