from ethereum import tester

# Logging
from ethereum import slogging
slogging.configure(':INFO')
#slogging.configure(':DEBUG')
#slogging.configure(':DEBUG,eth.vm:TRACE')

# Serpent code
contractA_code = """
event Notice(s:str, x:uint256)

extern contractA: [doubler:[int256]:int256]

def printer(a:address, x):
   log(type=Notice, text("x:"), x)
   log(type=Notice, text("2x:"), a.doubler(x))
"""

contractB_code = """
def doubler(x):
   return (2*x)
"""

s = tester.state()

# Create the contract
import serpent
print serpent.mk_signature(contractA_code)
print serpent.mk_signature(contractB_code)
contractA = s.abi_contract(contractA_code)
contractB = s.abi_contract(contractB_code)

contractA.printer(contractB.address, 10)
