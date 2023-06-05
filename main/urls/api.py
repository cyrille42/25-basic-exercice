from django.urls import path, include

from rest_framework import routers
from sales.views import SaleCreateView, SaleUpdateView, SaleListView, ArticleListView
from users.views import UserLoginView

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                path("login/", UserLoginView.as_view(), name="api-login"),
                path('sales/', SaleCreateView.as_view(), name='sale-create'),
                path('sales/<int:pk>/', SaleUpdateView.as_view(), name='sale-update'),
                path('sales/list/', SaleListView.as_view(), name='sale-list'),
                path('articles/list/', ArticleListView.as_view(), name='article-list'),
            ]
        ),
    )
]
