import pytest
from django.db import IntegrityError, transaction

from apps.warehouses.models import Warehouse


@pytest.mark.django_db
def test_create_warehouse():
    warehouse = Warehouse.objects.create(
        code="RIGA-01",
        name="Main Warehouse",
        address="Riga, Latvia",
    )

    assert warehouse.code == "RIGA-01"
    assert warehouse.name == "Main Warehouse"
    assert warehouse.address == "Riga, Latvia"
    assert warehouse.is_active is True
    assert warehouse.created_at is not None
    assert str(warehouse) == "RIGA-01 - Main Warehouse"


@pytest.mark.django_db
def test_warehouse_code_must_be_unique():
    Warehouse.objects.create(
        code="RIGA-01",
        name="Main Warehouse",
    )

    with pytest.raises(IntegrityError), transaction.atomic():
        Warehouse.objects.create(
            code="RIGA-01",
            name="Another Warehouse",
        )


@pytest.mark.django_db
def test_create_multiple_warehouses():
    Warehouse.objects.create(
        code="RIGA-01",
        name="First Warehouse",
    )

    Warehouse.objects.create(
        code="RIGA-02",
        name="Second Warehouse",
    )

    assert Warehouse.objects.all().count() == 2


@pytest.mark.django_db
def test_deactivate_warehosue():
    warehouse = Warehouse.objects.create(
        code="RIGA-01",
        name="Main Warehouse",
    )

    warehouse.is_active = False
    warehouse.save(update_fields=["is_active"])

    warehouse.refresh_from_db()

    assert warehouse.is_active is False


@pytest.mark.django_db
def test_warehouses_ordered_by_name():
    Warehouse.objects.create(
        code="RIGA-02",
        name="Second Warehouse",
    )

    Warehouse.objects.create(
        code="RIGA-01",
        name="Main Warehouse",
    )

    names = list(Warehouse.objects.values_list("name", flat=True))

    assert names == [
        "Main Warehouse",
        "Second Warehouse",
    ]
