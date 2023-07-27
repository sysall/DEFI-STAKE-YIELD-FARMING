// SPDX-Licence-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV2V3Interface.sol";

contract TokenFarm is Ownable{
    // mapping token address -> staker address -> amount
    mapping(address => mapping(address => uint256)) public stackingBalance;
    mapping(address => uint256) public uniqueTokensStacked;
    mapping(address => address) public tokenPriceFeedMapping;

    address [] public stackers;
    address [] public allowedTokens;
    IERC20 public sunucashToken;

    constructor(address _sunucashTokenAddress) public {
        sunucashToken = IERC20(_sunucashTokenAddress);
    }

    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner{
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    function addAllowedTokens(address _token) public onlyOwner{
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public view returns (bool) {
        for( uint256 allowedTokensIndex=0; allowedTokensIndex < allowedTokens.length; allowedTokensIndex++){
            if(allowedTokens[allowedTokensIndex] == _token){
                return true;
            }
        }
        return false;

    }

    function updateUniqueTokensStacked(address _user, address _token) internal {
        if(stackingBalance[_token][_user] <= 0) {
            uniqueTokensStacked[_user] = uniqueTokensStacked[_user] + 1;
        }
    }

    function getUserTotalValue(address _user) public view returns (uint256){
        uint256 totalValue = 0;
        require(uniqueTokensStacked[_user] > 0, "No Tokens staked!");
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ){
            totalValue = totalValue + getUserSingleTokenValue(_user,allowedTokens[allowedTokensIndex]);
        }
        
        return totalValue;

    }

    function getUserSingleTokenValue(address _user, address _token) public view returns (uint256){
        if (uniqueTokensStacked[_user] <= 0){
            return 0;
        }
        // price of the token * stackingBalance[_token][user]
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return (stackingBalance[_token][_user] * price / (10**decimals));

    }

    function getTokenValue(address _token) public view returns (uint256, uint256) {
        // PriceFeedAddress
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (,int256 price,,,) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowed(_token), "Token is currently not allowed!");
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        // check how many stacked token the user have
        updateUniqueTokensStacked(msg.sender, _token);
        stackingBalance[_token][msg.sender] = stackingBalance[_token][msg.sender] + _amount;
        if (uniqueTokensStacked[msg.sender] == 1){
            stackers.push(msg.sender);
        }

    }


    // reward user : example 100 ETH 1/1 for every 1 ETH we give 1 SunucashToken
    // 50 ETH and 50 DAI stacked and  we want to give a reward of 1 SUNUCASH / 1 DAI
    function issueTokens() public onlyOwner {
        // Issue tokens to all stakers
        for (
            uint256 stackersIndex = 0;
            stackersIndex < stackers.length;
            stackersIndex++
        ){
            address recipient = stackers[stackersIndex];
            uint256 userTotalValue = getUserTotalValue(recipient);
            // send them a token reward based on their total value locked
            sunucashToken.transfer(recipient, userTotalValue);
        }

    }

    function unstackTokens(address _token) public {
        uint256 balance = stackingBalance[_token][msg.sender];
        require(balance > 0, "Stacking balance cannot be 0");
        IERC20(_token).transfer(msg.sender, balance);
        stackingBalance[_token][msg.sender] = 0;
        uniqueTokensStacked[msg.sender] = uniqueTokensStacked[msg.sender] - 1;
    }

}