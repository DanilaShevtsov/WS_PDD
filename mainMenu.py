from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from main_menu import Ui_MainWindow
from ChangeVodUd import ChangeUd

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.eror= QtWidgets.QErrorMessage()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.change_vod_ud)


    
    def change_vod_ud(self):
        self.open = ChangeUd()
        self.open.show()

            
        


if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    myapp = MainMenu()
    myapp.show()
    sys.exit(app.exec())

