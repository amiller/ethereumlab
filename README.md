Course materials for the March 2017 Programming Project
=========
Basic resources on Solidity and smart contract programming security:
- [(Ethereum Lab [serpent based])](http://mc2-umd.github.io/ethereumlab/)
- [(Solidity Reference Documentation)](https://solidity.readthedocs.io/)
- [(Solidity Tutorial)](https://solidity.readthedocs.io/en/develop/solidity-by-example.html)
- [(Solidity Wiki)](https://github.com/ethereum/wiki/wiki/Solidity)


Virtual Machine
---
See the COURSE LIVE DOCUMENT for notes on using your virtual machine. Pyethereum and Solidity are already preinstalled
- pip install ipython

Resources in this directory:
--
   - [example-01-basics.py](example-01-basics.py) :
      Illustrates the use of the pyethereum.tester" simulation framework, along with useful idioms for printing the state of a contract, setting debug logs, and basic Serpent use
   - [example-02-buggy-lottery.py](example-02-buggy-lottery.py):
      A simple gambling game for 2 players, based on the block number. (Actually it's an example of several pitfalls, like those discussed in class)
   - [example-03a-rps.py](example-03a-rps.py):
      A Rock Paper Scissors game, also with several pitfalls
   - [example-03c-rps.py](example-03c-rps.py):
      A robustified version of the Rock Paper Scissors game
   - [example-04-micropayments.py](example-04-micropayments.py):
      A simple payment channel. Actually a useful smart contract for fast off-chain payments. Great starting point for learning about Lightning network, "State Channels", etc. Also provides idioms for verifying signatures and checking hashes, illustrates the use of Serpent macros
   - [example-05-merkletree.py](example-05-merkletree.py):
      Merkle tree example - The on-chain contract just stores the root hash of a dataset. The contract can verify a Merkle Tree proof that a particular element exists at a given element in the dataset. Starting point for a "decentralized file storage" application
   - [solidity-merkletree.py](solidity-merkletree.py):
      pyethereum also works with Solidity
   - [serpent_extern.py](serpent_extern.py):
     Illustrates how to call one contract from another



What next?
---
Roughly, the instructions for the lab assignment are "build something cool in the next 3 hours."