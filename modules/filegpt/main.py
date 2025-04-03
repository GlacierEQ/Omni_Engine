import os
import sys
import fitz  # PyMuPDF
import docx
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("sk-6l9UvPJaVhx458NbJ-941-0R_jhaZ-fvE41QpsYpTntYPEDpWZ3OFpDOUBPBjJ4PP3ojozC0ZWT3BlbkFJ5fMfO_9Vi4olJslhQmfsuXCKfa7A9AS673aGp3q7-8W3Y0fbBo2RHQmBWzAT1fD4kk3ludLjAA-") 

SUPPORTED_EXTENSIONS = ['txt', 'pdf', 'docx']
DEBUG = "--debug" in sys.argv

def extract_text(file_path):
    ext = file_path.lower().split('.')[-1]
    if ext not in SUPPORTED_EXTENSIONS:
        return None, f"❌ Unsupported file type: .{ext}"

    try:
        if ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), None
        elif ext == 'pdf':
            doc = fitz.open(file_path)
            return "\n".join([page.get_text() for page in doc]), None
        elif ext == 'docx':
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs]), None
    except Exception as e:
        return None, f"❌ Error extracting file: {str(e)}"

def summarize_with_gpt(content):
    try:
        print("🧠 Sending to GPT for summarization...")
        trimmed = content[:3000]  # truncate safely
        response = openai.ChatCompletion.create(
            model="gpt-4",  # fallback handled below
            messages=[{"role": "user", "content": f"Summarize this legal text:\n{trimmed}"}],
            temperature=0.6
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"⚠️ GPT-4 failed, trying GPT-3.5. Reason: {e}")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize this legal text:\n{trimmed}"}],
                temperature=0.6
            )
            return response['choices'][0]['message']['content']
        except Exception as ee:
            return f"❌ GPT failed: {str(ee)}"

if __name__ == "__main__":
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if len(args) < 1:
        print("📎 Usage: python main.py <filename> [--debug]")
        sys.exit()

    file_path = args[0]

    print(f"📄 Summarizing: {file_path}")
    if not os.path.exists(file_path):
        print("❌ File not found.")
        sys.exit()

    content, error = extract_text(file_path)
    if error:
        print(error)
        sys.exit()

    print(f"✅ Extracted {len(content.split())} words.")
    if DEBUG:
        print("🔍 DEBUG: Raw content preview:\n" + content[:500])

    summary = summarize_with_gpt(content)
    print("\n🧠 GPT Summary:\n" + summary)
