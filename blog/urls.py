from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

handler404 = "blog.views.custom_404"
handler500 = "blog.views.custom_500"

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.register, name='register'),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>", views.category_posts, name="category_posts"),
    path("search/", views.search_posts, name="search_posts"),
    path("post/<slug:slug>/like/",views.toggle_like,name="toggle_like"),
    path("post/<slug:slug>/bookmark/",views.toggle_bookmark,name="toggle_bookmark"),
    path("post/<slug:slug>/reading-session/",views.save_reading_session,name="save_reading_session"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("post/<slug:slug>/comment/",views.add_comment,name="add_comment",),
    path("ai-dashboard/",views.ai_dashboard,name="ai_dashboard",),
    path("about/",views.about,name="about",),
    path("contact/", views.contact, name="contact",),
]

