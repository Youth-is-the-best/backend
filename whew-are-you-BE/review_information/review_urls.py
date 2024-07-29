from django.urls import path
from .views import ReviewAPIView, ReviewDetailAPIView, ReviewLikeAPIView, ReviewStorageAPIView, CommentAPIView

urlpatterns = [
    path('', ReviewAPIView.as_view()),
    path('<int:id>/', ReviewDetailAPIView.as_view()),
    path('likes/<int:id>/', ReviewLikeAPIView.as_view()),
    path('storages/<int:id>/', ReviewStorageAPIView.as_view()),
    path('<int:review_id>/comments/', CommentAPIView.as_view())
]
