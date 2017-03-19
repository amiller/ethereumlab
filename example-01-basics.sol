pragma solidity ^0.4.3;

contract Test {

    int x;
    int y;
    
    mapping ( string => string ) strtest;

    event EventTest(string s);
    function test_function(bytes32 _x) {

	// Logging events
	EventTest("Hello World!");

	// Contract storage
	x = int(_x);

	// Arithmetic
	y = 10 + 1245 * 320; // 398410 = 06144a

	// Mappings
	strtest["Hello"] = "World!";   // "World!" = 0x576f726c6421
    }
    
}
