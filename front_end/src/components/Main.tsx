import { useEthers } from "@usedapp/core"
import HelperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../brownie-config.json"

export const Main = () => {
    // Show token values from the wallet
    // Get the address of different token
    // Get the balance of the user wallet 

    // send the brownie config to the src
    // send the build folder
    const { chainId } = useEthers()
    const networkName = chainId ? HelperConfig[chainId] : "dev"
    console.log(chainId)
    console.log(networkName)

    const sunucashTokenAddress = chainId ? networkMapping[String(chainId)]["SunucashToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
    const daiTokenAddress = chainId ? brownieConfig["networks"][networkName]["dai_token"] : constants.AddressZero



    return (<div>I'm Main </div>)
}