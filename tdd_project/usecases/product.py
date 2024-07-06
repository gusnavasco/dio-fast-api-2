from datetime import datetime, timezone
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from pymongo.errors import DuplicateKeyError, PyMongoError
from tdd_project.db.mongo import db_client
from tdd_project.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateOut,
)
from typing import List, Optional
from tdd_project.core.exceptions import InsertionErrorException, NotFoundException
from tdd_project.models.product import ProductModel


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(product_model.model_dump())
        except DuplicateKeyError:
            raise InsertionErrorException(
                message="A product with the same ID already exists."
            )
        except PyMongoError as exc:
            raise InsertionErrorException(message=f"Error inserting product: {exc}")

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> Optional[ProductOut]:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    # async def query(self) -> List[ProductOut]:
    #     return [ProductOut(**item) async for item in self.collection.find()]
    async def query(self, filters: dict = None) -> List[ProductOut]:
        cursor = self.collection.find(filters)
        results = await cursor.to_list(length=None)
        return [ProductOut(**result) for result in results]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid fields to update")

        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if result is None:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)
        # product = ProductUpdate(**body.model_dump(exclude_none=True))
        # result = await self.collection.find_one_and_update(
        #     filter={"id": id},
        #     update={"$set": product.model_dump()},
        #     return_document=pymongo.ReturnDocument.AFTER
        # )

        # if result is None:
        #     return None

        # return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
