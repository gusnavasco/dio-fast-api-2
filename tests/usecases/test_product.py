from typing import List
from uuid import UUID
import pytest
from tdd_project.usecases.product import product_usecase
from tdd_project.schemas.product import ProductOut, ProductUpdateOut

from tdd_project.core.exceptions import NotFoundException


@pytest.mark.asyncio
async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


@pytest.mark.asyncio
async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert (
        err.value.message
        == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"
    )


@pytest.mark.usefixtures("products_inserted")
@pytest.mark.asyncio
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


@pytest.mark.asyncio
async def test_usecases_update_should_return_success(product_inserted, product_up):
    product_up.price = "7.500"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


@pytest.mark.asyncio
async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


@pytest.mark.asyncio
async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert (
        err.value.message
        == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"
    )
