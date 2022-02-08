import csv
import json
from typing import Any


def read(path: str) -> list[list[str]]:
    outputs = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            outputs.append(row)

    # remove header
    return outputs[1:]


def write(obj: Any, path: str):
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(
            obj,
            f,
            indent=2,
            ensure_ascii=False,
        )
