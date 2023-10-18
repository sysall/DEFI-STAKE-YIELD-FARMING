import { useEthers } from "@usedapp/core"
import HelperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../brownie-config.json"
import dapp from "../dapp.png"
import eth from "../eth.png"
import dai from "../dai.png"
import { YourWallet } from "./yourWallet"
import { makeStyles } from "@material-ui/core"

export type Token = {
    image: string
    address: string
    name: string
}

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)
    }
}))

export const Main = () => {
    // Show token values from the wallet
    // Get the address of different token
    // Get the balance of the user wallet 

    // send the brownie config to the src
    // send the build folder
    const classes = useStyles()
    const { chainId } = useEthers()
    const networkName = chainId ? HelperConfig[chainId] : "dev"
    console.log(chainId)
    console.log(networkName)
    const sunucashTokenAddress = chainId ? networkMapping[String(chainId)]["SunucashToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
    const daiTokenAddress = chainId ? brownieConfig["networks"][networkName]["dai_token"] : constants.AddressZero

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: sunucashTokenAddress,
            name: "SUNUCASH"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dai,
            address: daiTokenAddress,
            name: "DAI"
        }
    ]

    return (<>
        <h2 className={classes.title}>Sunucash Token App</h2>
        <YourWallet supportedTokens={supportedTokens} />
    </>)


}