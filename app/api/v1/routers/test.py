from fastapi import APIRouter,Query,Path,Body
from enum import Enum
from pydantic import BaseModel,Field
from typing import Annotated,Literal

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

@router.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@router.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

@router.get("/items_get/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="Item ID", description="The ID of the item to get",ge=1,le=1000)],
    size: Annotated[float, Query(gt=0, lt=10.5)],
    q: Annotated[list[str] | None, Query(title="query list",
                                                          description="this is a query list",
                                                          min_length=3,
                                                          alias="q-alias",
                                                          deprecated=True,
                                                          include_in_schema=False)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results