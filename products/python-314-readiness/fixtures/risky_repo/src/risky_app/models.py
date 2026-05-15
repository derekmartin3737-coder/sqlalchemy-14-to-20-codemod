from __future__ import annotations

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import Any, get_type_hints

from pydantic.v1 import BaseModel


class LegacyUser(BaseModel):
    id: int
    email: str


class JobHandlers:
    printer = partial(print, "job")


def read_annotations(model: type[Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    return model.__annotations__, get_type_hints(model)


def run_workers() -> None:
    with ProcessPoolExecutor() as pool:
        list(pool.map(str, [1, 2, 3]))
    with mp.Pool(processes=1) as pool:
        pool.map(str, [1])
