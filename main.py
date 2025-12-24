from browser import load_website
from extractor import extract_raw_content
from ai_engine import gemini_extract
from exporter import save_output

def main():
    url = input("Enter Website URL: ")
    fields = input("Enter required fields (comma separated): ")
    output_type = input("Output format (excel/json): ").lower()

    user_fields = [f.strip() for f in fields.split(",")]

    print("🔹 Loading website...")
    html = load_website(url)

    print("🔹 Extracting raw content...")
    raw_text = extract_raw_content(html)

    print("🔹 Gemini AI understanding & extraction...")
    ai_output = gemini_extract(raw_text, user_fields)

    print("🔹 Saving output...")
    file_name = save_output(ai_output, output_type)

    print("✅ Completed Successfully")
    print(f"📁 Output File: {file_name}")

if __name__ == "__main__":
    main()
