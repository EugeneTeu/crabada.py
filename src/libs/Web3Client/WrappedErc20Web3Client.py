from typing import Any, Union
from eth_typing import Address, HexStr
from web3 import Web3
from web3.types import Wei
from src.libs.Web3Client.Erc20Web3Client import Erc20Web3Client
from src.libs.Web3Client.Web3Client import Web3Client
from web3.types import TxParams, Nonce
import os


class WrappedErc20Web3Client(Erc20Web3Client):

    """
    Client that comes with the wrapped ERC20 ABI preloaded.

    AMOUNTS
    =======

    Whenever we will refer to an "amount" of the token, we really mean an
    "amount in token units". A token unit is the smallest subdivision of
    the token. For example:
    - If the token has 6 digits (like most stablecoins) an amount of 1
      corresponds to one millionth of the token.
    - For tokens with 18 digits (like most non-stablecoins) an amount
      of 1 is equal to 1/10^18 of the token (a single wei).
    """

    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/wrappedErc20Abi.json")

    def deposit(self, amount: Wei) -> HexStr:
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.deposit(), valueInWei=amount
        )
        return self.signAndSendTransaction(tx)
