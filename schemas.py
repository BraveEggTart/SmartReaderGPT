from typing import Optional, Generic, TypeVar, Union, List

from pydantic import BaseModel

DataT = TypeVar("DataT")


class MetaModel(BaseModel, Generic[DataT]):
    code: int = 200
    msg: str = "Request response successful"
    data: Optional[Union[DataT, List, None, str]] = None


class Success(MetaModel, Generic[DataT]):
    ...


class Fail(MetaModel, Generic[DataT]):
    code: int = 400
    msg: str = "Request response failed"


class SuccessExtra(MetaModel, Generic[DataT]):
    total: int = 1
    page: int = 1
    size: int = 1
    pages: int = 1
