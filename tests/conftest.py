import pytest
from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import MockERC20

@pytest.fixture
def amount_stacked():
    return Web3.toWei(1, "ether")

@pytest.fixture
def random_erc20():
    account = get_account()
    erc20 = MockERC20.deploy({"from": account})
    return erc20
