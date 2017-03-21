from ethereum import tester, utils
import bitcoin
import os

contract_code = """
pragma solidity ^0.4.3;

contract Micropayment {

    event Notice(string x);

    address alice;
    address bob;
    uint deadline;

    function verifySignature(address pub, bytes32 h, uint8 v, bytes32 r, bytes32 s) returns(bool) {
        if (pub != ecrecover(h,v,r,s)) return false;
        return true;
    }

    function deposit() payable {}

    function Micropayment(address _bob) {
        // Constructor: initialize variables
        alice = msg.sender;
        bob = _bob;
        deadline = block.number + 10;
    }

    function refund() {
        if (msg.sender != alice) {
            Notice("refund called by other-than-Alice");
            return;
        }

        if (block.number < deadline) {
            Notice("Too soon for Alice to claim refund");
            return;
        }
        alice.send(this.balance);
    }

    function finalize(uint[3] sig, uint amount) {
        if (msg.sender != bob) {
            Notice("finalize called by other-than-Bob");
            return;
        }
        var h = sha3(amount);
        if (!verifySignature(alice, h, uint8(sig[0]), bytes32(sig[1]), bytes32(sig[2]))) {
            Notice("bad signature!");
            return;
        }

        bob.send(amount);
        alice.send(this.balance);
    } 
}
"""

s = tester.state()

# Use default addresses for Alice and Bob
alice = tester.a0
bob = tester.a1

print 'Initial balances:'
print 'Alice: %.2f' % (float(s.block.get_balance(alice)) / 10E21)
print '  Bob: %.2f' % (float(s.block.get_balance(bob)) / 10E21)

# Create the contract (Initialized by Alice)
contract = s.abi_contract(contract_code, language='solidity', constructor_parameters=(bob,), sender=tester.k0)


# Alice deposits 30 eth
contract.deposit(value=int(30*10E21), sender=tester.k0)

# zfill: left-pads a string with 0's until 32 bytes
zfill = lambda s: (32-len(s))*'\x00' + s


s.mine(10)
print 'After Deposit Balances:'
print 'Alice: %.2f' % (float(s.block.get_balance(alice)) / 10E21)
print '  Bob: %.2f' % (float(s.block.get_balance(bob)) / 10E21)
print 'Contract: %.2f' % ( float(s.block.get_balance(contract.address)) / 10E21 )

# The payment signature
def sigamt(amount, priv=tester.k0):
   amount = utils.int_to_bytes(amount)
   amount = zfill(amount)
   pub = bitcoin.privtopub(priv)
   amthash = utils.sha3(amount)
   V, R, S = bitcoin.ecdsa_raw_sign(amthash, priv)
   assert bitcoin.ecdsa_raw_verify(amthash, (V,R,S), pub)
   return V,R,S

# first payment
pay5 = sigamt(int(5*10E21))

# second payment
pay10 = sigamt(int(10*10E21))

# Bob calls finalize
V,R,S = pay10
fval = int(10*10E21)
contract.finalize((V,R,S), fval, sender=tester.k1)

s.mine(10)
# Alice calls refund
#contract.refund(sender=tester.k0)


print 'Finalized Balanced:'
print 'Alice: %.2f' % (float(s.block.get_balance(alice)) / 10E21)
print '  Bob: %.2f' % (float(s.block.get_balance(bob)) / 10E21)
print 'Contract: %.2f' % ( float(s.block.get_balance(contract.address)) / 10E21 )
