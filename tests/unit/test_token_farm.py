from brownie import network, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract, INITIAL_PRICE_FEED_VALUE, DECIMALS
import pytest
from scripts.deploy import deploy_token_farm_and_sunucash_token, KEPT_BALANCE

def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, sunucash_token = deploy_token_farm_and_sunucash_token()
    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(
        sunucash_token.address, price_feed_address, {"from": account}
    )
    # Assert
    assert token_farm.tokenPriceFeedMapping(sunucash_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
        sunucash_token.address, price_feed_address, {"from": non_owner}
    )
        
def test_stake_tokens(amount_stacked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm, sunucash_token = deploy_token_farm_and_sunucash_token()
    # Act
    sunucash_token.approve(token_farm.address, amount_stacked, {"from": account})
    token_farm.stakeTokens(amount_stacked, sunucash_token.address, {"from": account})
    # Assert
    assert (token_farm.stackingBalance(sunucash_token.address, account.address) == amount_stacked)
    assert token_farm.uniqueTokensStacked(account.address) == 1
    assert token_farm.stackers(0) == account.address
    return token_farm, sunucash_token

def test_issue_tokens(amount_stacked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm, sunucash_token = test_stake_tokens(amount_stacked)
    starting_balance = sunucash_token.balanceOf(account.address)
    end_balance = starting_balance + INITIAL_PRICE_FEED_VALUE

    print(end_balance)
    # Act
    token_farm.issueTokens({"from": account})
    # Assert
    # We are stacking 1 SUNUCASH == in price to 1 ETH
    # So we should got 2000 Sunucash Token in reward
    # Since the price of eth is $2000
    assert (sunucash_token.balanceOf(account.address) == end_balance)

def test_get_user_total_value_with_different_tokens(amount_stacked, random_erc20):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, sunucash_token = test_stake_tokens(amount_stacked)
    # Act
    token_farm.addAllowedTokens(random_erc20.address, {"from": account})
    token_farm.setPriceFeedContract(
        random_erc20.address, get_contract("eth_usd_price_feed"), {"from": account}
    )
    random_erc20_stake_amount = amount_stacked * 2
    random_erc20.approve(
        token_farm.address, random_erc20_stake_amount, {"from": account}
    )
    token_farm.stakeTokens(
        random_erc20_stake_amount, random_erc20.address, {"from": account}
    )
    # Assert
    total_value = token_farm.getUserTotalValue(account.address)
    assert total_value == INITIAL_PRICE_FEED_VALUE * 3

def test_get_token_value():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    token_farm, sunucash_token = deploy_token_farm_and_sunucash_token()
    # Act / Assert
    assert token_farm.getTokenValue(sunucash_token.address) == (
        INITIAL_PRICE_FEED_VALUE,
        DECIMALS,
    )

def test_unstake_tokens(amount_stacked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, sunucash_token = test_stake_tokens(amount_stacked)
    # Act
    token_farm.unstackTokens(sunucash_token.address, {"from": account})
    assert sunucash_token.balanceOf(account.address) == KEPT_BALANCE
    assert token_farm.stackingBalance(sunucash_token.address, account.address) == 0
    assert token_farm.uniqueTokensStacked(account.address) == 0

def test_add_allowed_tokens():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, sunucash_token = deploy_token_farm_and_sunucash_token()
    # Act
    token_farm.addAllowedTokens(sunucash_token.address, {"from": account})
    # Assert
    assert token_farm.allowedTokens(0) == sunucash_token.address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.addAllowedTokens(sunucash_token.address, {"from": non_owner})

def test_token_is_allowed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")

    token_farm, sunucash_token = deploy_token_farm_and_sunucash_token()

    # Assert
    assert token_farm.tokenIsAllowed(sunucash_token.address) == True