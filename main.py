import PyPDF2
from ollama import Client
import json
import re
import os

# Create a global client instance and verify connection/model availability
try:
    client = Client()  # Optionally, specify base_url if needed (e.g., Client(base_url="http://localhost:11434"))
    models = client.list()
    # Debug: Print the available models to inspect their structure and identifiers
    print("Available models:", models)
    
    # Set the expected model identifier; update this if the printed identifiers differ
    expected_model = 'llama3.2:3b'
    # Extract the model identifier using the attribute 'model' from each Model object
    available_ids = [m.model for m in models.get('models', [])]
    
    if expected_model not in available_ids:
        print(f"Model '{expected_model}' is not available. Available model ids: {available_ids}")
        print("If the model is already downloaded, please check the correct identifier and update the 'expected_model' variable accordingly.")
        exit(1)
except Exception as e:
    print(f"Error connecting to Ollama server: {e}. Ensure the server is running with 'ollama serve'.")
    exit(1)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a text-based PDF using PyPDF2."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            if not text.strip():
                print("No text found. The PDF may not be text-based.")
                return None
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def preprocess_text(text):
    """Cleans and standardizes text for LLM processing."""
    if not text:
        return ""
    # Normalize whitespace and remove special characters (except @, ., -)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s@.-]', '', text)
    return text.strip()

def extract_information(text, model_name='llama3.2:3b'):
    """Uses Llama 3.2 3B to extract structured info from text using a strict JSON schema."""
    if not text:
        return None
    # Truncate text to avoid exceeding token limits (e.g., 2048 tokens)
    max_words = 1000
    words = text.split()
    if len(words) > max_words:
        text = ' '.join(words[:max_words])
    prompt = (
        "Extract the following information from the resume and format it as a JSON object following this exact schema:\n\n"
        "{\n"
        '  "name": string or null,\n'
        '  "email": string or null,\n'
        '  "phone": string or null,\n'
        '  "education": [\n'
        "    {\n"
        '      "degree": string or null,\n'
        '      "institution": string or null,\n'
        '      "startYear": number or null,\n'
        '      "endYear": number or null\n'
        "    }\n"
        "  ],\n"
        '  "workExperience": [\n'
        "    {\n"
        '      "title": string or null,\n'
        '      "company": string or null,\n'
        '      "location": string or null,\n'
        '      "startDate": string or null,\n'
        '      "endDate": string or null,\n'
        '      "description": string or null\n'
        "    }\n"
        "  ],\n"
        '  "skills": [string]\n'
        "}\n\n"
        "Resume text: " + text
    )
    try:
        response = client.generate(model_name, prompt)
        return response.get('response')
    except KeyError:
        print(f"Key 'response' not found in LLM response: {response}")
        return None
    except Exception as e:
        print(f"Error with LLM: {e}")
        return None

def parse_output(output):
    """Parses the LLM’s output into a Python dictionary."""
    if not output:
        return {}
    try:
        # Try to extract JSON from a markdown code block (```...```)
        pattern = r"```(?:json)?\s*(\{.*\})\s*```"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            # Fallback: extract substring from first "{" to last "}"
            start = output.find('{')
            end = output.rfind('}')
            if start != -1 and end != -1:
                json_str = output[start:end+1]
            else:
                json_str = output
        return json.loads(json_str)
    except Exception as e:
        print("Couldn't parse output as JSON. Raw output:", output)
        print("Error:", e)
        return {}

def process_resume(pdf_path):
    """Processes a text-based PDF resume and returns structured data."""
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("File must be a PDF.")
    
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        print("Text extraction failed.")
        return None
    preprocessed_text = preprocess_text(text)
    
    raw_output = extract_information(preprocessed_text)
    if raw_output is None:
        print("Information extraction failed.")
        return None

    structured_data = parse_output(raw_output)
    return structured_data

def process_resumes_in_folder(folder_path):
    """Processes all PDF resumes found in the specified folder."""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {pdf_path}...")
            data = process_resume(pdf_path)
            if data:
                print("Extracted Information:")
                print(json.dumps(data, indent=2))
            else:
                print("No data extracted.")

if __name__ == "__main__":
    folder_path = r'C:\Users\KrishnaSivakumar\Documents\ResumeparserAI\resume data'
    try:
        process_resumes_in_folder(folder_path)
    except Exception as e:
        print(f"Error: {e}")
