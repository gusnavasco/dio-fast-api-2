from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from pydantic import UUID4
from tdd_project.schemas.product import ProductIn, ProductOut, ProductUpdate
from tdd_project.usecases.product import ProductUsecase
from tdd_project.core.exceptions import NotFoundException, InsertionErrorException


router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except InsertionErrorException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


# @router.get(path="/", status_code=status.HTTP_200_OK)
# async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
#     return await usecase.query()


@router.get("/", status_code=status.HTTP_200_OK)
async def query(
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    usecase: ProductUsecase = Depends(),
) -> List[ProductOut]:
    filters = {}
    if min_price is not None and max_price is not None:
        filters["price"] = {"$gt": min_price, "$lt": max_price}
    elif min_price is not None:
        filters["price"] = {"$gt": min_price}
    elif max_price is not None:
        filters["price"] = {"$lt": max_price}
    return await usecase.query(filters)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
