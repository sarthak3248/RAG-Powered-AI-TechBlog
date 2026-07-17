from sentence_transformers import SentenceTransformer
import numpy as np
from blog.models import PostEmbedding

class EmbeddingService:
    _model = None
    
    @classmethod
    def get_model(cls):
        
        if cls._model is None:
            
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
            
        return cls._model
    
    @classmethod
    def generate_embedding(cls, post):

        text = f"{post.title} {post.content}"

        embedding = cls.get_model().encode(
            text
        ).tolist()

        PostEmbedding.objects.update_or_create(
            post=post,
            defaults={
                "embedding": embedding
            }
        )
    
    
    @classmethod
    def get_embedding(cls, post):
        
        try:
            return post.embedding.embedding
        
        except PostEmbedding.DoesNotExist:
            
            cls.generate_embedding(post)
            
            return post.embedding.embedding
        
    @classmethod
    def encode(cls, text):
        
        return cls.get_model().encode(text).tolist()
    
    
    @staticmethod
    def cosine_similarity(vec1, vec2):
        
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        denominator = np.linalg.norm(v1) * np.linalg.norm(v2)
        
        if denominator == 0:
            return 0.0
        
        return float(np.dot(v1,v2)/denominator)
            
    
        