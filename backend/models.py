from pydantic import BaseModel
from typing import Union
from datetime import datetime

import numpy as np


class AudioFile(BaseModel):
    y: Union[list | None] = None
    sr: Union[int | None] = None


class ResultMeas(BaseModel):
    data_last_meas: datetime
    res_last_meas: bool