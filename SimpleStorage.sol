// Defining the version of solidity that our program will use
// pragma solidity >= 0.6.0 < 0.9.0;

// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    //uint256 favoriteNumber = 5;
    //bool favoriteBool = false;
    //string favoriteString = "String";
    //int256 favoriteInt = -5;
    //address favoriteAddress = 0xFe63c8dE1b9A79E4EA5c740F4bFe62ADFb26dc8B;
    //bytes32 favoriteBytes = "cat";
    //uint256 public favoriteNumber; // If we not assigned any value to a variable it will automatically initialised with value = 0;
    uint256 favoriteNumber;
    bool favoriteBool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //People public person = People({favoriteNumber: 2, name: "Sumit"});

    People[] public people; // This type of array is called dynamic array because we can change its size
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber; // also use and learn about "external", "internal", "private" keywords
    }

    // learn about "view", "pure" keyword as we don't make transaction on them
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
        //function retrieve(uint256 favoriteNumber) public pure {
        //    favoriteNumber + favoriteNumber;  }
    }

    // learn about "storage"(i.e like Hard Disk storage stored even after the function executed) and "memory" (i.e RAM storage) keyword there is a very slight difference
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name)); // As People() is once written so we don't have to write it again as whole
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
