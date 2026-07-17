from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from blog.models import Post
from .embedding_service import EmbeddingService

class SemanticRecommendationEngine:
    
    @classmethod
    def get_similar_posts(cls, post, top_n=5):

        posts = list(
            Post.objects.filter(
                is_published=True
            )
        )

        if len(posts) < 2:
            return []

        embeddings = []

        for p in posts:

            text = f"{p.title} {p.content}"

            embeddings.append(
                EmbeddingService.encode(text)
            )

        similarity = cosine_similarity(
            np.array(embeddings)
        )

        current_index = posts.index(post)

        scores = list(
            enumerate(
                similarity[current_index]
            )
        )

        scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []

        for index, score in scores:

            if posts[index].id != post.id:

                recommendations.append(posts[index])

            if len(recommendations) == top_n:
                break

        return recommendations
    