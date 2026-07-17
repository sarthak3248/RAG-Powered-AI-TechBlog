from transformers import pipeline


class ToxicityService:

    _classifier = None

    LABELS = [
        "toxic",
        "severe_toxic",
        "obscene",
        "threat",
        "insult",
        "identity_hate",
    ]
    
    THRESHOLD = 0.60

    @classmethod
    def get_classifier(cls):

        if cls._classifier is None:

            print("Loading Jigsaw Toxicity Model...")

            cls._classifier = pipeline(
                task="text-classification",
                model="martin-ha/toxic-comment-model",
                top_k=None
            )

            print("Model loaded.")

        return cls._classifier

    @classmethod
    def analyze(cls, text):

        classifier = cls.get_classifier()

        predictions = classifier(text)[0]

        scores = {}

        for item in predictions:
            scores[item["label"]] = round(float(item["score"]), 4)
            
        highest_category = max(scores, key=scores.get)
        
        highest_score = scores[highest_category]
        
        approved = highest_score < cls.THRESHOLD
        
        return {
            "approved": approved,
            "overall_score": highest_score,
            "highest_category": highest_category,
            "scores": scores
        }
        