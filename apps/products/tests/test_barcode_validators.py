import pytest
from django.core.exceptions import ValidationError

from apps.products.validators.barcode import validate_ean13, validate_upca


@pytest.mark.parametrize(
    "barcode",
    ["4006381333931", "5901234123457", "9780306406157"],
)
def test_valid_ean13(barcode):
    validate_ean13(barcode)


@pytest.mark.parametrize(
    "barcode",
    [
        "4006381333932",
        "400638133393",
        "40063813339312",
        "ABCDEFGHIJKLM",
        "",
    ],
)
def test_invalid_ean13(barcode):
    with pytest.raises(ValidationError):
        validate_ean13(barcode)


@pytest.mark.parametrize(
    "barcode",
    [
        "036000291452",
        "012345678905",
        "042100005264",
    ],
)
def test_valid_upca(barcode):
    validate_upca(barcode)


@pytest.mark.parametrize(
    "barcode",
    [
        "036000291453",
        "03600029145",
        "0360002914520",
        "ABCDEFGHIJKL",
        "",
        "０36000291452",
    ],
)
def test_invalid_upca(barcode):
    with pytest.raises(ValidationError):
        validate_upca(barcode)
