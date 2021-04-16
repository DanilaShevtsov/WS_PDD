from PyQt5 import QtWidgets, QtCore
import sys

from Change_vod_ud import ChangeVod
from a import Contract
import datetime




class ChangeUd(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ChangeVod()
        self.eror= QtWidgets.QErrorMessage()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.savedan)
        self.adr = "0x0fcaa8df99cba856cf72059652c6ebb7acdbcffd"
        self.Cont = Contract(self.adr)
    
    def savedan(self):
        number = int(self.ui.lineEdit.text())
        data = self.ui.lineEdit_2.text()

        kateg = int(self.ui.lineEdit_3.text())
        ans = self.Cont.add_dr_pass(number, data, kateg)
        if ans == 'Ошибка регистрации страховки':
            self.eror.setWindowTitle("Ошибка входа")
            self.eror.showMessage("Данные введены неверно.")
        else:
            self.close()
    

if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    myapp = ChangeUd()
    myapp.show()
    sys.exit(app.exec())