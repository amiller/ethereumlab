pragma solidity ^0.4.3;

contract RPS {
    event Balance(string s, uint x);
    
    struct Player {
	address addr;
	uint choice;
    }
    
    Player[2] player;
    uint num_players;
    uint reward;
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
    function add_player(uint choice) payable returns(int) {
	if (num_players < 2 && msg.value >= 2000 szabo) {
	    reward += msg.value;
	    player[num_players].addr = msg.sender;
	    player[num_players].choice = choice;
	    num_players++;
	    return(int(choice));
	} else {
	    return(-1);
	}
    }


    function check() returns(int) {
	var p0_choice = player[0].choice;
	var p1_choice = player[1].choice;
	// If player 0 wins
	if (check_winner[p0_choice][p1_choice] == 0) {
	    player[0].addr.send(reward);
	    return(0);
	}
	// If player 1 wins
	else if (check_winner[p0_choice][p1_choice] == 1) {
	    player[1].addr.send(reward);
	    return(1);
	}
	// If no one wins
	else {
	    player[0].addr.send(reward/2);
	    player[1].addr.send(reward/2);
	    return(2);
	}
    }

    function balance_check() {
	Balance("Alice", player[0].addr.balance);
	Balance("Bob",   player[1].addr.balance);
    }
}
