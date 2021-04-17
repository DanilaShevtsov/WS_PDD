from logging import ERROR
import web3
import os
import json

class Contract:
    def __init__(self, u_addr=None):
        self.w3 = web3.Web3(web3.HTTPProvider('http://192.168.0.2:8545'))
        with open(f'{os.path.dirname(__file__)}/abi.txt', 'r') as f:
            abi = json.load(f)

        with open(f'{os.path.dirname(__file__)}/contract_address.txt', 'r') as f:
            contract_address = f.read()
        contract_address = web3.Web3.toChecksumAddress(contract_address)
        self.contract = self.w3.eth.contract(contract_address, abi=abi)
        self.u_addr=u_addr
        

    def get_auth(self, addr1):
        addr1 = web3.Web3.toChecksumAddress(addr1)
        ans = self.contract.functions.auth(addr1).call()
        return ans

    def add_dr_pass(self, number, deadline, category):
        ans = self.contract.functions.add_dr_pass(number, deadline, category).transact({'from':self.u_addr})
        return ans

    def registration(self, pass_hash, fio, dr_exp, dtp, addr):
        addr = web3.Web3.toChecksumAddress(addr)
        ans = self.contract.functions.registration(pass_hash, fio, dr_exp, dtp).transact({'from':addr})
        return ans

    def get_dr_pass(self, number):
        ans = self.contract.functions.dr_pass(number).call({'from':self.u_addr})
        return ans

    def get_driver(self, addr):
        addr = web3.Web3.toChecksumAddress(addr)
        ans = self.contract.functions.get_driver(addr).call({'from':self.u_addr})
        return ans

    def reg_transport(self, category, price, yearsold):
        ans = self.contract.functions.reg_transport(category, price, yearsold).transact({'from':self.u_addr})
        return ans
    
    def prolong_dr_pass(self):
        ans = self.contract.functions.prolong_dr_pass().transact({'from': self.u_addr})
        return ans
    
    def pay_fines(self, id, value):
        ans = self.contract.functions.pay_fines(id).transact({'from':self.u_addr, 'value': value})
        return ans
    
    def reg_ins(self, value):
        """
        Регистрирует страховку\n
        value - деньги, которые уйдут в контракт
        """
        try:
            ans = self.contract.functions.reg_ins().transact({'from': self.u_addr, 'value': value})
        except:
            ans = 'Ошибка регистрации страховки'
        return ans

    def reg_fine(self, num_dr_pass):
        """
        Регистрарует штраф
        """
        ans = self.contract.functions.reg_fine(num_dr_pass).transact('from')
        return ans
        

