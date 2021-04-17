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
        

    def get_auth(self, addr1)->str:
        """
        Функция для входа возвращает хэш-строку пароля\n
        addr1 - адресс пользователя в системе 
        """
        addr1 = web3.Web3.toChecksumAddress(addr1)
        ans = self.contract.functions.auth(addr1).call()
        return ans

    def add_dr_pass(self, number, deadline, category):
        """
        Добавляет водительское удостоверение\n
        number - номер документа\n
        deadline - дата конца годности\n
        category - категория удоств.\n
        000-11.01.2021-1\n
        111-12.05.2025-2\n
        222-09.09.2020-3\n
        333-13.02.2027-1\n
        444-11.12.2026-2\n
        555-24.06.2029-3\n
        666-31.03.2030-1\n
        !!! 000 нужно преобразовать в 0 !!!
        A - 1\n
        B - 2\n
        C - 3\n
        Без категории - 9
        """
        self.contract.functions.add_dr_pass(number, deadline, category).transact({'from':self.u_addr})


    def registration(self, pass_hash:str, fio:str, dr_exp:int, dtp:int, addr:str):
        """
        Функция регистрации, задает пароль пользователю\n
        pass_hash - хэш-строка пароля\n
        fio - Фамилия, Имя, Отчество через пробел\n
        dr_exp - Опыт вождения в годах\n
        dtp - Количество дтп\n
        addr - Адрес пользователя
        """
        addr = web3.Web3.toChecksumAddress(addr)
        self.contract.functions.registration(pass_hash, fio, dr_exp, dtp).transact({'from':addr})
        

    def get_dr_pass(self, number:int)->tuple:
        """
        Возвращает информацию о водительском удостоверении по номеру\n
        number - номер документа
        """
        ans = self.contract.functions.dr_pass(number).call({'from':self.u_addr})
        return ans

    def get_driver(self, addr)->tuple:
        """
        Возвращает информацию о водителе\n
        addr - адрес водителя
        """
        addr = web3.Web3.toChecksumAddress(addr)
        ans = self.contract.functions.get_driver(addr).call({'from':self.u_addr})
        return ans

    def reg_transport(self, category, price, yearsold):
        """
        Добавляет транспорт водителю. Если категория транспорта не соответствует категории прав, вернется ошибка\n
        category - категория транспорта\n
        price - цена транспорта\n
        yearsold - возраст транспорта
        """
        self.contract.functions.reg_transport(category, price, yearsold).transact({'from':self.u_addr})
        
    
    def prolong_dr_pass(self):
        """
        Продление прав на год\n
        Вернется ошибка, если продляется позже 30 дней до конца срока 
        """
        ans = self.contract.functions.prolong_dr_pass().transact({'from': self.u_addr})
        return ans
    
    def pay_fines(self, id, value):
        """
        Оплата штрафа.\n
        id - идентификатор штрафа\n
        value - Сумма оплаты. Обычно равна 10 eth, если есть страховка - к оплате 5 eth
        """
        self.contract.functions.pay_fines(id).transact({'from':self.u_addr, 'value': value})
        
    
    def reg_ins(self, value):
        """
        Регистрирует страховку\n
        value - деньги, которые уйдут в контракт
        """
        
        ans = self.contract.functions.reg_ins().transact({'from': self.u_addr, 'value': value})
        
        

    def reg_fine(self, num_dr_pass):
        """
        Регистрарует штраф
        num_dr_pass - номер водительского удостоверения
        """
        self.contract.functions.reg_fine(num_dr_pass).transact('from')
        
        
adr = web3.Web3.toChecksumAddress("0xA54A98E716855c47E172cFC7Ab5Dc482a9783c81")
c = Contract(adr)
print(c.get_driver(adr))


