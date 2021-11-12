import sys 
from mainLogin import Ui_Login_Dialog
from createAcc import Ui_Sign_Up_Dialog
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QDialog, QApplication

class Login(QDialog, Ui_Login_Dialog):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)

        self.loginButton.clicked.connect(self.authenticate)
        self.signUpButton.clicked.connect(self.goToCreateAcc)

    def authenticate(self):

        username = self.uEdit.text()
        password = self.pEdit.text()

        if username == 'user' and password == 'pass':
            qtw.QMessageBox.information(self, 'Success', 'You are logged in.')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You did not log in.')

    def goToCreateAcc(self):
        create = CreateAcc()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog, Ui_Sign_Up_Dialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        self.setupUi(self)

        self.loginButton.clicked.connect(self.createAccFunction)
        
    def createAccFunction(self):
        username = self.uEdit.text()
        if self.pEdit.text() == self.pEdit_2.text():
            password = self.pEdit.text()
            qtw.QMessageBox.information(self, 'Success', 'You\'re account has been created, you may now login!')
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You\'re passwords didn\'t match, please reenter your password.')


app = QApplication(sys.argv)
mainWindow = Login()
widget = qtw.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()