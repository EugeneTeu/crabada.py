from decimal import Decimal
from eth_typing import Address, ChecksumAddress
from numpy import number
from web3 import Web3
from web3.types import Wei
from src.common.clients import makeAvalancheCraClient, makeAvalancheTusClient
from src.common.logger import logTx, logger
from src.libs.RouterWeb3Client.PangolinRouterWeb3Client import (
    PangolinRouterWeb3Client,
)
from src.libs.RouterWeb3Client.RouterWeb3Client import RouterWeb3Client
from src.libs.RouterWeb3Client.TraderJoeRouterWeb3Client import (
    TraderJoeRouterWeb3Client,
)

from src.models.User import User
from src.common.config import nodeUri, users
from src.common.constants import tokens
from web3 import Web3

TUS_TO_AVAX_PATH = [
    Web3.toChecksumAddress("0xf693248f96fe03422fea95ac0afbbbc4a8fdd172"),
    Web3.toChecksumAddress("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"),
]

CRA_TO_AVAX_PATH = [
    Web3.toChecksumAddress("0xA32608e873F9DdEF944B24798db69d80Bbb4d1ed"),
    Web3.toChecksumAddress("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"),
]


def makePangolinClient(user: User) -> RouterWeb3Client:
    pangolinRouterContract = "0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106"
    return RouterWeb3Client(
        nodeUri=nodeUri,
        privateKey=users[0]["privateKey"],
        upperLimitForBaseFeeInGwei=user.config["mineMaxGasInGwei"],
        contractAddress=pangolinRouterContract,
    )


def makeTraderJoeClient(user: User) -> RouterWeb3Client:
    traderJoeRouterContract = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4"
    return RouterWeb3Client(
        nodeUri=nodeUri,
        privateKey=users[0]["privateKey"],
        upperLimitForBaseFeeInGwei=user.config["mineMaxGasInGwei"],
        contractAddress=traderJoeRouterContract,
    )


def getTusBalance(address: Address) -> int:
    tusClient = makeAvalancheTusClient()
    return tusClient.balanceOf(address)


def getCraBalance(address: Address) -> int:
    craClient = makeAvalancheCraClient()
    return craClient.balanceOf(address)


def swapTokenToAvaxPangolin(
    user: User, amtIn: Wei, path: list[ChecksumAddress]
) -> None:
    """
    amtIn here is in wei
    """
    client = makePangolinClient(user)
    amtsOut = client.getAmountsOut(amtIn, path)
    amtOut = amtsOut[len(amtsOut) - 1]
    # account for slippage
    amtOutMin = int(amtOut / 100 * 99.5)
    askForUserInput(amtIn, amtOutMin, path, client)


def swapTokenToAvaxTraderJoe(
    user: User, amtIn: Wei, path: list[ChecksumAddress]
) -> None:
    """
    amtIn here is in wei
    """
    client = makeTraderJoeClient(user)
    amtsOut = client.getAmountsOut(amtIn, path)
    amtOut = amtsOut[len(amtsOut) - 1]
    # account for slippage
    amtOutMin = int(amtOut / 100 * 99.5)
    askForUserInput(amtIn, amtOutMin, path, client)


def swapTokenToAvaxTraderJoeVariableBalance(
    user: User, balance: Decimal, path: list[ChecksumAddress]
) -> None:
    """
    balance here in readable format (ethers)
    """

    while True:
        ans = Decimal(input(f"Currently you have {balance}. Input amount to swap: "))
        if ans > balance or ans <= 0:
            logger.error("Amount given not a possible swap amount")
            break
        else:
            swapTokenToAvaxTraderJoe(user, Web3.toWei(ans, "ether"), path)
            break


def askForUserInput(
    amtIn: Wei,
    amtOutMin: int,
    path: list[ChecksumAddress],
    client: RouterWeb3Client,
) -> None:
    readableAmtIn = Web3.fromWei(amtIn, "ether")
    readableAmtOutMin = Web3.fromWei(amtOutMin, "ether")
    while True:
        ans = input(
            f"Swapping {readableAmtIn} {path[0]} for {readableAmtOutMin} {path[1]}. proceed?[Y/N]: "
        )
        if ans == "Y" or ans == "y":
            swapTokenForAvax(amtIn, amtOutMin, path, client)
        else:
            logger.info("user rejected txn")
        break


def swapTokenForAvax(
    amtIn: float,
    amtOutMin: float,
    path: list[ChecksumAddress],
    client: RouterWeb3Client,
) -> None:
    txHash = client.swapExactTokensForAvax(amtIn, amtOutMin, path)
    logger.info(txHash)
    txReceipt = client.getTransactionReceipt(txHash)
    logTx(txReceipt)
