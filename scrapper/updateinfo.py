from typing import NamedTuple
from datetime import datetime


class UpdateInfo(NamedTuple):
    title: str
    description: str
    short_description: str
    image_url: str
    publication_date: datetime
    origin_url: str
    game_id: int
