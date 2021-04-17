pragma solidity ^0.7.0;
pragma abicoder v2;

/*
1 - Банк
2 - СтрКмп
3 - ДПС
0 - Юзер
*/

/*
A - 1
B - 2
C - 3
9 - Net prav
*/
contract PDD{
    struct Transport{
        uint category;
        uint price;
        uint yearsold;
    }
    
    struct Driver{
        string fio;
        uint dr_pass;
        uint dr_exp;
        uint dtp;
        uint[] fines;
        uint ins;
    }
    
    struct DriverPass{
        uint deadline;
        uint category;
        address payable owner;
    }
    
    mapping(address => uint) public role;
    mapping(address => Driver) public drivers;
    mapping(uint => DriverPass) public dr_pass;
    mapping(address => string) public auth;
    mapping(address => Transport) public transports;
    
    uint[] void = [0];
    address payable BANK;
    address payable INS;
    address DPS;
    
    constructor(address payable bank, address payable ins, address payable dps, address dr1, address dr2, string memory hs1, string memory hs2, string memory hs3, string memory hs4, string memory hs5){
        
        role[bank] = 1;
        role[ins] = 2;
        role[dps] = 3;
        drivers[dps] = Driver("Ivanov Ivan Ivanovich", 9, 2, 0, void, 0);
        drivers[dr1] = Driver("Semenov Semen Semenovich", 9, 5, 0, void, 0);
        drivers[dr2] = Driver("Petrov Petr Petrovich", 9, 10, 3, void, 0);
        auth[bank] = hs1;
        auth[ins] = hs2;
        auth[dps] = hs3;
        auth[dr1] = hs4;
        auth[dr2] = hs5;
        dr_pass[0] = DriverPass(1610312400, 1, address(0));
        dr_pass[111] = DriverPass(1746997200, 2, address(0));
        dr_pass[222] = DriverPass(1599598800, 3, address(0));
        dr_pass[333] = DriverPass(1802466000, 1, address(0));
        dr_pass[444] = DriverPass(1796936400, 2, address(0));
        dr_pass[555] = DriverPass(1876942800, 3, address(0));
        dr_pass[666] = DriverPass(1901134800, 1, address(0));
        BANK = bank;
        INS = ins;
        DPS = dps;
    }

    
    function registration(string memory _pass_hash, string memory _fio, uint _dr_exp, uint _dtp) public{
        auth[msg.sender] = _pass_hash;
        drivers[msg.sender] = Driver(_fio, 9, _dr_exp, _dtp, void, 0);
    }
    
    function add_dr_pass(uint _number, uint _deadline, uint _category) public{
        require(dr_pass[_number].deadline == _deadline, "Wrong deadline");
        require(dr_pass[_number].category == _category, "Wrong category");
        require(dr_pass[_number].owner == address(0), "Already used");
        require(dr_pass[_number].deadline != 0, "Doesn't exist");
        drivers[msg.sender].dr_pass = _number;
        dr_pass[_number].owner = msg.sender;
    }
    
    function reg_transport(uint _category, uint _price, uint _yearsold) public{
        uint pass = drivers[msg.sender].dr_pass;
        require(dr_pass[pass].category == _category, "Wrong category");
        transports[msg.sender] = Transport(_category, _price, _yearsold);
    }
    
    function prolong_dr_pass() public{
        Driver memory dr = drivers[msg.sender];
        require(block.timestamp + 30*24*60*60 <= dr_pass[dr.dr_pass].deadline);
        require(dr.fines.length == 0, "You have fines");
        dr_pass[dr.dr_pass].deadline += 365 days;
    }
    
    function pay_fines(uint _id) public payable{
        uint to_pay = 10 ether;
        if (block.timestamp <= drivers[msg.sender].fines[_id] + 5 days){
            to_pay = 5 ether;
        }
        require(msg.value == to_pay, "Not enough money");
        BANK.transfer(msg.value);
    }
    
    function reg_ins() public payable{
        INS.transfer(msg.value);
        drivers[msg.sender].ins = msg.value;
    }
    
    function reg_fine(uint _num_dr_pass) public{
        require(role[msg.sender] == 3, "You aren't dpsman");
        drivers[dr_pass[_num_dr_pass].owner].fines.push(block.timestamp);
    }
    
    function reg_dtp(uint _num_dr_pass) public{
        require(role[msg.sender] == 3, "You aren't dpsman");
        drivers[dr_pass[_num_dr_pass].owner].dtp += 1;
    }
    
    function pay_compens(uint _num_dr_pass) public{
        require(role[msg.sender] == 2, "You aren't Ins company");
        if  (drivers[dr_pass[_num_dr_pass].owner].ins > 0){
            dr_pass[_num_dr_pass].owner.transfer(drivers[dr_pass[_num_dr_pass].owner].ins * 10);
        }
    }
    
    function get_driver(address user) public view returns(Driver memory){
        return drivers[user];
    }
}

