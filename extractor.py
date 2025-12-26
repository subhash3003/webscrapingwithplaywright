from bs4 import BeautifulSoup

def extract_raw_content(html, max_length=10000):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    raw_text = "\n".join(lines)
    # Limit text length for performance
    return raw_text[:max_length]
