import numpy as np
from blog.models import PostEmbedding
from blog.ai.embedding_service import EmbeddingService

class Retriver:    
    @staticmethod
    def retrive(query, top_k=3):
        
        query_embedding = EmbeddingService.encode(query)
        
        scored_posts = []
        
        for item in PostEmbedding.objects.select_related("post"):
            
            score = EmbeddingService.cosine_similarity(
                query_embedding,
                item.embedding
            )        
            
            scored_posts.append(
            (score, item.post)
            )
        
        scored_posts.sort(
            key=lambda x:x[0], reverse=True
        )
        
        return [
            post for score, post in scored_posts[:top_k]
        ]
        
        
        