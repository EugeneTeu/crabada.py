#!/usr/bin/env python3
"""
script to swap TUS to avax via traderjoe with variable balance

Usage:
    python3 -m bin.traderjoe.swapTus

"""
from typing import cast
from web3 import Web3
from decimal import Decimal

from src.helpers.general import secondOrNone, thirdOrNone
from src.common.config import nodeUri, users
from src.models.User import User
from sys import argv
from src.common.logger import logger
from src.swap import (
    TUS_TO_AVAX_PATH,
    getTusBalance,
    swapTokenToAvaxTraderJoeVariableBalance,
)

userAddress = users[0]["address"]
readableTusBalance = cast(Decimal, Web3.fromWei(getTusBalance(userAddress), "ether"))
swapTokenToAvaxTraderJoeVariableBalance(
    User(userAddress), readableTusBalance, TUS_TO_AVAX_PATH
)
