import pytest
from django.db import IntegrityError, transaction

from apps.products.models import ProductCondition


@pytest.mark.django_db
def test_create_product_condition():
    condition = ProductCondition.objects.create(
        code="NEW",
        name="New",
    )

    assert condition.code == "NEW"
    assert condition.name == "New"
    assert condition.is_active is True
    assert str(condition) == "New"


@pytest.mark.django_db
def test_condition_must_be_unique():
    ProductCondition.objects.create(
        code="NEW",
        name="New",
    )

    with pytest.raises(IntegrityError), transaction.atomic():
        ProductCondition.objects.create(code="NEW", name="Another New")


@pytest.mark.django_db
def test_create_inactive_condition():
    condition = ProductCondition.objects.create(
        code="DAMAGED",
        name="Damaged",
        is_active=False,
    )

    assert condition.is_active is False


@pytest.mark.django_db
def test_condition_ordered_by_name():
    ProductCondition.objects.create(code="USED", name="Used")
    ProductCondition.objects.create(code="NEW", name="New")
    ProductCondition.objects.create(code="DAMAGED", name="Damaged")

    condition = list(ProductCondition.objects.values_list("name", flat=True))

    assert condition == ["Damaged", "New", "Used"]
