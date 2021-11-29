#-----------------------------------------------------------------------------------------------------------
#
#                                           BOOTLEG STEAM
#
#-----------------------------------------------------------------------------------------------------------
import sys, os, psycopg2, pandas as pd 
from mainLogin import Ui_Login_Dialog
from createAcc import Ui_Sign_Up_Dialog
from mainWindow import Ui_MainWindow
from filteredSearch import Ui_filteredResults
from orderPage import Ui_orderPage
from functools import partial
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QDialog as qd, QApplication as qapp, QMainWindow as qwin, QVBoxLayout

username = " "

# Initialize database connection.
con = psycopg2.connect(
host="localhost", 
database="steam",
user="postgres",
password="AptechkaStrelok2!",
port=5432
)
cur = con.cursor()

# Class implementing the main login page.
class mainLogin(qd, Ui_Login_Dialog):
    def __init__(self):
        super(mainLogin, self).__init__()
        self.setupUi(self)
        self.setFixedSize(600, 800)

        self.loginButton.clicked.connect(self.authenticate)
        self.signUpButton.clicked.connect(self.goToCreateAcc)

    # Login authentication.
    def authenticate(self):

        global username
        username = self.uEdit.text()
        password = self.pEdit.text()

        #Username Validity Checker
        Valid = Check_Login(password)

        if Valid == 1:
            qtw.QMessageBox.information(self, 'Success', 'You are logged in.')
            self.goToMainWindow()
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

        self.createAccountButton.clicked.connect(self.createAccFunction)
    
    # To do: add functionality for updating users table w/ psycopg2
    def createAccFunction(self):
        global username
        username = self.uEdit.text()
        country = self.cEdit.text()
        if self.pEdit.text() == self.pEdit_2.text() and self.pEdit.text() != "":
            password = self.pEdit.text()
            #Check if username exists
            Added = Add_User(password, country)
            if Added == 1: 
                qtw.QMessageBox.information(self, 'Success', 'You\'re account has been created, you may now login!')
                login = mainLogin()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                qtw.QMessageBox.critical(self, 'Fail', 'This username already exists. Please choose a different username.')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You\'re passwords didn\'t match, please reenter your password.')


# Main window for app.
class Main_Window(qwin, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1100, 800)
        self.windows = []


        # Initialize the table view
        dataFrame = initializeTableView('top100', ' ')
        self.model = TableModel(dataFrame)
        self.tableView.setModel(self.model)

        self.filterButtonSpecials.clicked.connect(self.goToFilteredSearchSpecials)
        self.filterButtonScore.clicked.connect(self.goToFilteredSearchScore)
        self.filterValveGames.clicked.connect(self.goToFilteredSearchValve)
        self.searchButton.clicked.connect(self.goToFilteredSearch)

    def goToFilteredSearchSpecials(self):
        window = filteredSearch("Current Specials", "", Main_Window)
        window.show()
        self.windows.append(window)
    
    def goToFilteredSearchScore(self):
        window = filteredSearch("Top Scoring Games", "", Main_Window)
        window.show()
        self.windows.append(window)

    def goToFilteredSearchValve(self):
        window = filteredSearch("Games by Valve", "", Main_Window)
        window.show()
        self.windows.append(window)

    def goToFilteredSearch(self):
        searchTerm = self.searchBar.text()
        window = filteredSearch("search", searchTerm, Main_Window)
        window.show()
        self.windows.append(window)


class filteredSearch(qd, Ui_filteredResults):
    def __init__(self, filtering, searchTerm, Main_Window):
        super(filteredSearch, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1100, 800)
        self.windows = []
        if filtering == "search":
            self.filterType.setText(searchTerm)
        else:
            self.filterType.setText(filtering)

        dataFrame = initializeTableView(filtering, searchTerm)
        self.model = TableModel(dataFrame)
        self.tableFilteredResults.setModel(self.model)

        order = self.orderEdit.text()
        self.orderButton.clicked.connect(partial(self.goToOrderPage, order))
    
    def goToOrderPage(self, order):
        order = self.orderEdit.text()
        window = orderPage(order)
        window.show()
        self.windows.append(window)


class orderPage(qd, Ui_orderPage):
    def __init__(self, order):
        super(orderPage, self).__init__()
        #print(type(order))
        self.setupUi(self)
        self.setFixedSize(500, 500)

        self.Cancel.clicked.connect(self.closeWindow)
        self.Ok.clicked.connect(partial(self.makeOrder, order))
    
    def makeOrder(self, order):
        global cur
        #print(type(order))
        cur.execute("SELECT product_id FROM product WHERE name = %s;", (order, ))
        ID = cur.fetchone()
        cur.execute("SELECT discounted_price FROM product WHERE name = %s;", (order, ))
        FP = cur.fetchone()
        print(ID)
        Make_Order(ID, FP)
        self.close()

    
    def closeWindow(self):
        self.close()

