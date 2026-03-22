import os
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import pdfplumber
import anthropic
  
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def analyze_insurance_with_ai(pdf_text):
    """Send insurance text to Claude for analysis."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""You are an expert car insurance analyst. A user has uploaded their car insurance policy or renewal document. 
Analyze the following text and return a JSON response with this exact structure:

{{
  "summary": "2-3 sentence plain English summary of what this policy covers",
  "monthly_cost": "extracted monthly or annual premium (string, e.g. '$1,200/year')",
  "coverage_items": [
    {{
      "name": "Coverage name",
      "amount": "Coverage amount or limit",
      "assessment": "good|average|overpriced",
      "explanation": "1-2 sentence plain English explanation of this coverage and if the price seems fair"
    }}
  ],
  "red_flags": [
    "List of specific things the user might be overpaying for or missing"
  ],
  "savings_tips": [
    "Specific actionable tips to reduce their premium"
  ],
  "overall_rating": "good|average|overpriced",
  "overall_explanation": "2-3 sentences on whether this policy seems like good value overall"
}}

Be specific and helpful. If you can't find certain information, make reasonable notes. 
Return ONLY valid JSON, no markdown, no extra text.

Insurance document text:
{pdf_text[:6000]}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()
    
    # Strip markdown code fences if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    
    return json.loads(response_text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(filepath)
        
        if not pdf_text or len(pdf_text) < 50:
            return jsonify({'error': 'Could not extract text from PDF. Make sure it is not a scanned image.'}), 400
        
        # Analyze with AI
        analysis = analyze_insurance_with_ai(pdf_text)
        
        return jsonify({'success': True, 'analysis': analysis})
    
    except json.JSONDecodeError:
        return jsonify({'error': 'AI response could not be parsed. Try again.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5000)
