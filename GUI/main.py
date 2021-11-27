#-----------------------------------------------------------------------------------------------------------
#
#                                           BOOTLEG STEAM
#
#-----------------------------------------------------------------------------------------------------------
import sys 
import psycopg2
import steamspypi
import os
from mainLogin import Ui_Login_Dialog
from createAcc import Ui_Sign_Up_Dialog
from mainWindow import Ui_MainWindow
from filteredSearch import Ui_filteredResults
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QDialog as qd, QApplication as qapp, QMainWindow as qwin, QVBoxLayout

# Class implementing the main login page.
class Login(qd, Ui_Login_Dialog):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setFixedSize(600, 800)

        self.loginButton.clicked.connect(self.authenticate)
        self.loginButton.clicked.connect(self.goToMainWindow)
        self.signUpButton.clicked.connect(self.goToCreateAcc)

    # Primitive login authentication.
    # To do: Add one way hash to users table, and passwords column.
    def authenticate(self):

        username = self.uEdit.text()
        password = self.pEdit.text()

        #Username Validity Checker
        Valid = Check_Login(username, password)
        print(Valid)

        if Valid == 1:
            qtw.QMessageBox.information(self, 'Success', 'You are logged in.')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You did not log in.')

    # Opens createAcc window.
    def goToCreateAcc(self):
        create = CreateAcc()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # Opens main window.
    def goToMainWindow(self):
        window = Main_Window()
        widget.addWidget(window)
        widget.setCurrentIndex(widget.currentIndex()+1)

# Class to implement the create account page.
class CreateAcc(qd, Ui_Sign_Up_Dialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        self.setupUi(self)
        self.setFixedSize(600, 800)

        self.loginButton.clicked.connect(self.createAccFunction)
    
    # To do: add functionality for updating users table w/ psycopg2
    def createAccFunction(self):
        username = self.uEdit.text()
        if self.pEdit.text() == self.pEdit_2.text():
            password = self.pEdit.text()
            #Check if username exists
            Added = Check_User(username)
            if Added == 1: 
                Add_User(username, password)
                qtw.QMessageBox.information(self, 'Success', 'You\'re account has been created, you may now login!')
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                qtw.QMessageBox.critical(self, 'Fail', 'You\'re passwords didn\'t match, please reenter your password.')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You\'re passwords didn\'t match, please reenter your password.')

class filteredSearch(qd, Ui_filteredResults):
    def __init__(self):
        super(filteredSearch, self).__init__()
        self.setupUi(self)
        self.setFixedSize(800, 800)


# Main window for app. Now with Skyrim memes!
class Main_Window(qwin, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1100, 800)
        self.windows = []

        self.filterButtonSpecials.clicked.connect(self.goToFilteredSearch)
        self.filterButtonPositive.clicked.connect(self.goToFilteredSearch)
        self.filterButtonNegative.clicked.connect(self.goToFilteredSearch)
        self.filterValveGames.clicked.connect(self.goToFilteredSearch)

   # @qtc.pyqtSlot()
    def goToFilteredSearch(self):
        window = filteredSearch()
        window.show()
        self.windows.append(window)

#Checks for username and password in database
def Check_Login(username, pw):
    print(username)
    con = psycopg2.connect(
        host="localhost", 
        database="FP",
        user="postgres",
        password="AWEsome1",
        port=5432
    )

    cur = con.cursor()
    cur.execute("SELECT * FROM steam_account WHERE username = %s AND password = %s;", (username, pw))
    if (cur.fetchone() is not None == 1):
        cur.close()
        con.close()
        return 1
    else:
        cur.close()
        con.close()
        return 2

#Checks if user exists in table    
def Check_User(username):
    con = psycopg2.connect(
        host="localhost", 
        database="FP",
        user="postgres",
        password="AWEsome1",
        port=5432
    )

    cur = con.cursor()
    cur.execute("SELECT * FROM steam_account WHERE username = %s;", (username))
    if (cur.fetchone() is not None == 1):
        cur.close()
        con.close()
        return 1
    else:
        cur.close()
        con.close()
        return 2

#Would add a username and password to database
#WARNING, this is a To-Do, but you cannot just send username and password, you need more attributes
def Add_User(username, pw):
    print(username)

# App startup.
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
app = qapp(sys.argv)
qapp.setAttribute(qtc.Qt.AA_EnableHighDpiScaling, True)
qapp.setAttribute(qtc.Qt.AA_UseHighDpiPixmaps, True)
mainWindow = Login()
widget = qtw.QStackedWidget()
layout = QVBoxLayout()
widget.addWidget(mainWindow)
widget.setLayout(layout)
widget.show()
app.exec_()