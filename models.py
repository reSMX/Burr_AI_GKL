from pydantic import BaseModel
from typing import Union

import numpy as np


class AudioFile(BaseModel):
    y: Union[list[float] | None] = None
    sr: Union[int | None] = None