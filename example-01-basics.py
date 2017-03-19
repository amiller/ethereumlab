from ethereum import tester
from ethereum import utils
from ethereum._solidity import get_solidity
SOLIDITY_AVAILABLE = get_solidity() is not None

# Logging
from ethereum import slogging
slogging.configure(':INFO,eth.vm:INFO')
#slogging.configure(':DEBUG')
#slogging.configure(':DEBUG,eth.vm:TRACE')

# Serpent code
contract_code = """
contract Test {
    int x;
    int y;
    mapping ( string => string ) strtest;
    event EventTest(string s);
    function test_function(bytes32 _x) {
	EventTest("Hello World!");
	x = _x;
    }
}
"""


s = tester.state()

# Create the contract
contract_code = open('example-01-basics.sol').read()
contract = s.abi_contract(contract_code, language='solidity')

# Invoke a method (in the local "mempool", to go in the next block)
contract.test_function("C0FFEEBABE".decode('hex'))

# Mine blocks
s.mine(10)

# Inspect the contract storage
def simplify_trie(trie):
    return dict((k.encode('hex'), v[1:].encode('hex')) 
                for k,v in trie.to_dict().iteritems())

for k,v in simplify_trie(s.block.get_storage(contract.address)).iteritems():
    print k,v

# Print the balance of Alice
#print "[1] Alice' balance", s.block.get_balance(alice)
#s.send(tester.k0, contract.address, 1)
#print "[2] Alice' balance", s.block.get_balance(alice)


# Look at compiled code
# print serpent.pretty_compile(contract_code)

# Look at intermediate LLL language
# print serpent.pretty_compile(contract_code)
