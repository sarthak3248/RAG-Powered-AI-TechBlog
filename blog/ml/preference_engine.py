from collections import defaultdict

from blog.models import UserInteraction, ReadingSession


class PreferenceEngine:

    INTERACTION_WEIGHTS = {
        "view": 1,
        "like": 5,
        "bookmark": 7,
    }

    READING_SESSION_WEIGHT = 3

    @classmethod
    def build_user_profile(cls, user):

        scores = defaultdict(float)

        interactions = UserInteraction.objects.filter(
            user=user
        ).select_related(
            "post__category"
        )

        for interaction in interactions:

            category = interaction.post.category.name

            scores[category] += cls.INTERACTION_WEIGHTS.get(
                interaction.interaction_type,
                0
            )

        sessions = ReadingSession.objects.filter(
            user=user
        ).select_related(
            "post__category"
        )

        for session in sessions:

            if session.duration_seconds >= 30:

                category = session.post.category.name

                scores[category] += cls.READING_SESSION_WEIGHT

        return dict(scores)