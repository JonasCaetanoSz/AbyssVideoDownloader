from dataclasses import dataclass
from typing import List


@dataclass
class VideoMedia:

    sources: list
    domains: list[str]
    fristDatas: list