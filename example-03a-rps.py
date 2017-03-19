import serpent
from ethereum import tester, utils, abi

contract_code = open('rpsA.sol').read()

s = tester.state()
c = s.abi_contract(contract_code, language='solidity')

import random

codes = {0: "Rock", 1: "Paper", 2: "Scissors", -1: "#ERR"}

o = c.add_player(random.randint(0,2),value=int(2000E12), sender=tester.k1)
print("Player 1 Added: {}").format(codes[o])

o = c.add_player(random.randint(0,2),value=int(2000E12), sender=tester.k2)
print("Player 2 Added: {}").format(codes[o])

# Edge case example: what happens if a 3rd player joins?
#o = c.add_player(random.randint(0,2),value=1000,sender=tester.k2)
#print("Player 3 Added: {}").format(codes[o])

o = c.check(sender=tester.k0)
print
if o == 2: print('Tied!')
elif o == 0: print("Alice won!")
elif o == 1: print("Bob won!")

c.balance_check(sender=tester.k1)
print "Remaining contract balance:", s.block.get_balance(c.address)
