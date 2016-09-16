Course materials for the ECE598AM Fall 2016 programming project
=========

Get the docker image with `docker pull socrates1024/ece598am:fall2016`

Resources in this directory:
--
   - ./example-01-basics.py
      Illustrates the use of the pyethereum.tester" simulation framework, along with useful idioms for printing the state of a contract, setting debug logs, and basic Serpent use
   - ./example-02-buggy-lottery.py
      A simple gambling game for 2 players, based on the block number. (Actually it's an example of several pitfalls, like those discussed in class)
   - ./example-03a-rps.py:
      A Rock Paper Scissors game, also with several pitfalls
   - ./example-03c-rps.py:
      A robustified version of the Rock Paper Scissors game
   - ./example-04-micropayments.py:
      A simple payment channel. Actually a useful smart contract for fast off-chain payments. Great starting point for learning about Lightning network, "State Channels", etc. Also provides idioms for verifying signatures and checking hashes, illustrates the use of Serpent macros
   - ./example-05-merkletree.py:
      Merkle tree example - The on-chain contract just stores the root hash of a dataset. The contract can verify a Merkle Tree proof that a particular element exists at a given element in the dataset. Starting point for a "decentralized file storage" application
   - ./solidity-merkletree.py:
      pyethereum also works with Solidity
   - ./serpent_extern.py:
     Illustrates how to call one contract from another

Building from ./Dockerfile
--
```
sudo docker build -t "ece598:dockerfile" ./
sudo docker run --name testinstance -it ece598:dockerfile
sudo docker start testinstance
sudo docker attach testinstance
```

