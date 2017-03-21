from ethereum import tester
from ethereum import utils
from ethereum import slogging
import rlp

file_chunks = [
 "A  purely peer-to-peer",
 "version of electronic",
 "cash would allow online",
 "payments to be sent directly",
 "from one party to another",
 "without going through a",
 "financial institution.",
 "Digital signatures provide",
 "part of the solution, but",
 "the main benefits are lost",
 "if a trusted third party",
 "is still required to prevent",
 "double-spending. We propose",
 "a solution to the double",
 "-spending problem using a",
 "peer-to-peer network."]

zfill = lambda s: (32-len(s))*'\x00' + s
file_chunks = map(zfill, file_chunks)

contract_code = """
contract MerkleTree {
   bytes32 root = 0x{##ROOT##};

   function hash_node(bytes32 h, bytes32 sibling, uint8 bit) internal constant returns(bytes32) {
       if (bit == 0)
           return sha3(h, sibling);
       else
           return sha3(sibling, h);
    }

    function check_index(bytes32 x, uint8[4] bits, bytes32[4] siblings) returns(bool) {
        bytes32 h;
        h = hash_node(x, siblings[0], bits[0]);
        h = hash_node(h, siblings[1], bits[1]);
        h = hash_node(h, siblings[2], bits[2]);
        h = hash_node(h, siblings[3], bits[3]);
        if (h == root)
            return true;
        else
            return false;
    }
}
"""

# Build the merkle tree
layer_1 = [utils.sha3(file_chunks[2*i+0] + file_chunks[2*i+1])
           for i in range(8)]
layer_2 = [utils.sha3(layer_1[2*i+0] + layer_1[2*i+1])
           for i in range(4)]
layer_3 = [utils.sha3(layer_2[2*i+0] + layer_2[2*i+1])
           for i in range(2)]
root_hash = utils.sha3(layer_3[0] + layer_3[1])


def index_to_bits(ind):
    bits = []
    for i in range(4):
        bits.append(ind % 2)
        ind /= 2
    return bits

def get_siblings(bits):
    assert len(bits) == 4
    if bits[3] == 0: sibling3 = layer_3[1]
    else: sibling3 = layer_3[0]

    offset = bits[3]*2
    if bits[2] == 0: sibling2 = layer_2[offset+1]
    else: sibling2 = layer_2[offset]

    offset = 2*offset + bits[2]*2
    if bits[1] == 0: sibling1 = layer_1[offset+1]
    else: sibling1 = layer_1[offset]

    offset = 2*offset + bits[1]*2
    if bits[0] == 0: sibling0 = file_chunks[offset+1]
    else: sibling0 = file_chunks[offset]

    return [sibling0, sibling1, sibling2, sibling3]

s = tester.state()
c = s.abi_contract(contract_code.replace("{##ROOT##}", root_hash.encode('hex')),
                   language='solidity')

def test_index(ind):
    bits = index_to_bits(ind)
    chunk = file_chunks[ind]
    siblings = get_siblings(bits)
    outcome = c.check_index(chunk, bits, siblings)
    print bits, chunk, siblings
    assert outcome == True

test_index(0)
test_index(1)
test_index(11)
