from datetime import timedelta

from django.utils import timezone

from blog.models import UserInteraction

from blog.models import ReadingSession

class InteractionService:

    @staticmethod
    def log_view(user, post):
        """
        Record a view only if the user hasn't viewed
        the same post in the last 30 minutes.
        """

        if not user.is_authenticated:
            return

        thirty_minutes_ago = timezone.now() - timedelta(minutes=30)

        already_viewed = UserInteraction.objects.filter(
            user=user,
            post=post,
            interaction_type="view",
            timestamp__gte=thirty_minutes_ago
        ).exists()

        if not already_viewed:
            UserInteraction.objects.create(
                user=user,
                post=post,
                interaction_type="view"
            )
    
    @staticmethod
    def toggle_like(user, post):
        """
        Toggle a like for the given user and post.
        Returns True if liked, False if unliked.
        """

        if not user.is_authenticated:
            return False

        existing_like = UserInteraction.objects.filter(
            user=user,
            post=post,
            interaction_type="like"
        )

        if existing_like.exists():
            existing_like.delete()
            return False

        UserInteraction.objects.create(
            user=user,
            post=post,
            interaction_type="like"
        )

        return True


    @staticmethod
    def get_like_count(post):
        return UserInteraction.objects.filter(
            post=post,
            interaction_type="like"
        ).count()


    @staticmethod
    def has_liked(user, post):
        if not user.is_authenticated:
            return False

        return UserInteraction.objects.filter(
            user=user,
            post=post,
            interaction_type="like"
        ).exists()        
        
    @staticmethod
    def toggle_bookmark(user, post):
        """
        Toggle bookmark status.
        Returns True if bookmarked,
        False if removed.
        """

        if not user.is_authenticated:
            return False

        bookmark = UserInteraction.objects.filter(
            user=user,
            post=post,
            interaction_type="bookmark"
        )

        if bookmark.exists():
            bookmark.delete()
            return False

        UserInteraction.objects.create(
            user=user,
            post=post,
            interaction_type="bookmark"
        )

        return True


    @staticmethod
    def has_bookmarked(user, post):

        if not user.is_authenticated:
            return False

        return UserInteraction.objects.filter(
            user=user,
            post=post,
            interaction_type="bookmark"
        ).exists()        
        
    @staticmethod
    def save_reading_session(user, post, duration):

        if not user.is_authenticated:
            return

        # Ignore accidental clicks
        if duration < 5:
            return

        ReadingSession.objects.create(
            user=user,
            post=post,
            duration_seconds=duration
        )