from scripts.helpful_scripts import get_account, get_contract
from brownie import SunucashToken, TokenFarm, network, config
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")
initial_supply = Web3.toWei(14000000, "ether")

def deploy_token_farm_and_sunucash_token():
    account = get_account()
    sunucash_token = SunucashToken.deploy(initial_supply, {"from": account})
    token_farm = TokenFarm.deploy(
        sunucash_token.address, 
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
        )
    tx = sunucash_token.transfer(
        token_farm.address, sunucash_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    # sunacashToken, weth_token, dai_token
    weth_token = get_contract("weth_token")
    dai_token = get_contract("dai_token")
    dict_of_allowed_tokens = {
        sunucash_token: get_contract("dai_usd_price_feed"),
        dai_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    return token_farm, sunucash_token

def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(token.address, dict_of_allowed_tokens[token], {"from": account})
        set_tx.wait(1)
    return token_farm

def main():
    deploy_token_farm_and_sunucash_token()