from typing import NamedTuple
from datetime import datetime


class UpdateInfo(NamedTuple):
    title: str
    description: str
    publication_date: datetime
    origin_url: str
    game_id: int
