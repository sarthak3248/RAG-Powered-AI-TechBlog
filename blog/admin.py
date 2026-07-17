from django.contrib import admin
from . models import Category, Post, Comment, Contact, UserInteraction, ReadingSession, PostEmbedding

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "created_at",
        "is_published",
    )
    
    list_filter = (
            "category",
            "is_published",
            "created_at",
            )   
    
    search_fields = (
        "title",
        "content",
    ) 
    
    prepopulated_fields = {"slug": ("title",)}
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    list_display = (
        "user",
        "post",
        "toxicity_label",
        "toxicity_score",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "toxicity_label",
        "is_approved",
    )

    search_fields = (
        "user__username",
        "post__title",
        "content",
    )

    ordering = (
        "-created_at",
    )
    
    actions = ["approve_comments"]

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):

        queryset.update(is_approved=True)
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
    )    
    
@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "post",
        "interaction_type",
        "timestamp",
    )

    list_filter = (
        "interaction_type",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "post__title",
    )

    ordering = ("-timestamp",)    
    
@admin.register(ReadingSession)    
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "duration_seconds",
        "started_at",
    )

    list_filter = ("started_at",)
    
@admin.register(PostEmbedding)
class PostEmbeddingAdmin(admin.ModelAdmin):
    
    list_display=(
        "post",
        "updated_at",
    )
    
    search_fields=(
        "post_title",
    )
    
    
admin.site.site_header = "TechBlog Administration"
admin.site.site_title = "TechBlog Admin Portal"
admin.site.index_title = "Welcome to TechBlog Dashboard"    

