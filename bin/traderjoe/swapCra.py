#!/usr/bin/env python3
"""
script to swap CRA to avax via traderjoe with variable balance

Usage:
    python3 -m bin.traderjoe.swapCra

"""
from typing import cast
from web3 import Web3

from src.helpers.general import secondOrNone, thirdOrNone
from src.common.config import nodeUri, users
from src.models.User import User
from sys import argv
from src.common.logger import logger
from src.swap import (
    CRA_TO_AVAX_PATH,
    getCraBalance,
    swapTokenToAvaxTraderJoe,
    swapTokenToAvaxTraderJoeVariableBalance,
)

userAddress = users[0]["address"]
readableCraBalance = Web3.fromWei(getCraBalance(userAddress), "ether")
swapTokenToAvaxTraderJoeVariableBalance(
    User(userAddress), readableCraBalance, CRA_TO_AVAX_PATH
)
