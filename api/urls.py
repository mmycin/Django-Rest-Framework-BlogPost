from django.urls import path
from . import views

urlpatterns = [
    path("blogs", view=views.BlogPostListCreate.as_view(), name="blog-view-create"),
    path(
        "blogs/<int:pk>",
        view=views.BlogPostRetrieveUpdateDestroy.as_view(),
        name="update",
    ),
]
