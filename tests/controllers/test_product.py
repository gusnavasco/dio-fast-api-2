from datetime import datetime, timezone
from typing import List
import pytest
from fastapi import status
from tests.factories import product_data


@pytest.mark.asyncio
async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


@pytest.mark.usefixtures("products_inserted")
@pytest.mark.asyncio
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


@pytest.mark.asyncio
async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


# ----------------------------------------------------------
@pytest.mark.asyncio
async def test_controller_patch_should_update_updated_at_field(
    client, products_url, product_inserted
):
    initial_updated_at = product_inserted.updated_at

    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()

    updated_at = datetime.fromisoformat(content["updated_at"]).replace(
        tzinfo=timezone.utc
    )

    assert response.status_code == status.HTTP_200_OK
    assert content["price"] == "7.500"
    assert updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_controller_patch_should_return_not_found(client, products_url):
    response = await client.patch(
        f"{products_url}57d1002d-de69-48bc-85a3-6377bac97360", json={"price": "7.500"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 57d1002d-de69-48bc-85a3-6377bac97360"
    }


@pytest.mark.asyncio
async def test_controller_create_multiple_products(client, products_url):
    product_data_1 = {
        "name": "Produto A",
        "quantity": 5,
        "price": "6.000",
        "status": True,
    }
    product_data_2 = {
        "name": "Produto B",
        "quantity": 3,
        "price": "9.000",
        "status": True,
    }

    response_1 = await client.post(products_url, json=product_data_1)
    response_2 = await client.post(products_url, json=product_data_2)

    assert response_1.status_code == status.HTTP_201_CREATED
    assert response_2.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_controller_query_with_price_filter(
    client, products_url, products_inserted
):
    min_price = 5000
    max_price = 8000

    response = await client.get(
        products_url, params={"min_price": min_price, "max_price": max_price}
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    for product in response.json():
        assert min_price <= float(product["price"]) <= max_price


@pytest.mark.asyncio
async def test_controller_create_should_handle_insertion_error(client, products_url):
    data = {
        "name": "Produto C",
        "quantity": 5,
        "price": "7000",
    }

    response = await client.post(products_url, json=data)

    response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "status"],
                "msg": "Field required",
                "input": {"name": "Produto C", "quantity": 5, "price": "7000"},
            }
        ]
    }
