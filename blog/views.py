from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .forms import (RegisterForm,CommentForm,ContactForm,)
from .models import Post, Category, UserInteraction
from django.db.models import Q
from django.core.paginator import Paginator
from .services.interaction_service import InteractionService
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import UserInteraction, ReadingSession
from .ml.recommender import RecommendationEngine
from .ml.user_recommender import UserRecommendationEngine
from .ml.preference_engine import PreferenceEngine
from django.contrib import messages
from django.shortcuts import redirect
from .ai.toxicity_service import ToxicityService
from django.db.models import Avg, Sum, Count
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def home(req):
    
    posts_list = Post.objects.filter(is_published=True).order_by("-created_at")
    
    paginator = Paginator(posts_list, 3) #3 post per page
    
    page_num = req.GET.get("page")
    
    ps = paginator.get_page(page_num)
    
    context = {
        "posts": ps
    }
    
    return render(req, "home.html", context)

def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    comment_form = CommentForm()
    
    InteractionService.log_view(request.user, post)
    
    similar_posts = RecommendationEngine.get_similar_posts(post)
    
    comments = post.comments.filter(
        is_approved=True,
        parent__isnull=True
    ).select_related("user")
    
    print("COMMENTS:", comments)
    
    context = {
        "post": post,
        "liked": InteractionService.has_liked(
            request.user,
            post
        ),
        "like_count": InteractionService.get_like_count(post),
        "bookmarked": InteractionService.has_bookmarked(request.user,post),
        "similar_posts": similar_posts,
        "comment_form": comment_form,
        "comments": comments,
    }

    return render(
        request,
        "blog/post_detail.html",
        context
    )

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)

    posts = Post.objects.filter(
        category=category,
        is_published=True
    ).order_by("-created_at")

    context = {
        "category": category,
        "posts": posts,
    }
    
    return render(request, "blog/category_posts.html", context)

def search_posts(request):
    query = request.GET.get("q", "")
    posts = []

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__icontains=query),
            is_published=True
        ).distinct()

    context = {
        "query": query,
        "posts": posts,
    }

    return render(request, "blog/search_results.html", context)

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )
    
@login_required
def toggle_like(request, slug):

    post = get_object_or_404(Post, slug=slug)

    liked = InteractionService.toggle_like(
        request.user,
        post
    )

    like_count = InteractionService.get_like_count(post)

    return JsonResponse({
        "liked": liked,
        "like_count": like_count,
    })    

@login_required
def toggle_bookmark(request, slug):

    post = get_object_or_404(Post, slug=slug)

    bookmarked = InteractionService.toggle_bookmark(
        request.user,
        post
    )

    return JsonResponse({
        "bookmarked": bookmarked
    })

@login_required
@require_POST
def save_reading_session(request, slug):

    post = get_object_or_404(Post, slug=slug)

    data = json.loads(request.body)

    duration = int(data.get("duration", 0))

    InteractionService.save_reading_session(
        request.user,
        post,
        duration
    )

    return JsonResponse({
        "status": "success"
    })
    
    
@login_required
def dashboard(request):

    user = request.user

    viewed = UserInteraction.objects.filter(
        user=user,
        interaction_type="view"
    )

    liked = UserInteraction.objects.filter(
        user=user,
        interaction_type="like"
    )

    bookmarked = UserInteraction.objects.filter(
        user=user,
        interaction_type="bookmark"
    )

    recent_views = viewed.select_related("post")[:5]

    recent_likes = liked.select_related("post")[:5]

    recent_bookmarks = bookmarked.select_related("post")[:5]

    total_reading = ReadingSession.objects.filter(
        user=user
    ).aggregate(
        total=Sum("duration_seconds")
    )["total"] or 0

    hours = total_reading // 3600
    minutes = (total_reading % 3600) // 60
    
    recommended_posts = UserRecommendationEngine.recommend_for_user(
    request.user,
    top_n=5
    )
    
    category_profile = PreferenceEngine.build_user_profile(request.user)

    context = {
        "view_count": viewed.count(),
        "like_count": liked.count(),
        "bookmark_count": bookmarked.count(),
        "recent_views": recent_views,
        "recent_likes": recent_likes,
        "recent_bookmarks": recent_bookmarks,
        "reading_time": f"{hours}h {minutes}m",
        "recommended_posts": recommended_posts,
        "category_profile": category_profile,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )   
    
    
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post

            comment.user = request.user

                # -----------------------------
            # AI Toxicity Moderation
            # -----------------------------

            moderation = ToxicityService.analyze(
                comment.content
            )

            comment.is_approved = moderation["approved"]

            comment.toxicity_score = moderation["overall_score"]

            comment.toxicity_label = moderation["highest_category"]

            comment.save()

            if moderation["approved"]:

                messages.success(
                    request,
                    "✅ Your comment has been published."
                )

            else:

                messages.warning(
                    request,
                    "⚠️ Your comment has been submitted for moderation because it may contain inappropriate language."
                )
    
    return redirect("post_detail", slug=slug)   


@staff_member_required
def ai_dashboard(req):
    from . models import (Post, UserInteraction, ReadingSession, Comment, Category)
    
    total_post = Post.objects.count()
    
    total_views = UserInteraction.objects.filter(
        interaction_type="view"
    ).count()
    
    total_likes = UserInteraction.objects.filter(
       interaction_type="like"
    ).count()
    
    total_bookmark = UserInteraction.objects.filter(
        interaction_type = "bookmark"
    ).count()
    
    total_reading = ReadingSession.objects.aggregate(
        total=Sum("duration_seconds")
    )["total"] or 0
    
    approved_comments = Comment.objects.filter(
        is_approved="True"
    ).count()
    
    flagged_comments = Comment.objects.filter(
        is_approved="False"
    ).count()
    
    avg_toxicity = Comment.objects.aggregate(
        Avg("toxicity_score")
    )["toxicity_score__avg"] or 0

    popular_categories = (
        Category.objects
        .annotate(total_posts=Count("posts"))
        .order_by("-total_posts")
    )
    
    context = {
        "total_posts": total_post,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_bookmarks": total_bookmark,
        "reading_hours": round(total_reading / 3600, 2),
        "approved_comments": approved_comments,
        "flagged_comments": flagged_comments,
        "avg_toxicity": round(avg_toxicity, 3),
        "popular_categories": popular_categories,
    }
    
    return render(req, "dashboard/ai_dashboard.html", context,)

def about(request):

    technologies = [
        "Python",
        "Django",
        "Bootstrap 5",
        "SQLite",
        "PyTorch",
        "Transformers",
        "Sentence Transformers",
        "Scikit-learn",
    ]

    ai_features = [
        "🤖 AI Article Summarization",
        "🎯 Hybrid Recommendation System",
        "🧠 Semantic Recommendations",
        "🛡 AI Toxicity Detection",
        "📊 AI Analytics Dashboard",
        "📖 Reading Analytics",
    ]

    context = {
        "technologies": technologies,
        "ai_features": ai_features,
    }

    return render(
        request,
        "about.html",
        context,
    )


def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "✅ Thank you! Your message has been sent successfully."
            )

            return redirect("contact")

    else:

        form = ContactForm()

    return render(
        request,
        "contact.html",
        {
            "form": form
        }
    )        
    
def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_500(request):
    return render(request, "500.html", status=500)    
