from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .services.recommendation_service import RecommendationService

from blog.ai.embedding_service import EmbeddingService


@receiver(post_save, sender=Post)
def update_ai_assets(sender, instance, **kwargs):

    RecommendationService.build_similarity_matrix()

    EmbeddingService.generate_embedding(instance)