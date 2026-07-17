from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.core.cache import cache

from blog.models import Post


class RecommendationService:

    CACHE_KEY = "recommendation_matrix"

    @classmethod
    def build_similarity_matrix(cls):
        """
        Build TF-IDF vectors and cosine similarity matrix.
        Cache the result for faster recommendations.
        """

        posts = list(
            Post.objects.filter(
                is_published=True
            )
        )

        if len(posts) < 2:
            return None

        documents = [
            f"{p.title} {p.content}"
            for p in posts
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(tfidf)

        cache.set(
            cls.CACHE_KEY,
            {
                "posts": posts,
                "similarity": similarity,
            },
            timeout=None
        )

        return cache.get(cls.CACHE_KEY)

    @classmethod
    def get_cached_matrix(cls):

        matrix = cache.get(cls.CACHE_KEY)

        if matrix is None:
            matrix = cls.build_similarity_matrix()

        return matrix