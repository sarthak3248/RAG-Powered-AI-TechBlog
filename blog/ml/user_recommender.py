from collections import defaultdict
from .preference_engine import PreferenceEngine

from blog.models import (
    Post,
    UserInteraction,
    ReadingSession,
)

from .recommender import RecommendationEngine


class UserRecommendationEngine:

    INTERACTION_WEIGHTS = {
        "view": 1,
        "like": 5,
        "bookmark": 7,
    }

    @classmethod
    def recommend_for_user(cls, user, top_n=5):
        
        profile = PreferenceEngine.build_user_profile(user)

        if not user.is_authenticated:
            return Post.objects.filter(
                is_published=True
            )[:top_n]

        interacted_posts = set()

        scores = defaultdict(float)

        # -------- Views / Likes / Bookmarks --------
        interactions = UserInteraction.objects.filter(
            user=user
        ).select_related("post")

        for interaction in interactions:

            interacted_posts.add(interaction.post.id)

            weight = cls.INTERACTION_WEIGHTS.get(
                interaction.interaction_type,
                0
            )

            similar_posts = RecommendationEngine.get_similar_posts(
                interaction.post,
                top_n=5
            )

            for post in similar_posts:
                category_bonus = profile.get(post.category.name,0)
                scores[post.id] += (weight+category_bonus)

        # -------- Reading Sessions --------
        sessions = ReadingSession.objects.filter(
            user=user
        ).select_related("post")

        for session in sessions:

            if session.duration_seconds >= 30:

                similar_posts = RecommendationEngine.get_similar_posts(
                    session.post,
                    top_n=5
                )

                for post in similar_posts:
                    scores[post.id] += 3

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True
        )

        recommendations = []

        for post_id in ranked_ids:

            if post_id not in interacted_posts:

                recommendations.append(
                    Post.objects.get(id=post_id)
                )

            if len(recommendations) == top_n:
                break

        return recommendations