from django.db import transaction

from apps.products.models import Product, ProductBarcode


@transaction.atomic
def create_barcode(
    *,
    product: Product,
    barcode: str,
    barcode_type: str = ProductBarcode.BarcodeType.OTHER,
    is_primary: bool = False,
) -> ProductBarcode:
    product_barcode = ProductBarcode(
        product=product,
        barcode=barcode,
        barcode_type=barcode_type,
        is_primary=is_primary,
    )

    product_barcode.full_clean()
    product_barcode.save()

    return product_barcode


def get_product_by_barcode(barcode: str) -> Product:
    product_barcode = ProductBarcode.objects.select_related("product").get(
        barcode=barcode
    )
    return product_barcode.product
