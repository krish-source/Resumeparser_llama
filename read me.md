Resume Parser AI Agent 🚀🤖
Welcome to the Resume Parser AI Agent!
A quirky project that uses Ollama and LLMs to extract structured information from resumes 🎉📄

What It Does ✨
This project takes in PDF resumes, extracts text using PyPDF2, and then sends that text to an LLM (via Ollama) to generate a structured JSON output containing:

Name 😎
Email 📧
Phone Number 📞
Education 🎓
Work Experience 💼
Skills 💪
It’s like magic, but with code! ✨🪄

Features 🌟
PDF Text Extraction: Fast and efficient extraction using PyPDF2.
LLM Integration: Uses Ollama for natural language processing and extraction.
Custom JSON Schema: Generates a consistent JSON structure for each resume.
Quirky & Fun: Because coding should be as fun as it is functional! 😄
Requirements ✅
Python 3.7+
PyPDF2
Ollama (Ensure your Ollama server is up and running using ollama serve)
A modern processor – we've tested on Intel® Core™ i5 (11th Gen) with 8GB RAM, though more power means more speed! ⚡
Installation 🔧
Clone the repository:

bash
Copy
git clone https://github.com/yourusername/resume-parser-ai-agent.git
cd resume-parser-ai-agent
Install dependencies:

bash
Copy
pip install -r requirements.txt
Download the required model:

Make sure you have the correct model downloaded:

bash
Copy
ollama pull llama3.2:3b
Tip: For faster processing, consider switching to llama3.2:1b!

Usage 🚀
Start the Ollama Server:

In a separate terminal, run:

bash
Copy
ollama serve
Tip: Close it anytime with CTRL+C if needed.

Run the Resume Parser:

bash
Copy
python resumeparser_aiagent.py
Watch the magic happen!
Extracted resumes will be printed out in your terminal as a structured JSON output. JSON never looked this fun! 🎉

Contributing 💡
Contributions are welcome! Whether you’re a code wizard 🧙‍♂️ or just love quirky projects, feel free to open an issue or submit a pull request. Let’s build something awesome together! 🤝✨

License 📄
This project is licensed under the MIT License.

Got Questions? 🤔
Feel free to open an issue or contact me directly. Let's chat code and coffee! ☕💬

Happy parsing and keep on coding! 😄👩‍💻👨‍💻
