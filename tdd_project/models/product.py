from tdd_project.models.base import CreateBaseModel
from tdd_project.schemas.product import ProductIn


class ProductModel(ProductIn, CreateBaseModel):
    pass
