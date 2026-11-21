from decimal import Decimal

import pytest
from django.db import IntegrityError, transaction

from apps.products.models import ProductCondition, ProductPrice


@pytest.mark.django_db
def test_create_product_price(product):
    condition = ProductCondition.objects.get(code="NEW")
    price = ProductPrice.objects.create(
        product=product,
        condition=condition,
        purchase_price=Decimal("600.00"),
        selling_price=Decimal("800.00"),
        currency="EUR",
    )

    assert price.product == product
    assert price.condition == condition
    assert price.purchase_price == Decimal("600.00")
    assert price.selling_price == Decimal("800.00")
    assert price.currency == "EUR"


@pytest.mark.django_db
def test_product_price_must_be_unique(product):
    condition = ProductCondition.objects.get(code="NEW")
    ProductPrice.objects.create(
        product=product,
        condition=condition,
        purchase_price=Decimal("600.00"),
        selling_price=Decimal("800.00"),
        currency="EUR",
    )
    with pytest.raises(IntegrityError), transaction.atomic():
        ProductPrice.objects.create(
            product=product,
            condition=condition,
            purchase_price=Decimal("650.00"),
            selling_price=Decimal("850.00"),
            currency="EUR",
        )


@pytest.mark.parametrize(
    ("purchase_price", "selling_price"),
    [
        (Decimal("-100.00"), Decimal("150.00")),
        (Decimal("100.00"), Decimal("-150.00")),
    ],
)
def test_product_price_cannot_be_negative(
    product,
    purchase_price,
    selling_price,
):
    condition = ProductCondition.objects.get(code="NEW")
    with pytest.raises(IntegrityError), transaction.atomic():
        ProductPrice.objects.create(
            product=product,
            condition=condition,
            purchase_price=purchase_price,
            selling_price=selling_price,
            currency="EUR",
        )


def test_product_can_have_price_for_different_conditions(product):
    new_condition = ProductCondition.objects.get(code="NEW")
    used_condition = ProductCondition.objects.get(code="USED")

    new_price = ProductPrice.objects.create(
        product=product,
        condition=new_condition,
        purchase_price=Decimal("600.00"),
        selling_price=Decimal("800.00"),
        currency="EUR",
    )

    used_price = ProductPrice.objects.create(
        product=product,
        condition=used_condition,
        purchase_price=Decimal("350.00"),
        selling_price=Decimal("500.00"),
        currency="EUR",
    )

    assert new_price.product == used_price.product
    assert new_price.condition != used_price.condition
    assert product.prices.count() == 2


def test_product_can_have_prices_in_different_currencies(product):
    condition = ProductCondition.objects.get(code="NEW")

    ProductPrice.objects.create(
        product=product,
        condition=condition,
        purchase_price=Decimal("600.00"),
        selling_price=Decimal("800.00"),
        currency="EUR",
    )
    ProductPrice.objects.create(
        product=product,
        condition=condition,
        purchase_price=Decimal("650.00"),
        selling_price=Decimal("850.00"),
        currency="USD",
    )

    assert product.prices.count() == 2

    currencies = set(product.prices.values_list("currency", flat=True))

    assert currencies == {"EUR", "USD"}


def test_product_price_can_be_zero(product):
    condition = ProductCondition.objects.get(code="NEW")

    price = ProductPrice.objects.create(
        product=product,
        condition=condition,
        purchase_price=Decimal("0.00"),
        selling_price=Decimal("0.00"),
        currency="EUR",
    )

    price.refresh_from_db()

    assert price.purchase_price == Decimal("0.00")
    assert price.selling_price == Decimal("0.00")


def test_update_product_price(product):
    condition = ProductCondition.objects.get(code="NEW")

    price = ProductPrice.objects.create(
        product=product,
        condition=condition,
        purchase_price=Decimal("600.00"),
        selling_price=Decimal("800.00"),
        currency="EUR",
    )

    original_updated_at = price.updated_at

    price.selling_price = Decimal("900.00")
    price.save(update_fields=["selling_price", "updated_at"])
    price.refresh_from_db()

    assert price.selling_price == Decimal("900.00")
    assert price.purchase_price == Decimal("600.00")
    assert price.updated_at >= original_updated_at
