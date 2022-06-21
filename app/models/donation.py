from pydantic import BaseModel
from typing import Union

from decimal import Decimal


class Donation(BaseModel):
    Amount: Decimal
    Message: str
