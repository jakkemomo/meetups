from enum import Enum


class Currency(Enum):
    USD = 840
    EUR = 978
    RUB = 643
    BYN = 974


class PeriodRepeatability(Enum):
    DAY = 'Daily'
    WEEK = 'Weekly'
    MONTH = 'Monthly'
