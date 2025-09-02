# SemantiScore Microservice Project Setup Guide

## Project Overview
SemantiScore is a microservice that provides semantic similarity comparison between texts using sentence transformers. This guide will walk you through setting up and implementing the project from scratch.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Environment Setup](#environment-setup)
3. [Implementation Steps](#implementation-steps)
4. [Running the Service](#running-the-service)
5. [API Usage](#api-usage)

## Project Structure
First, create the following directory structure:
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── models.py         # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── similarity.py # Similarity computation logic
│   └── utils/
│       ├── __init__.py
│       └── file.py       # File handling utilities
├── requirements.txt
└── README.md
```

## Environment Setup

1. Create a new virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Create and populate requirements.txt:
```txt
fastapi==0.104.1
uvicorn==0.24.0
sentence-transformers==2.2.2
pandas==2.1.3
python-multipart==0.0.6
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Implementation Steps

### 1. Create Pydantic Models (app/models.py)
```python
from pydantic import BaseModel
from typing import List

class TextComparisonInput(BaseModel):
    text1: str
    text2: str

class BatchComparisonInput(BaseModel):
    ground_truth: List[str]
    generated_answers: List[str]

class SimilarityScore(BaseModel):
    score: float

class BatchSimilarityScore(BaseModel):
    scores: List[float]
```

### 2. Implement Similarity Service (app/services/similarity.py)
```python
from sentence_transformers import SentenceTransformer, util
import pandas as pd

class SimilarityService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        return float(util.cos_sim(emb1, emb2))
    
    def compute_batch_similarity(self, ground_truth: list, generated: list) -> list:
        scores = []
        for gt, gen in zip(ground_truth, generated):
            score = self.compute_similarity(str(gt), str(gen))
            scores.append(score)
        return scores
    
    def process_csv(self, input_file, output_file, 
                   col_ground_truth='GroundTruth', 
                   col_generated='GeneratedAnswer'):
        df = pd.read_csv(input_file)
        scores = self.compute_batch_similarity(
            df[col_ground_truth].tolist(),
            df[col_generated].tolist()
        )
        df['SemanticSimilarity'] = scores
        df.to_csv(output_file, index=False)
        return df
```

### 3. Create FastAPI Application (app/main.py)
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os
from .models import TextComparisonInput, BatchComparisonInput, SimilarityScore, BatchSimilarityScore
from .services.similarity import SimilarityService

app = FastAPI(title="SemanticScore API")
similarity_service = SimilarityService()

@app.post("/compare", response_model=SimilarityScore)
async def compare_texts(input_data: TextComparisonInput):
    """Compare two texts and return similarity score"""
    score = similarity_service.compute_similarity(input_data.text1, input_data.text2)
    return SimilarityScore(score=score)

@app.post("/compare/batch", response_model=BatchSimilarityScore)
async def compare_batch(input_data: BatchComparisonInput):
    """Compare batches of texts and return similarity scores"""
    scores = similarity_service.compute_batch_similarity(
        input_data.ground_truth,
        input_data.generated_answers
    )
    return BatchSimilarityScore(scores=scores)

@app.post("/compare/csv")
async def compare_csv(file: UploadFile = File(...)):
    """Process CSV file and return results"""
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    
    try:
        content = await file.read()
        with open(temp_input.name, 'wb') as f:
            f.write(content)
        
        similarity_service.process_csv(temp_input.name, temp_output.name)
        
        return FileResponse(
            temp_output.name,
            media_type='text/csv',
            filename='semantic_similarity_results.csv'
        )
    finally:
        os.unlink(temp_input.name)
        os.unlink(temp_output.name)
```

## Running the Service

1. Make sure you're in the project root directory
2. Activate your virtual environment
3. Run the service:
```bash
uvicorn app.main:app --reload
```

The service will start on `http://localhost:8000`

## API Usage

### 1. Compare Two Texts
```bash
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{"text1": "Hello world", "text2": "Hi world"}'
```

### 2. Batch Compare Texts
```bash
curl -X POST "http://localhost:8000/compare/batch" \
     -H "Content-Type: application/json" \
     -d '{
           "ground_truth": ["Hello world", "Test text"],
           "generated_answers": ["Hi world", "Testing text"]
         }'
```

### 3. Process CSV File
```bash
curl -X POST "http://localhost:8000/compare/csv" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/input.csv"
```

## API Documentation
Once the service is running, you can access:
- Interactive API documentation at `http://localhost:8000/docs`
- Alternative API documentation at `http://localhost:8000/redoc`

## Next Steps
1. Add error handling and logging
2. Implement authentication
3. Add Docker support
4. Set up monitoring
5. Implement caching for better performance
6. Add test suite

This microservice architecture provides a scalable and maintainable solution for semantic similarity comparison, with clear separation of concerns and well-defined APIs.
