import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError

from apps.products.models import Product, ProductBarcode


@pytest.mark.django_db
def test_create_barcode(product):
    barcode = ProductBarcode.objects.create(
        product=product,
        barcode="5901234567890",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
        is_primary=True,
    )

    assert barcode.product == product
    assert barcode.barcode == "5901234567890"
    assert barcode.is_primary is True


@pytest.mark.django_db
def test_product_can_have_multiple_barcodes(product):
    ProductBarcode.objects.create(
        product=product,
        barcode="0591234567890",
    )

    ProductBarcode.objects.create(
        product=product,
        barcode="5901234567891",
    )

    assert product.barcodes.count() == 2


@pytest.mark.django_db
def test_barcode_must_be_unique(product):
    ProductBarcode.objects.create(
        product=product,
        barcode="0591234567890",
    )

    with pytest.raises(IntegrityError), transaction.atomic():
        ProductBarcode.objects.create(product=product, barcode="0591234567890")


@pytest.mark.django_db
def test_only_one_primary_barcode_per_product(product):
    ProductBarcode.objects.create(
        product=product,
        barcode="0591234567890",
        is_primary=True,
    )

    with pytest.raises(IntegrityError), transaction.atomic():
        ProductBarcode.objects.create(
            product=product,
            barcode="0591234567891",
            is_primary=True,
        )


@pytest.mark.django_db
def test_multiple_non_primary_barcodes_allowed(product):
    ProductBarcode.objects.create(
        product=product,
        barcode="5901234567890",
        is_primary=False,
    )

    ProductBarcode.objects.create(
        product=product,
        barcode="5901234567891",
        is_primary=False,
    )

    assert product.barcodes.filter(is_primary=False).count() == 2


@pytest.mark.django_db
def test_cannot_delete_product_with_barcodes(product):
    ProductBarcode.objects.create(
        product=product,
        barcode="5901234567890",
        is_primary=False,
    )

    with pytest.raises(ProtectedError):
        product.delete()


@pytest.mark.django_db
def test_different_products_can_have_primary_barcodes(product):
    another_product = Product.objects.create(
        sku="LEN-T14-002",
        name="Another product",
        category=product.category,
    )

    ProductBarcode.objects.create(
        product=product,
        barcode="5901234567890",
        is_primary=True,
    )

    ProductBarcode.objects.create(
        product=another_product,
        barcode="5901234567891",
        is_primary=True,
    )

    assert ProductBarcode.objects.filter(is_primary=True).count() == 2


@pytest.mark.django_db
def test_model_accepts_valid_ean13(product):
    barcode = ProductBarcode(
        product=product,
        barcode="4006381333931",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
    )

    barcode.full_clean()


@pytest.mark.django_db
def test_model_rejects_invalid_ean13(product):
    barcode = ProductBarcode(
        product=product,
        barcode="4006381333932",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
    )

    with pytest.raises(ValidationError) as exc_info:
        barcode.full_clean()

    assert "barcode" in exc_info.value.message_dict


@pytest.mark.django_db
def test_model_accepts_valid_upca(product):
    barcode = ProductBarcode(
        product=product,
        barcode="036000291452",
        barcode_type=ProductBarcode.BarcodeType.UPC,
    )

    barcode.full_clean()


@pytest.mark.django_db
def test_model_rejects_invalid_upca(product):
    barcode = ProductBarcode(
        product=product,
        barcode="036000291453",
        barcode_type=ProductBarcode.BarcodeType.UPC,
    )

    with pytest.raises(ValidationError) as exc_info:
        barcode.full_clean()

        assert "barcode" in exc_info.value.message_dict


@pytest.mark.django_db
def test_model_rejects_empty_barcode(product):
    barcode = ProductBarcode(
        product=product, barcode="   ", barcode_type=ProductBarcode.BarcodeType.OTHER
    )

    with pytest.raises(ValidationError) as exc_info:
        barcode.full_clean()

    assert "barcode" in exc_info.value.message_dict
