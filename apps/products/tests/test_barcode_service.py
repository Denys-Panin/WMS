import pytest
from django.core.exceptions import ValidationError

from apps.products.models import ProductBarcode
from apps.products.services.barcode import create_barcode, get_product_by_barcode


@pytest.mark.django_db
def test_create_valid_barcode(product):
    barcode = create_barcode(
        product=product,
        barcode="4006381333931",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
        is_primary=True,
    )

    assert barcode.pk is not None
    assert barcode.product == product
    assert barcode.is_primary is True
    assert product.barcodes.count() == 1


@pytest.mark.django_db
def test_service_rejects_invalid_barcode(product):
    with pytest.raises(ValidationError):
        create_barcode(
            product=product,
            barcode="4006381333932",
            barcode_type=ProductBarcode.BarcodeType.EAN13,
        )

    assert product.barcodes.count() == 0


@pytest.mark.django_db
def test_service_rejects_duplicate_barcode(product):
    create_barcode(
        product=product,
        barcode="4006381333931",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
    )

    with pytest.raises(ValidationError):
        create_barcode(
            product=product,
            barcode="4006381333931",
            barcode_type=ProductBarcode.BarcodeType.EAN13,
        )

    assert product.barcodes.count() == 1


@pytest.mark.django_db
def test_get_product_by_barcode(product):
    create_barcode(
        product=product,
        barcode="4006381333931",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
    )

    result = get_product_by_barcode("4006381333931")

    assert result == product


@pytest.mark.django_db
def test_get_product_by_barcode_not_found(product):
    with pytest.raises(ProductBarcode.DoesNotExist):
        get_product_by_barcode("9999999999999")


@pytest.mark.django_db
def test_get_product_by_barcode_query_count(product, django_assert_num_queries):
    create_barcode(
        product=product,
        barcode="4006381333931",
        barcode_type=ProductBarcode.BarcodeType.EAN13,
    )

    with django_assert_num_queries(1):
        result = get_product_by_barcode("4006381333931")
        assert result.name == product.name
