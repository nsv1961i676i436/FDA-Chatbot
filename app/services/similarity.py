from sentence_transformers import SentenceTransformer, util
import pandas as pd

class SimilarityService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        # Load once at startup; reused for all requests
        self.model = SentenceTransformer(model_name)

    def compute_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        return float(util.cos_sim(emb1, emb2))  # 1x1 tensor -> float

    def compute_batch_similarity(self, ground_truth: list, generated: list) -> list:
        # Assumes same length; enforce in API layer
        scores = []
        for gt, gen in zip(ground_truth, generated):
            score = self.compute_similarity(str(gt), str(gen))
            scores.append(score)
        return scores

    def process_csv(
        self,
        input_file: str,
        output_file: str,
        col_ground_truth: str = "GroundTruth",
        col_generated: str = "GeneratedAnswer",
    ):
        df = pd.read_csv(input_file)
        scores = self.compute_batch_similarity(
            df[col_ground_truth].astype(str).tolist(),
            df[col_generated].astype(str).tolist(),
        )
        df["SemanticSimilarity"] = scores
        df.to_csv(output_file, index=False)
        return df
