from django.db import models


class Warehouse(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(
        max_length=150,
    )
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
