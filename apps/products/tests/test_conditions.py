import pytest
from django.db import IntegrityError, transaction

from apps.products.models import ProductCondition


@pytest.mark.django_db
def test_create_product_condition():
    condition = ProductCondition.objects.create(
        code="TEST_NEW",
        name="Test new",
    )

    assert condition.code == "TEST_NEW"
    assert condition.name == "Test new"
    assert condition.is_active is True
    assert str(condition) == "Test new"


@pytest.mark.django_db
def test_condition_must_be_unique():
    ProductCondition.objects.create(
        code="TEST_DUPLICATE",
        name="First",
    )

    with pytest.raises(IntegrityError), transaction.atomic():
        ProductCondition.objects.create(code="TEST_DUPLICATE", name="Second")


@pytest.mark.django_db
def test_create_inactive_condition():
    condition = ProductCondition.objects.create(
        code="TEST_DAMAGED",
        name="Test damaged",
        is_active=False,
    )

    assert condition.is_active is False


@pytest.mark.django_db
def test_condition_ordered_by_name():
    ProductCondition.objects.create(code="TEST_USED", name="Used")
    ProductCondition.objects.create(code="TEST_NEW", name="New")
    ProductCondition.objects.create(code="TEST_DAMAGED", name="Damaged")

    condition = list(
        ProductCondition.objects.filter(code__startswith="TEST_").values_list(
            "name", flat=True
        )
    )

    assert condition == ["Damaged", "New", "Used"]


@pytest.mark.django_db
def test_initial_conditions_exist():
    expected_codes = {
        "NEW",
        "USED",
        "DAMAGED",
        "REFURBISHED",
    }

    actual_codes = set(
        ProductCondition.objects.filter(code__in=expected_codes).values_list(
            "code", flat=True
        )
    )

    assert actual_codes == expected_codes
