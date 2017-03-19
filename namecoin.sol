pragma solidity ^0.4.3;

contract Namecoin {
    mapping (bytes32 => bytes32) domainMap;
    function register(bytes32 k, bytes32 v) returns(bool) {
	if (domainMap[k] == 0) {
	    // Take it!
	    domainMap[k] = v;
	    return(true);
	}
	return false;
    }
}
