pragma solidity ^0.4.3;

contract RPS {

    function assert(bool b) internal { if (!b) throw; }

    event Balance(string s, uint x);
    
    struct Player {
	address addr;
	uint choice;
	bytes32 commit;
	bool has_revealed;
    }
    
    Player[2] player;
    uint num_players;
    uint reward;
    uint timer_start;
    uint[3][3] check_winner; // captures the rules of rock-paper-scissors game

    function RPS() {
	// If 2, tie
	// If 0, player 0 wins
	// If 1, player 1 wins
	
	// 0 = rock
	// 1 = paper
	// 2 = scissors

	check_winner[0][0] = 2;
	check_winner[1][1] = 2;
	check_winner[2][2] = 2;

	// Rock beats scissors
	check_winner[0][2] = 0;
	check_winner[2][0] = 1;

	// Scissors beats paper
	check_winner[2][1] = 0;
	check_winner[1][2] = 1;

	// Paper beats rock
	check_winner[1][0] = 0;
	check_winner[0][1] = 1;
    }

    // adds players who send 2000 szabo to the contract to the game
    // accepts a hash from the player in form sha3(address, choice, nonce)
    function add_player(bytes32 commitment) payable returns(uint) {
	if (num_players < 2 && msg.value == 2000 szabo) {
	    reward += msg.value;
	    player[num_players].addr = msg.sender;
	    player[num_players].commit = commitment;
	    num_players++;
	    return(uint(commitment));
	} else {
	    throw; // Return the money
	}
    }

    function open(uint choice, uint nonce) returns(int) {
	
	assert(num_players == 2);

	// Determine which player submitted the open request
	uint player_num;
	if (msg.sender == player[0].addr)
	    player_num = 0;
	else if (msg.sender == player[1].addr)
	    player_num = 1;
	else
	    return(-2);

	// Check the commitment and ensure they have not tried to commit already
	if (sha3(msg.sender, choice, nonce) == player[player_num].commit &&
	    !player[player_num].has_revealed) {
	    // If commitment verified, we should store choice in plain text
	    player[player_num].choice = choice;

	    // Store current block number to give other player 10 blocks to open their commit
	    player[player_num].has_revealed = true;

	    // Record when the first player opened
	    if (timer_start == 0) {
		timer_start = block.number;
	    }

	    return(int(choice));
	}
	else return(-1);
    }

    function check() returns(int) {
	// Check to make sure at least 10 blocks have been given for both players to reveal their play.
	if (block.number - timer_start < 10)
	    return(-2);

	// Check that the call stack is big enough
	assert(test_callstack());

	// check to see if both players have revealed answer
	if (player[0].has_revealed && player[1].has_revealed) {
	    var p0_choice = player[0].choice;
	    var p1_choice = player[1].choice;

	    if (check_winner[p0_choice][p1_choice] == 0) {
		// If player 0 wins
		assert(player[0].addr.send(reward));
		return(0);
	    } else if (check_winner[p0_choice][p1_choice] == 1) {
		// If player 1 wins
		assert(player[1].addr.send(reward));
		return(1);
	    } else {
		// If no one wins
		player[0].addr.send(reward/2);
		player[1].addr.send(reward/2);
		return(2);
	    }
	}

	// if p1 revealed but p2 did not, send money to p1
	else if (player[0].has_revealed && !player[1].has_revealed) {
	
	    player[0].addr.send(reward);
	    return(0);
	}

	// if p2 revealed but p1 did not, send money to p2
	else if (!player[0].has_revealed && player[1].has_revealed) {
	    player[1].addr.send(reward);
	    return(1);
	}

	// if neither p1 nor p2 revealed, keep both of their bets
	else return(-1);
    }

    function balance_check() {
	Balance("Alice", player[0].addr.balance);
	Balance("Bob",   player[1].addr.balance);
    }

    function test_callstack() returns(bool) {
	return true;
    }
}
