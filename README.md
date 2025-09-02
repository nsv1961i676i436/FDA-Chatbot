# FDA Drug Chatbot- AI Healthcare Project Documentation

## Project Overview
This project implements an AI-powered healthcare application that processes medical documents and provides an interactive interface for querying drug-related information.

## Project Structure 

### Root Directory
```
AIHC/
├── app/                   # Core application code
├── clients/               # Client applications
├── Datasets/              # Data storage
├── tools/                 # Analysis tools
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

### Core Application (`app/`)
```
app/
├── services/             # Business logic services
│   └── similarity.py     # Similarity computation service
├── utils/               # Utility functions
│   └── file.py         # File handling utilities
├── __init__.py         # Package initialization
├── main.py             # Application entry point
├── models.py           # Data models
└── help.md            # Usage documentation
```

### Client Applications (`clients/`)
```
clients/
└── pdf_chatbot_Submission.py    # Streamlit web interface for PDF chat
```

### Data Directory (`Datasets/`)
```
Datasets/
├── Datasets1/          # First dataset collection (Drug information PDFs)
│   ├── AFINITOR.pdf
│   ├── ARIMIDEX.pdf
│   └── ...
└── Datasets2/         # Second dataset collection (Drug information PDFs)
    ├── ENHERTU.pdf
    ├── FARESTON.pdf
    └── ...
```

### Tools (`tools/`)
```
tools/
└── SemantiScore-Final.py    # Semantic similarity analysis tool
```

## Features
- PDF document processing and text extraction
- Interactive chat interface using Azure OpenAI
- Semantic similarity analysis
- Drug information retrieval system
- Multi-document support

## Development Setup

### Prerequisites
- Python 3.12+
- Azure OpenAI API access
- VS Code (recommended)

### Installation
1. Clone the repository
2. Create a Python virtual environment:
```bash
python -m venv .
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Required Packages
- streamlit
- pymupdf
- openai
- spacy
- sentence-transformers
- pandas
- en-core-sci-sm (spaCy model)

## Usage

### PDF Chatbot
1. Navigate to the project directory:
```bash
cd AIHC
```

2. Run the Streamlit application:
```bash
streamlit run clients/pdf_chatbot_Submission.py
```

3. Upload PDF documents and start asking questions about the drug information.

### Semantic Analysis
The `SemantiScore-Final.py` tool can be used to analyze semantic similarity between different text segments:

```python
python tools/SemantiScore-Final.py
```

## Data Files
- `gptGeneratedAnswers.csv` - Contains GPT model responses
- `semantic_similarity_results.csv` - Results of semantic similarity analysis

## Configuration
- Azure OpenAI credentials need to be configured in the client applications
- Environment variables for API keys and endpoints
- Streamlit configuration for web interface

## Documentation
- Refer to `app/help.md` for detailed usage instructions
- Individual component documentation in respective directories
- API documentation in service modules

## Future Improvements
- Enhanced error handling
- Additional drug information sources
- Improved semantic analysis
- Extended API functionality
- Better documentation coverage