#Checks for username and password in database
def Check_Login(pw):

    global username
    cur.execute("select * from steam_account where username = %s and password = %s;", (username, pw,))
    loginInfo = cur.fetchone()
    if (loginInfo[0] == username and loginInfo[1] == pw):
        return 1
    else:
        return 2

# #Checks if user exists in table
# def Check_User():
#     global username
#     cur.execute("SELECT * FROM steam_account WHERE username = %s;", (username,))
#     userInfo = cur.fetchone()
#     if (userInfo is not None):
#         return 2
#     else:
#         return 1

#Would add a username and password to database
#WARNING, this is a To-Do, but you cannot just send username and password, you need more attributes
def Add_User(pw, country):
    global username

    try:
        cur.execute("INSERT into steam_account (username, password, country_of_residence, steam_wallet) values (%s, %s, %s, 0);", (username, pw, country))
    except psycopg2.errors.UniqueViolation:
        #make popup that says username already exists
        return 2

    con.commit()
    return 1


def initializeTableView(tableType, searchTerm):

    # Checks the table view type.
    if (tableType == 'top100'):

        cur = con.cursor()
        cur.execute("SELECT name, developer, publisher, discounted_price, positive_ratings, negative_ratings, genres FROM product;")
        col_names = [desc[0] for desc in cur.description]
        retList = cur.fetchall()
        retFrame = pd.DataFrame(retList, columns = col_names)
        return retFrame

    if (tableType == "Top Scoring Games"):
        # add SQL queries here
        cur = con.cursor()
        cur.execute("SELECT name, developer, publisher, discounted_price, positive_ratings, negative_ratings, genres FROM product;")
        col_names = [desc[0] for desc in cur.description]
        retList = cur.fetchall()
        retFrame = pd.DataFrame(retList, columns = col_names)
        return retFrame

    if (tableType == "Games by Valve"):
        # add SQL queries here
        cur = con.cursor()
        cur.execute("SELECT name, developer, publisher, discounted_price, positive_ratings, negative_ratings, genres FROM product;")
        col_names = [desc[0] for desc in cur.description]
        retList = cur.fetchall()
        retFrame = pd.DataFrame(retList, columns = col_names)
        return retFrame

    if (tableType == "Current Specials"):
        # add SQL queries here
        cur = con.cursor()
        cur.execute("SELECT name, developer, publisher, discounted_price, positive_ratings, negative_ratings, genres FROM product;")
        col_names = [desc[0] for desc in cur.description]
        retList = cur.fetchall()
        retFrame = pd.DataFrame(retList, columns = col_names)
        return retFrame
        
    if (tableType == "search"):
        # add SQL queries here
        # Use extra passed value to indicated search term.
        cur = con.cursor()
        cur.execute("SELECT name, developer, publisher, discounted_price, positive_ratings, negative_ratings, genres FROM product;")
        col_names = [desc[0] for desc in cur.description]
        retList = cur.fetchall()
        retFrame = pd.DataFrame(retList, columns = col_names)
        return retFrame

# Class to define tables using PyQt5 abstract class.
class TableModel(qtc.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

def Make_Order(ID, FP):
    global username
    print(type(username))

    
    cur = con.cursor()
    print(type(username))
    cur.execute("INSERT into orders (username, order_time) values (%s, CURRENT_TIMESTAMP)", (username, ))
    con.commit()

    cur.execute("SELECT order_id FROM orders WHERE username = %s ORDER BY order_time DESC LIMIT 1", (username, ))
    ordernum = cur.fetchone()

    try:
        cur.execute("INSERT into order_details (product_id, order_id, final_price) values (%s, %s, %s)", (ID, ordernum, FP, ))
    except (Exception, psycopg2.DatabaseError) as ex:
        #make order page spit this error out if return type is string, which this is
        return str(ex)
    
    con.commit()
    #success if 1, return type int
    return 1

# App startup.
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
app = qapp(sys.argv)
qapp.setAttribute(qtc.Qt.AA_EnableHighDpiScaling, True)
qapp.setAttribute(qtc.Qt.AA_UseHighDpiPixmaps, True)
login = mainLogin()
widget = qtw.QStackedWidget()
layout = QVBoxLayout()
widget.addWidget(login)
widget.setLayout(layout)
widget.show()
widget.setWindowTitle("Vapor")
sys.exit(app.exec_())