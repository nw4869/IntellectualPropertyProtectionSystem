pragma solidity ^0.4.11;

contract HashProof {

    struct AuthorizationLog {
        address user;
        uint256 timestamp;
    }

    struct PurchaseLog {
        address user;
        uint price;
        uint256 timestamp;
    }

    struct OwnerLog {
        address user;
        uint256 timestamp;
    }

    struct Proof {
        string name;
        string  description;
        uint256 timestamp;
        address owner;
        bool forSell;
        uint price;
        PurchaseLog[] purchases;
        AuthorizationLog[] authorizations;
        OwnerLog[] owenerLogs;
    }

    mapping(bytes32 => Proof) public proofs;


    function proof(bytes32 hash, string name, string description, bool forSell,
                    uint price, address owner) {
        require(!isExisting(hash));

        proofs[hash].name = name;
        proofs[hash].description = description;
        proofs[hash].timestamp = block.timestamp;
        address theOwner = owner;
        if (theOwner == 0) {
            theOwner = msg.sender;
        }
        proofs[hash].owner = theOwner;
        proofs[hash].forSell = forSell;
        proofs[hash].price = price;

        proofs[hash].owenerLogs.push(OwnerLog({
            user: theOwner,
            timestamp: block.timestamp
        }));
    }

    function proof(bytes32 hash, string name, string description) {
        proof(hash, name, description, false, 0, 0);
    }

    function proof(bytes32 hash, string name, string description, address owner) {
        proof(hash, name, description, false, 0, owner);
    }


    function proof(bytes32 hash, string name, string description, uint price) {
        proof(hash, name, description, true, price, 0);
    }


    function proof(bytes32 hash, string name, string description, uint price, address owner) {
        proof(hash, name, description, true, price, owner);
    }

    function purchase(bytes32 hash) payable {
        purchase(hash, 0);
    }

    function purchase(bytes32 hash, address user) payable {
        if (!isForSell(hash)) throw;

        address theUser = user;
        if (theUser == 0) {
            theUser = msg.sender;
        }

        if (getProofOwner(hash) == theUser) throw;

        PurchaseLog[] purchaseLogs = proofs[hash].purchases;
        for (uint i = 0; i < purchaseLogs.length; i++) {
            if (purchaseLogs[i].user == theUser) throw;
        }

        uint price = getPrice(hash);
        if (price > msg.value) throw;


        proofs[hash].purchases.push(PurchaseLog({
            user: theUser,
            timestamp: block.timestamp,
            price: price
        }));
        proofs[hash].owner.transfer(price);
    }

    function transfer(bytes32 hash, address user) {
        address owner = getProofOwner(hash);
        if (owner != msg.sender || owner == user) throw;

        proofs[hash].owenerLogs.push(OwnerLog({
            user: owner,
            timestamp: block.timestamp
        }));

        proofs[hash].owner = user;
    }

    function authorize(bytes32 hash, address user) {
        address owner = getProofOwner(hash);
        if (owner != msg.sender || owner == user) throw;

        AuthorizationLog[] authorizations = proofs[hash].authorizations;
        for (uint i = 0; i < authorizations.length; i++) {
            if (authorizations[i].user == user) throw;
        }

        authorizations.push(AuthorizationLog({
            user: owner,
            timestamp: block.timestamp
        }));
    }

    uint a;
    function test() {
        require(msg.sender != 0);
        a = 1;
    }

    function testException() {
        throw;
    }

    function isExisting(bytes32 hash) constant returns (bool) {
        return getProofTimestamp(hash) > 0;
    }

    function getProofTimestamp(bytes32 hash) constant returns (uint256) {
        return proofs[hash].timestamp;
    }

    function getProofName(bytes32 hash) constant returns (string) {
        return proofs[hash].name;
    }

    function getProofDescription(bytes32 hash) constant returns (string) {
        return proofs[hash].description;
    }

    function getProofOwner(bytes32 hash) constant returns (address) {
        return proofs[hash].owner;
    }

    function isForSell(bytes32 hash) constant returns (bool) {
        return proofs[hash].forSell;
    }

    function getPrice(bytes32 hash) constant returns (uint) {
        return proofs[hash].price;
    }

    function add(int a, int b) constant returns (int) {
        return a + b;
    }
}