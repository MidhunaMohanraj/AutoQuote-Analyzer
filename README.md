# 🚗 AutoQuote Analyzer

> Upload your car insurance PDF. Get an AI-powered breakdown of every charge — and find out if you're overpaying.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![Claude AI](https://img.shields.io/badge/Claude-AI-orange) ![License](https://img.shields.io/badge/license-MIT-purple)

## What it does

Car insurance documents are deliberately confusing. AutoQuote Analyzer fixes that.

1. **Upload** your renewal or policy PDF
2. **AI extracts** every coverage item, limit, and premium
3. **Get a plain-English breakdown** of what you're paying for — and whether it's fair
4. **See red flags** and specific tips to lower your bill

## Demo

![AutoQuote Analyzer Screenshot](https://via.placeholder.com/800x450/0a0a0a/e8ff47?text=AutoQuote+Analyzer)

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python, Flask |
| PDF Parsing | pdfplumber |
| AI Analysis | Anthropic Claude (claude-sonnet) |
| Frontend | Vanilla HTML/CSS/JS |

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/autoquote-analyzer.git
cd autoquote-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
# Get one free at https://console.anthropic.com
```

Then export it:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 4. Run it

```bash
python app.py
```

Visit `http://localhost:5000`

## How it works

```
PDF Upload → pdfplumber extracts text → Claude analyzes coverage items,
limits, and premiums → Returns structured JSON → Frontend renders
color-coded breakdown with savings tips
```

The Claude prompt is engineered to extract:
- Every coverage line item with amounts
- Assessment of each item (good / average / overpriced)
- Specific red flags
- Actionable savings tips
- Overall policy rating

## Why I built this

I was shopping for car insurance and couldn't understand my renewal. I knew I was probably overpaying but couldn't tell where. I spent a weekend building this so nobody has to stare at confusing insurance jargon again.

## Roadmap

- [ ] Side-by-side comparison of two policies
- [ ] Average market rate benchmarks by ZIP code
- [ ] Email summary export
- [ ] Support for scanned PDFs (OCR)

## License

MIT — do whatever you want with it.
