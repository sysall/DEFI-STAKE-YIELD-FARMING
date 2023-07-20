from brownie import network, config, accounts, MockV3Aggregator, Contract, LinkToken, MockDAI, MockWETH

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONNEMENTS = ["mainnet-fork","mainnet-fork-dev"]

def get_account(index=None, id=None):
    if id:
        return accounts.load(id)
    
    if index:
        return accounts[index]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONNEMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "dai_token": MockDAI,
    "weth_token": MockWETH,
}

def get_contract(contract_name):
    """This functionn will grap the contract addresses from the brownie config if defined,
    otherwise, it will deploy a mock version of that contract, and return that mock contract.

        Args:
            contract_name(string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of this contract.

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type, contract_address,contract_type.abi)
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000
def deploy_mocks(decimals = DECIMALS, initial_value = INITIAL_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock DAI...")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed to {dai_token.address}")
    print("Deploying Mock WETH")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed to {weth_token.address}")

def issue_tokens():
    """
        This function will:
            - Print your account address and deployed TokenFarm contract address to confirm that you're using the right ones
            - Call issueTokens on your deployed TokenFarm contract to issue the DAPP token reward to your users
    """
    account = get_account()
    print(f"Issue Tokens called by: {account}")
    token_farm = get_contract("TokenFarm")
    print(f"TokenFarm contract called to issue tokens: {token_farm}")
    tx = token_farm.issueTokens({"from": account})
    tx.wait(1)