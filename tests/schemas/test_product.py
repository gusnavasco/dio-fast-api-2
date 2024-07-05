from pydantic import ValidationError
import pytest
from tdd_project.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_return_success():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 pro Max"


def test_schemas_return_raise():
    data = dict(name="Iphone 14 pro Max", quantity=10, price=8500)

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 14 pro Max", "quantity": 10, "price": 8500},
        "url": "https://errors.pydantic.dev/2.8/v/missing",
    }
