pragma solidity >=0.7.0 <=0.8.0;
pragma abicoder v2;

/*
    1 - Государственный банк
    2 - Страховая компания
    3 - Сотрудник ДПС
*/

contract PDD{
    struct Transport{
        string category;
        uint price;
        uint age;
    }
    
    struct Driver{
        string fio;
        uint d_exp;
        uint dtp;
        uint[] fines;
        uint insurance;
        Driver_pass d_pass;
    }
    
    struct Driver_pass{
        address owner;
        uint number;
        uint deadline;
        string category;
    }
    
    address payable public _owner;
    
    constructor () public{
        _owner = msg.sender;
    }
    
    modifier onlyOwner {
        require (msg.sender == _owner, "Only for owner");
        _;
    }
    
    modifier onlyDPS {
        require (u_roles[msg.sender] == 3, "You are not DPS man");
        _;
    }
    
    modifier onlyIns {
        require (u_roles[msg.sender] == 2, "You are not DPS man");
        _;
    }
    
    mapping(address => uint) u_roles;
    mapping(address => Driver) drivers;
    mapping(address => Driver_pass) d_pass;
    mapping(address => Transport[]) u_transport;
    mapping(uint => address payable) d_pass_to_user;
    Driver_pass[] uncomfirmed;
    address payable [] to_paying;
    
    function get_dr_info() public view returns(Driver memory){
        return drivers[msg.sender];
    }
    
    function set_role(address _user, uint _role) public onlyOwner{
        u_roles[_user] = _role;
    }
    
    function reg_driver(string memory _fio, uint16 _d_exp, uint16 _dtp, uint[] memory _fines, uint8 _num_pass, uint _deadline, string memory _category) public {
        require(u_roles[msg.sender] != 1, "You can't be a driver");
        require(u_roles[msg.sender] != 2, "You can't be a driver");
        drivers[msg.sender] = Driver(_fio, _d_exp, _dtp, _fines, 0, Driver_pass(msg.sender, _num_pass, _deadline, _category));
    }
    
    function reg_dr_pass(uint _number, uint _deadline, string memory _category) public{
        uncomfirmed.push(Driver_pass(msg.sender, _number, _deadline, _category));
    }
    
    function confirm_pass(uint _id) public onlyDPS{
        Driver_pass memory passport = uncomfirmed[_id];
        uncomfirmed[_id] = Driver_pass(address(0), 0, 0, "0");
        d_pass[passport.owner] = passport;
        drivers[passport.owner].d_pass = passport;
        d_pass_to_user[passport.number] = msg.sender;
    }

    function get_unpass() public view returns(Driver_pass[] memory){
        return uncomfirmed;
    }
    
    function get_dr_pass() public view returns(Driver_pass memory){
        return d_pass[msg.sender];
    }
    
    function reg_transpot(string memory _category, uint _price, uint _age) public{
        require(keccak256(bytes(d_pass[msg.sender].category)) == keccak256(bytes(_category)), "Unsuitable category");
        u_transport[msg.sender].push(Transport(_category, _price, _age));
    }
    
    function update_pass_life() public{
        Driver_pass memory passport = d_pass[msg.sender];
        require(passport.deadline <= block.timestamp+30*24*60*60);
        require(drivers[msg.sender].fines.length == 0);
        d_pass[msg.sender].deadline = block.timestamp+10*12*30*5;
        drivers[passport.owner].d_pass = passport;
    }
    
    function fines_paying(uint _id) public payable{
        uint price = 10 ether;
        if (drivers[msg.sender].fines[_id]+5*5 < block.timestamp){
            price /= 2; 
        }
        
        require(msg.value == price, "Not enough money");
        drivers[msg.sender].fines[_id] = 0;
    }
    
    function get_fines() public view returns(uint[] memory){
        return drivers[msg.sender].fines;
    }
    
    function insurance(uint _t_id, address payable _ins_comp) public payable{
        Transport memory transport = u_transport[msg.sender][_t_id];
        Driver memory driver = drivers[msg.sender];
        uint fines = 0;
        for (uint8 i = 0; i < driver.fines.length; i++){
            if (driver.fines[i] !=0)
                fines++;
        }
        
        uint price = transport.price*(uint(1-transport.age)/10+fines/5+driver.dtp-driver.d_exp/5);
        require(price == msg.value);
        require(u_roles[_ins_comp] == 2, "Not a insurance company");
        _ins_comp.transfer(msg.value);
        drivers[msg.sender].insurance=price;
    }
    
    function add_fine(uint _pass_num) public onlyDPS{
        address owner = d_pass_to_user[_pass_num];
        drivers[owner].fines.push(block.timestamp);
    }
    
    function add_dtp(uint _pass_num) public onlyDPS{
        address payable owner = d_pass_to_user[_pass_num];
        if (drivers[owner].insurance != 0){
            to_paying.push(owner);
        }
        drivers[owner].dtp++;
    }
    
    function paying_ins(uint _id) public payable onlyIns {
        address payable owner = to_paying[_id];
        to_paying[_id] = address(0);
        owner.transfer(drivers[owner].insurance*10);
    }
    
}