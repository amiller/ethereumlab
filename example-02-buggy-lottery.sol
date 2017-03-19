pragma solidity ^0.4.3;

contract Lottery {

    event Notice(string s);

    address alice = 0x{##alice##};
    address bob = 0x{##bob##};

    mapping (address => bool) hasPaid;

    function load_money() payable {
	// Must pay before time #1
	if (block.number > 1) { 
	    Notice("load_money: called after block 1");
	    return;
	}

	if (msg.value != 10*(10**21)) {
	    Notice("load_money: wrong amount");
	    return;
	}

	if (msg.sender == alice) {
	    Notice("load_money: Alice's deposit is OK");
	}
	
	if (msg.sender == bob) {
	    Notice("load_money: Bob's deposit is OK");
	}

	// Mark user as having paid
	hasPaid[msg.sender] = true;
    }

    function cash_out() {
	// Critical block is #2
	// Must wait for block #3 to cash out
	if (block.number < 3) {
	    Notice("cash_out: called before block 3");
	    return;
	}
	
	if (!hasPaid[alice]) {
	    Notice("cash_out: Alice didn't pay!");
	    bob.send(this.balance);
	    return;
	}

	if (!hasPaid[bob]) {
	    Notice("cash_out: Bob didn't pay!");
	    alice.send(this.balance);
	    return;
	}

	var block2 = block.blockhash(block.number - 2);
	if (int256(block2) % 2 == 0) {
	    Notice("cash_out: Alice won!");
	    alice.send(this.balance);
	} else {
	    Notice("cash_out: Bob won!");
	    bob.send(this.balance);
	}
    }
}
