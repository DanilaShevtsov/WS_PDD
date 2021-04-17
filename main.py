from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys

import hashlib
import web3
import datetime


import a
from sign import Ui_Registration_Or_Sign
from main_menu import Ui_MainWindow
from Change_vod_ud import ChangeVod

class Sign(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Registration_Or_Sign()
        self.eror= QtWidgets.QErrorMessage()
        self.ui.setupUi(self)

        self.Cont = a.Contract()
        self.ui.pushButton.clicked.connect(self.reg)
        self.ui.Sign.clicked.connect(self.sign)
    
    def reg(self):
        address = self.ui.Addres.text()
        fio = self.ui.FIO.text()
        stag = int(self.ui.Stag.text())
        kol_DTP = int(self.ui.Kol.text())
        password = self.ui.Password.text()
        password_two = self.ui.Password_two.text()

        if password == password_two:
            hash1 = hashlib.sha256(password_two.encode()).hexdigest()
            address = web3.Web3.toChecksumAddress(address)
            self.Cont.registration(hash1, fio, stag, kol_DTP, address)
            self.Cont.u_addr=address
            self.open = MainMenu(self.Cont)
            self.open.show()
            self.close()
        else:
            self.eror.setWindowTitle("Ошибка")
            self.eror.showMessage("Пароли не совпадают")   


    def sign(self):
        password_sign = self.ui.Password_sign.text()
        address_sign = self.ui.Addres_Sign.text()
        hash_sign = hashlib.sha256(password_sign.encode()).hexdigest()
        if hash_sign == self.Cont.get_auth(address_sign):
            self.Cont.u_addr = web3.Web3.toChecksumAddress(address_sign)
            self.open = MainMenu(self.Cont)
            self.open.show()
            self.close()
        else:
            self.eror.setWindowTitle("Ошибка входа")
            self.eror.showMessage("Данные введены неверно.")
        


        
class MainMenu(QtWidgets.QMainWindow):
    kat ={
        1: "A",
        2: "B",
        3: "C",
        9: "Не указанно"
    }
    def __init__(self, Cont=None):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.eror= QtWidgets.QErrorMessage()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.change_vod_ud)
        self.Cont = Cont
        self.sho()


        #self.adrus = web3.Web3.toChecksumAddress("0xb62b0d39a824fab6fb7e5915c59fe3a779765ef2")
        #self.Cont = a.Contract(self.adrus)


    
    def change_vod_ud(self):
        self.open = ChangeUd(self.Cont)
        self.open.show()
        lis = self.Cont.get_driver(self.Cont.u_addr)
        if not lis[1]==9:
            lis_ud = self.Cont.get_dr_pass(lis[1])
            self.ui.label_11.setText(str(lis[1]))
            self.ui.label_12.setText(str(datetime.datetime.fromtimestamp(lis_ud[0])))
            self.ui.label_13.setText(self.kat[lis_ud[1]])
        else:
            self.ui.label_11.setText("Не указано")
            self.ui.label_12.setText("")
            self.ui.label_13.setText("")


    def sho(self):
        lis = self.Cont.get_driver(self.Cont.u_addr)
        self.ui.label.setText(lis[0])
        self.ui.label_8.setText(str(lis[2]))
        self.ui.label_9.setText(str(lis[3]))
        self.ui.label_10.setText(str(len(lis[4])))
        if not lis[1]==9:
            lis_ud = self.Cont.get_dr_pass(lis[1])
            self.ui.label_11.setText(str(lis[1]))
            self.ui.label_12.setText(str(datetime.datetime.fromtimestamp(lis_ud[0])))
            print(self.kat)
            self.ui.label_13.setText(self.kat[lis_ud[1]])
        else:
            self.ui.label_11.setText("Не указано")
            self.ui.label_12.setText("")
            self.ui.label_13.setText("")

        

class ChangeUd(QtWidgets.QMainWindow):
    def __init__(self, Cont=None):
        super().__init__()
        self.ui = ChangeVod()
        self.eror= QtWidgets.QErrorMessage()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.savedan)
        self.Cont = Cont


    def savedan(self):
        number = int(self.ui.lineEdit.text())
        data = self.ui.lineEdit_2.text().split('.')
        dt = datetime.datetime(day=int(data[0]), month=int(data[1]), year=int(data[2]))
        dt = int(dt.timestamp())        
        kateg = int(self.ui.lineEdit_3.text())
        ans = self.Cont.add_dr_pass(number, dt, kateg)
        if ans == 'Ошибка регистрации страховки':
            self.eror.setWindowTitle("Ошибка входа")
            self.eror.showMessage("Данные введены неверно.")
        else:
            self.close()
    


if __name__ == "__main__":
    app=QtWidgets.QApplication([])
    myapp = Sign()
    #myapp = MainMenu()
    myapp.show()
    sys.exit(app.exec())