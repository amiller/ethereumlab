from ethereum import tester
from ethereum import slogging
import os

#contract_code = """
#"""

s = tester.state()

# Use default addresses for Alice and Bob
alice = tester.a0
bob   = tester.a1

print 'Initial balances:'
print 'Alice: %.2f' % (float(s.block.get_balance(alice)) / 10E21)
print '  Bob: %.2f' % (float(s.block.get_balance(bob)) / 10E21)

# Create the contract
contract_code = open('example-02-buggy-lottery.sol').read()
contract_code = contract_code.replace('{##alice##}', alice.encode('hex'))
contract_code = contract_code.replace(  '{##bob##}',   bob.encode('hex'))

contract = s.abi_contract(contract_code, language='solidity')

# Both parties deposit money
contract.load_money(value=int(10E21), sender=tester.k0) # Alice
contract.load_money(value=int(10E21), sender=tester.k1) # Bob

# Mine some blocks
s.block.extra_data = os.urandom(20) # Add actual randomness
s.mine(3)

# Run the cash_out 
contract.cash_out()

print 'Final balances:'
print 'Alice: %.2f' % (float(s.block.get_balance(alice)) / 10E21)
print '  Bob: %.2f' % (float(s.block.get_balance(bob)) / 10E21)
