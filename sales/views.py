from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from .models import Article, Sale
from .serializers import ArticleSerializer, SaleSerializer, SaleListSerializer


class SaleListView(generics.ListAPIView):
    """
        API view for listing and creating sales.
        Returns sales with date, article category, article code, article name, quantity,
        unit selling price, and total selling price.
        Pagination is set to 25 items per page.
    """
    queryset = Sale.objects.all()
    serializer_class = SaleListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 25
    ordering = ['-date']


class SaleCreateView(generics.CreateAPIView):
    """
    API view for creating a sale.
    """
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]


class SaleUpdateView(generics.UpdateAPIView):
    """
    API view for updating a sale.
    Only the author of the sale can update it.
    """
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sale_id = self.kwargs['pk']
        queryset = Sale.objects.filter(id=sale_id)
        return queryset

    def perform_update(self, serializer):
        sale = self.get_object()
        if sale.author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to update this sale.")


class ArticleListView(generics.ListAPIView):
    """
    API view for listing articles.
    Returns articles with their category, total sales, profit margin percentage,
    and the date of the last sale.
    Articles are ordered by total sales in descending order.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
