import logging
import asyncio
from urllib.parse import urlparse
from browser import load_website
from extractor import extract_raw_content
from ai_engine import gemini_extract
from exporter import save_output

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        url = input("Enter Website URL: ").strip()
        fields = input("Enter required fields (comma separated): ").strip()
        output_type = input("Output format (excel/json): ").lower().strip()

        # Input validation
        if not url:
            raise ValueError("URL cannot be empty.")
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format.")

        if not fields:
            raise ValueError("Fields cannot be empty.")
        user_fields = [f.strip() for f in fields.split(",") if f.strip()]
        if not user_fields:
            raise ValueError("At least one field must be provided.")

        if output_type not in ["excel", "json"]:
            raise ValueError("Output format must be 'excel' or 'json'.")

        logging.info("🔹 Loading website...")
        html = await load_website(url)

        logging.info("🔹 Extracting raw content...")
        raw_text = extract_raw_content(html)

        logging.info("🔹 Gemini AI understanding & extraction...")
        ai_output = gemini_extract(raw_text, user_fields)

        logging.info("🔹 Saving output...")
        file_name = save_output(ai_output, output_type)

        logging.info("✅ Completed Successfully")
        print(f"📁 Output File: {file_name}")

    except ValueError as e:
        logging.error(f"Input validation error: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
