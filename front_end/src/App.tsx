import React from 'react';

import { DAppProvider, ChainId } from '@usedapp/core';

import { Header } from "./components/Header";

import { Container } from "@material-ui/core";

import { Main } from './components/Main';


function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Sepolia, ChainId.Localhost, ChainId.Rinkeby],
    }}>
      <Header></Header>
      <Container maxWidth="md">
        <div>Hi</div>
        <Main/>
      </Container>
    </DAppProvider>
    
  );
}

export default App;
