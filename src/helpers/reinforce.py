from typing import Literal
from eth_typing.evm import Address
from web3.types import Wei
from src.helpers.mines import (
    mineHasBeenAttacked,
    mineIsOpen,
    mineIsSettled,
    mineReadyToBeSettled,
)
from src.models.User import User
from src.libs.CrabadaWeb2Client.types import Game


def getTimesMinerReinforced(mine: Game) -> int:
    """
    Number of times the miner has reinforced so far
    """
    return len([x for x in mine["process"] if x["action"] == "reinforce-defense"])


def minerCanReinforce(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment, regardless of whether its the first or the
    second time
    """
    return getMinerReinforcementStatus(mine) != 0


def getMinerReinforcementStatus(mine: Game) -> Literal[0, 1, 2]:
    """
    Determines whether the miner can reinforce and, if this
    is the case, whether the 1st or 2nd reinforcement is
    needed

    Returns:
    - 0 if the miner cannot reinforce
    - 1 if the miner can reinforce for the first time
    - 2 if the miner can reinforce for the second time
    """
    if minerCanReinforceForTheFirstTime(mine):
        return 1
    elif minerCanReinforceForTheSecondTime(mine):
        return 2
    else:
        return 0


def minerCanReinforceForTheFirstTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the first time
    """
    return (
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not mineReadyToBeSettled(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 0
    )


def minerCanReinforceForTheSecondTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the miner (the defense) can
    reinforce at this moment for the second time
    """
    return (
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not mineReadyToBeSettled(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 2
    )


def getTimesLooterReinforced(mine: Game) -> int:
    """
    Number of times the looter has reinforced so far
    """
    return len([x for x in mine["process"] if x["action"] == "reinforce-attack"])


def looterCanReinforce(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment, regardless of whether its the first or the
    second time
    """
    return getLooterReinforcementStatus(mine) != 0


def getLooterReinforcementStatus(mine: Game) -> Literal[0, 1, 2]:
    """
    Determines whether the looter can reinforce and, if this
    is the case, whether the 1st or 2nd reinforcement is
    needed

    Returns:
    - 0 if the looter cannot reinforce
    - 1 if the looter can reinforce for the first time
    - 2 if the looter can reinforce for the second time
    """
    if looterCanReinforceForTheFirstTime(mine):
        return 1
    elif looterCanReinforceForTheSecondTime(mine):
        return 2
    else:
        return 0


def looterCanReinforceForTheFirstTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment for the first time
    """
    return (
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not mineReadyToBeSettled(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 1
    )


def looterCanReinforceForTheSecondTime(mine: Game) -> bool:
    """
    Return True if, in the given game, the looter (the attack) can
    reinforce at this moment for the second time
    """
    return (
        mineIsOpen(mine)
        and mineHasBeenAttacked(mine)
        and not mineReadyToBeSettled(mine)
        and not mineIsSettled(mine)
        and mine["round"] == 3
    )
