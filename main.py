from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from sign import Ui_Registration_Or_Sign
from mainMenu import MainMenu
import hashlib
import web3
import a


class Sign(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Registration_Or_Sign()
        self.eror= QtWidgets.QErrorMessage()
        self.ui.setupUi(self)
        self.adr = "0x991f64Ae7879bD192A89A35502ec34612AF34EB8"
        self.Cont = a.Contract(self.adr)
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
            self.open = MainMenu()
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
            self.open = MainMenu()
            self.open.show()
            self.close()
        else:
            self.eror.setWindowTitle("Ошибка входа")
            self.eror.showMessage("Данные введены неверно.")
        
        




if __name__ == "__main__":
    app=QtWidgets.QApplication([])
    myapp = Sign()
    myapp.show()
    sys.exit(app.exec())

