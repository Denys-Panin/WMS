from django.db import models


class ProductPrice(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="prices",
    )
    condition = models.ForeignKey(
        "products.ProductCondition",
        on_delete=models.PROTECT,
        related_name="prices",
    )
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    currency = models.CharField(
        max_length=5,
        default="EUR",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product", "condition", "currency"]

        constraints = [
            models.UniqueConstraint(
                fields=["product", "condition", "currency"],
                name="unique_product_condition_currency",
            ),
            models.CheckConstraint(
                condition=models.Q(purchase_price__gte=0),
                name="product_purchase_price_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(selling_price__gte=0),
                name="product_selling_price_non_negative",
            ),
        ]

    def __str__(self):
        return f"{self.product.sku} - {self.condition.code} - {self.currency}"
