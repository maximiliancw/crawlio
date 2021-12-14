from dataclasses import dataclass
from typing import Callable, Any, List


def identity(obj: List[Any]) -> Any:
    """ Return the identity of a list object """
    return obj


@dataclass
class Request:
    url: str


@dataclass
class Response:
    url: str
    status: int
    html: str


@dataclass
class Selector:
    name: str
    query: str
    type: str = 'xpath'
    process: Callable[[List[Any]], Any] = identity
