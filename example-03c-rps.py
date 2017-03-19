import serpent
from ethereum import tester, utils, abi
from sha3 import sha3_256
import sys
import struct
import binascii
import random

contract_code = open('rpsC.sol').read()

s = tester.state()
c = s.abi_contract(contract_code, language='solidity')

print("Output of 1 designated success for player 1.")
print("Output of 2 designated success for player 2.")
print("Output of 0 designated a tie.\n")
print("Output of -1 designated an error.\n")

##################################### SETUP COMMITMENTS ########################################
choice = ["rock", "paper", "scissors"]

# Use default addresses for Alice and Bob
alice = tester.a1
alice_key = tester.k1
bob = tester.a2
bob_key = tester.k2

tobytearr = lambda n, L: [] if L == 0 else tobytearr(n / 256, L - 1)+[n % 256]
zfill = lambda s: (32-len(s))*'\x00' + s

choice1 = random.randint(0,2)
nonce1 = random.randint(0,2**256-1)
ch1 = ''.join(map(chr, tobytearr(choice1, 32)))
no1 = ''.join(map(chr, tobytearr(nonce1, 32)))
print("Alice chooses {} which is: {}").format(choice1, choice[choice1])



## Use Alice's address for the commitment
s1 = ''.join([alice, ch1, no1])
comm1 = utils.sha3(s1)

choice2 = random.randint(0,2)
nonce2 = random.randint(0,2**256-1)
ch2 = ''.join(map(chr, tobytearr(choice2, 32)))
no2 = ''.join(map(chr, tobytearr(nonce2, 32)))
print("Bob chooses {} which is: {}\n").format(choice2, choice[choice2])


## Use Bob's address for the commitment
s2 = ''.join([bob, ch2, no2])
comm2 = utils.sha3(s2)

print 'Alice\'s nonce:', no1.encode('hex')
print 'Alice\'s choice:', ch1.encode('hex')
print 'Alice\'s commitment:', comm1.encode('hex')

print 'Bob\'s nonce:', no2.encode('hex')
print 'Bob\'s choice:', ch2.encode('hex')
print 'Bob\'s commitment:', comm2.encode('hex')

o = c.add_player(comm1, value=int(2000E12), sender=alice_key)
print("Alice Added: {}").format(o)

o = c.add_player(comm2, value=int(2000E12), sender=bob_key)
print("Bob Added: {}\n").format(o)

codes = {0: "Rock", 1: "Paper", 2: "Scissors", -1: "#ERR"}

o = c.open(choice1, no1, sender=alice_key)
print("Open for Alice: {}").format(o)

o = c.open(choice2, no2, sender=bob_key)
print("Open for Bob: {}\n").format(o)

s.mine(11) # needed to move the blockchain at least 10 blocks so check can run

o = c.check(sender=tester.k0)
if o == 2: print('Tied!')
elif o == 0: print("Alice won!")
elif o == 1: print("Bob won!")

c.balance_check(sender=tester.k0)
#print "Remaining contract balance:", s.block.get_balance(c.address)
