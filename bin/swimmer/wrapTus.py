#!/usr/bin/env python3
"""
script to wrap TUS to wTUS via wrap.swimmer.network

Usage:
    python3 -m bin.swimmer.wrapTus <ur address> <amount of TUS to wrap>

"""

from eth_typing import Address
from web3 import Web3
from src.common.clients import makeSwimmerNetworkClient, makeSwimmerWtusClient
from src.common.logger import logger, logTx

# code smell, circular dependency
swimmerNetworkClient = makeSwimmerNetworkClient()
wTusClient = makeSwimmerWtusClient()

# wTusClient.deposit(Web3.toWei(100, "ether"))
# gas token
tusBalance = swimmerNetworkClient.w3.eth.get_balance(
    swimmerNetworkClient.account.address
)
# normal contract balance
wTusBalance = wTusClient.balanceOf(wTusClient.account.address)


print(tusBalance)
print(wTusBalance)
txHash = wTusClient.deposit(Web3.toWei(100, "ether"))
logger.info(txHash)
txReceipt = wTusClient.getTransactionReceipt(txHash)
logTx(txReceipt)


tusBalance = swimmerNetworkClient.w3.eth.get_balance(
    swimmerNetworkClient.account.address
)
# normal contract balance
wTusBalance = wTusClient.balanceOf(wTusClient.account.address)
print(tusBalance)
print(wTusBalance)
