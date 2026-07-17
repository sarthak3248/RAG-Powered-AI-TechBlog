from blog.services.recommendation_service import RecommendationService


class RecommendationEngine:

    @staticmethod
    def get_similar_posts(post, top_n=5):

        data = RecommendationService.get_cached_matrix()

        if not data:
            return []

        posts = data["posts"]

        similarity = data["similarity"]

        try:
            current_index = posts.index(post)
        except ValueError:
            return []

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