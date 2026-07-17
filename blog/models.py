from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from .ai.ai_summarizer import ArticleSummarizer



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    title = models.CharField(max_length=250)

    slug = models.SlugField(unique=True, blank=True)

    author = models.CharField(
        max_length=100,
        default="Sarthak Agrawal"
    )

    featured_image = models.ImageField(
        upload_to="blog_images/"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True)
    
    summary = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        # Generate summary only if needed
        if self.content and not self.summary:
            try:
                self.summary = ArticleSummarizer.summarize(self.content)
            except Exception as e:
                print("Summary generation failed:", e)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    content = models.TextField()

    #AI Moderation using toxicity model
    is_approved = models.BooleanField(default=True)

    toxicity_score = models.FloatField(default=0.0)
    
    toxicity_label = models.CharField(
        max_length=30,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =["created_at"]
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
        
    
    


class Contact(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class UserInteraction(models.Model):

    INTERACTION_TYPES = [
        ("view", "View"),
        ("like", "Like"),
        ("bookmark", "Bookmark"),
        ("search", "Search"),
        ("comment", "Comment"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interactions"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="interactions"
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.post.title}"    
    

class ReadingSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    started_at = models.DateTimeField(auto_now_add=True)

    duration_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.post.title} "
            f"({self.duration_seconds}s)"
        )   
    
class PostEmbedding(models.Model):
        
        post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="embedding")
        
        embedding = models.JSONField()
        
        updated_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return f"Embedding - {self.post.title}"
        
             