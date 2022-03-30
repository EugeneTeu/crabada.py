#!/usr/bin/env python3
"""
Crabada script to send mining all available teams for
the given user.

Usage:
    python3 -m bin.mining.sendTeamsMiningSingle <userAddress> <team id>

"""

from src.bot.mining.sendTeamsMiningSingle import sendTeamsMiningSingle
from src.helpers.general import secondOrNone, thirdOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv, exit

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

nSent = sendTeamsMiningSingle(User(userAddress), teamId)
