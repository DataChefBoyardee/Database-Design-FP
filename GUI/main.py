#-----------------------------------------------------------------------------------------------------------
#
#                                           BOOTLEG STEAM
#
#-----------------------------------------------------------------------------------------------------------
import sys 
from mainLogin import Ui_Login_Dialog
from createAcc import Ui_Sign_Up_Dialog
from mainWindow import Ui_MainWindow
from filteredSearch import Ui_filteredResults
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QDialog as qd, QApplication as qapp, QMainWindow as qwin
import psycopg2
import steamspypi

# Class implementing the main login page.
class Login(qd, Ui_Login_Dialog):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setFixedSize(477, 620)
        self.loginButton.clicked.connect(self.authenticate)
        self.loginButton.clicked.connect(self.goToMainWindow)
        self.signUpButton.clicked.connect(self.goToCreateAcc)

    # Primitive login authentication.
    # To do: Add one way hash to users table, and passwords column.
    def authenticate(self):

        username = self.uEdit.text()
        password = self.pEdit.text()

        if username == 'user' and password == 'pass':
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
        self.setFixedSize(477, 620)

        self.loginButton.clicked.connect(self.createAccFunction)
    
    # To do: add functionality for updating users table w/ psycopg2
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
        
#Database Connection
def connection(data):
    #Connect to db
    con = psycopg2.connect(
        host="localhost", 
        database="FP",
        user="postgres",
        password="AWEsome1",
        port=5432
    )
    gappid = data['appid']
    gname = data['name']
    gdev = data['developer']
    gpub = data['publisher']
    ggenre = data['genre']
    #print(data)
    #cursor
    cur = con.cursor()

    #execute query
    cur.execute("insert into steamdata (name, Developer, Publisher, Genre) values (%s, %s, %s, %s)", (gname, gdev, gpub, ggenre) )
    #rows = cur.fetchall()

    #for r in rows:
    #    print(f"charID: {r[0]} name: {r[1]}")


    con.commit()
    #close cursor
    cur.close()

    #close connection
    con.close()

#SteamSpy Data grabbing
def data():
    data_request = dict()
    data_request['request'] = 'appdetails'
    data_request['appid'] = '393380'

    data = steamspypi.download(data_request)
    connection(data)
    gname = data['name']
    gdev = data['developer']
    gpub = data['publisher']
    ggenre = data['genre']
    print(data)
    #print("%s, %s, %s, %s" % (gname, gdev, gpub, ggenre))

# App startup.
app = qapp(sys.argv)
mainWindow = Login()
widget = qtw.QStackedWidget()
widget.addWidget(mainWindow)
widget.show()
app.exec_()