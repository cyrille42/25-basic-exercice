from django.db.models import Sum, F
from rest_framework import serializers
from .models import Article, Sale


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    total_sales = serializers.SerializerMethodField()
    profit_margin = serializers.SerializerMethodField()
    last_sale_date = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "code",
            "name",
            "category",
            "total_sales",
            "profit_margin",
            "last_sale_date",
        )

    def get_total_sales(self, obj):
        return Sale.objects.filter(article=obj).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0

    def get_profit_margin(self, obj):
        total_cost = self.get_total_sales(obj) * obj.manufacturing_cost
        total_revenue = Sale.objects.filter(article=obj).aggregate(total_revenue=Sum(F('unit_selling_price') * F('quantity')))['total_revenue'] or 0
        return ((total_revenue - total_cost) / total_revenue) * 100 if total_revenue > 0 else 0

    def get_last_sale_date(self, obj):
        sale = Sale.objects.filter(article=obj).order_by('-date').first()
        return sale.date if sale else None


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('date', 'author', 'article', 'quantity', 'unit_selling_price')


class SaleListSerializer(serializers.ModelSerializer):
    article_category = serializers.ReadOnlyField(source="article.category.display_name")
    article_code = serializers.ReadOnlyField(source="article.code")
    article_name = serializers.ReadOnlyField(source="article.name")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            "date",
            "article_category",
            "article_code",
            "article_name",
            "quantity",
            "unit_selling_price",
            "total_price",
        )

    def get_total_price(self, obj):
        return obj.quantity * obj.unit_selling_price