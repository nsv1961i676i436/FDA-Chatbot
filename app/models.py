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