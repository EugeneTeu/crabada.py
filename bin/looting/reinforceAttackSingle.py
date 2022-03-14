#!/usr/bin/env python3
"""
Crabada script to reinforce all looting teams of the given user

Usage:
    python3 -m bin.looting.reinforceAttackSingle <userAddress> <teamId>

"""

from src.bot.looting.reinforceAttack import reinforceAttack
from src.bot.looting.reinforceAttackSingle import reinforceAttackSingle
from src.helpers.general import secondOrNone, thirdOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv

userAddress = secondOrNone(argv)

teamId = thirdOrNone(argv)

if not teamId:
    logger.error('Specify a team id')
    exit(1)

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

if not User.isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)

nReinforced = reinforceAttackSingle(userAddress, teamId)
