from pydantic import BaseModel
from typing import List

from decimal import Decimal


class FundRequest(BaseModel):
    StartAmount: Decimal
    Motivation: str
    IBAN: str


class NeedType(BaseModel):
    Needs: List[int]
