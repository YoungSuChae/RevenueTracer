import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox, QGraphicsScene, QLabel
from PyQt6.QtCore import Qt, QTimer
from LoginCreatePage import Ui_MainWindow
from SaleInterface import Ui_MainUI
from User import User
from Store import Store
from Item import Item
from Department import Department
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from model import SalesForecaster 


class SaleInterfaceWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_MainUI()
        self.ui.setupUi(self)
        self.username = username
        self.showUsernameLabel()
        self.setValueProgessBars()
        self.showCurrentMonthlyRevenue()
        self.showPreviousMonthlyrevenue()
        self.showMostProfitItem()
        self.showProfitableStore()
        #self.uncheckDepartment()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setValuetoStock)
        self.timer.start(3000)  # Update every 3 seconds (3000 milliseconds)

        self.scene = QGraphicsScene(parent=self.ui.AnalysisTab)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.setSceneRect(0,0,700,500)  # Set scene size

        sales_forecaster = SalesForecaster()
        sales_forecaster.model()

        fig = sales_forecaster.plot_forecast()
        canvas = FigureCanvas(fig)

        # Add the FigureCanvas to the QGraphicsScene
        self.scene.addWidget(canvas)

        # Only checks one at a time for store
        self.ui.addCheckBox.stateChanged.connect(self.uncheckStore) 
        self.ui.searchCheckBox.stateChanged.connect(self.uncheckStore) 
        self.ui.deleteCheckBox.stateChanged.connect(self.uncheckStore) 

        # Only checks one at a time for department
        self.ui.depAddBox.stateChanged.connect(self.uncheckDepartment)
        self.ui.depDeleteBox.stateChanged.connect(self.uncheckDepartment)
        self.ui.depSearchBox.stateChanged.connect(self.uncheckDepartment)

        #Only chcks one at a time for Item
        self.ui.itemAddCheckBox.stateChanged.connect(self.unCheckItem)
        self.ui.itemDeleteCheckBox.stateChanged.connect(self.unCheckItem)
        self.ui.itemSearchCheckBox.stateChanged.connect(self.unCheckItem)

        # Connects enter button for store page
        self.ui.storeEnterButton.clicked.connect(self.showStoreInfo)
        self.ui.departmentEnterButton.clicked.connect(self.showDepartmentInfo)
        self.ui.itemEnterButton.clicked.connect(self.showItemInfo)

    def setValueProgessBars(self):
        self.ui.quarterOneProgessBar.setValue(SalesForecaster.last_quarter_revenue())
        self.ui.quarterTwoProgessBar.setValue(SalesForecaster.second_last_quarter_revenue())
        self.ui.quarterThreeProgessBar.setValue(SalesForecaster.third_last_quarter_revenue())
        self.ui.quarterFourProgessBar.setValue(SalesForecaster.fourth_last_quarter_revenue())

    def setValuetoStock(self):
            current_stock = random.randint(-20, 20)
            self.ui.stockOutput.setText(f"% {str(current_stock)}")

            if current_stock < 0:
                self.ui.stockOutput.setStyleSheet("color: red;font-size: 15pt;")
            else:
                self.ui.stockOutput.setStyleSheet("color: green;font-size: 15pt;")

    def showUsernameLabel(self):
        if self.username:
            self.ui.usernameLabel.setStyleSheet("color: blue;font-size: 20pt;")
            self.ui.usernameLabel.setText(self.username)

    def showCurrentMonthlyRevenue(self):
        currentMonthlyRevenue = Store.currentMonthlyRevenue()
        self.ui.currentMonthRev.setText(f"${currentMonthlyRevenue}")

    def showPreviousMonthlyrevenue(self):
        previousMonthlyRevenue = Store.previousMonthlyRevenue()
        self.ui.pastMonthLabel_2.setText(f"${previousMonthlyRevenue}")

    def showMostProfitItem(self):
        current_max_item = Item.item_revenue()
        self.ui.itemMostRevTextbox.setText(current_max_item)

    def showProfitableStore(self):
        currentStore = Store.mostProfitableStore()
        self.ui.mostProfitableStoreTextbox.setText(currentStore)

    def uncheckStore(self):
        sender_checkbox = self.sender()
        self.ui.scrollAreaStore.clear()

        if sender_checkbox == self.ui.addCheckBox and sender_checkbox.isChecked():
            self.ui.searchCheckBox.setChecked(False) 
            self.ui.deleteCheckBox.setChecked(False)
            self.ui.storeAddressLabel.show()
            self.ui.storeAddressInput.show()
            self.ui.storePhoneLabel.show()
            self.ui.storePhoneInput.show()
            self.ui.storeMonthlyLabel.show()
            self.ui.storeMonthlyInput.show()
            self.ui.storeDateLabel.show()
            self.ui.dateEdit.show()

        elif sender_checkbox == self.ui.searchCheckBox and sender_checkbox.isChecked():
            self.ui.addCheckBox.setChecked(False) 
            self.ui.deleteCheckBox.setChecked(False)
            self.ui.storeAddressLabel.show()
            self.ui.storeAddressInput.show()
            self.ui.storePhoneLabel.hide()
            self.ui.storePhoneInput.hide()
            self.ui.storeMonthlyLabel.hide()
            self.ui.storeMonthlyInput.hide()
            self.ui.storeDateLabel.hide()
            self.ui.dateEdit.hide()

        elif sender_checkbox == self.ui.deleteCheckBox and sender_checkbox.isChecked():
            self.ui.searchCheckBox.setChecked(False) 
            self.ui.addCheckBox.setChecked(False)
            self.ui.storeAddressLabel.show()
            self.ui.storeAddressInput.show()
            self.ui.storePhoneLabel.hide()
            self.ui.storePhoneInput.hide()
            self.ui.storeMonthlyLabel.hide()
            self.ui.storeMonthlyInput.hide()
            self.ui.storeDateLabel.hide()
            self.ui.dateEdit.hide()
        
    def showStoreInfo(self):
        # Search Store
        if self.ui.searchCheckBox.isChecked():
            currentStoreName = self.ui.storeNameinput.text()
            currentStoreAddr = self.ui.storeAddressInput.text()
            listOfStores = Store.search_store(currentStoreName,currentStoreAddr)
            self.ui.scrollAreaStore.setText(f"{str(listOfStores)}")
        # Delete Store
        if self.ui.deleteCheckBox.isChecked():
            currentStoreName = self.ui.storeNameinput.text()
            currentStoreAddr = self.ui.storeAddressInput.text()
            listOfStores = Store.deleteStore(currentStoreName,currentStoreAddr)
            self.ui.scrollAreaStore.clear()
            self.ui.scrollAreaStore.setText("The store has been deleted.")
        # Add Store and Revenue
        if self.ui.addCheckBox.isChecked():
            StoreName = self.ui.storeNameinput.text()
            StoreAddr = self.ui.storeAddressInput.text()
            StorePhone = self.ui.storePhoneInput.text()
            StoreRevenue = self.ui.storeMonthlyInput.text()
            StoreDate = self.ui.dateEdit.date().toString(Qt.DateFormat.ISODate)  # Convert QDate to string
            addStore = Store.add_store(StoreName,StoreAddr,StorePhone,StoreRevenue,StoreDate)
            self.ui.scrollAreaStore.setText(f"The store: {StoreName} on {StoreAddr} have been added.")

    #Integrate Department checkbox into gui, change names of functions
    # Make sure multiple things cannot be checked

    def uncheckDepartment(self):
        sender_checkbox = self.sender()
        self.ui.scrollAreaDepart.clear()
        # Add check box
        if sender_checkbox == self.ui.depAddBox and sender_checkbox.isChecked():
            self.ui.depSearchBox.setChecked(False) 
            self.ui.depDeleteBox.setChecked(False)
            self.ui.departmentNameLabel.show()
            self.ui.departmentNameInput.show()
            self.ui.departmentDescLabel.show()
            self.ui.depDescTextBox.show()

        # Delete check box
        elif sender_checkbox == self.ui.depDeleteBox and sender_checkbox.isChecked():
            self.ui.depSearchBox.setChecked(False) 
            self.ui.depAddBox.setChecked(False)
            self.ui.departmentNameLabel.show()
            self.ui.departmentNameInput.show()
            self.ui.departmentDescLabel.hide()
            self.ui.depDescTextBox.hide()

        # Search check box
        elif sender_checkbox == self.ui.depSearchBox and sender_checkbox.isChecked():
            self.ui.depDeleteBox.setChecked(False) 
            self.ui.depAddBox.setChecked(False)
            self.ui.departmentNameLabel.show()
            self.ui.departmentNameInput.show()
            self.ui.departmentDescLabel.hide()
            self.ui.depDescTextBox.hide()

    # Department info into variables
    def showDepartmentInfo(self):

        # self.ui.scrollAreaDepart.clear()
        # Search for a department, call the search function
        if self.ui.depSearchBox.isChecked():
            name = self.ui.departmentNameInput.text()
            output_dep_name = Department.search_file(name)
            self.ui.scrollAreaDepart.setText(output_dep_name)
        # Delete a department, call the delete function 
        if self.ui.depDeleteBox.isChecked():
            department_name = self.ui.departmentNameInput.text()
            output_dep_name = Department.delete_from_file(department_name)
            self.ui.scrollAreaDepart.setText(output_dep_name)
        # Add a department, call the add function 
        if self.ui.depAddBox.isChecked():
            department_name = self.ui.departmentNameInput.text()
            department_description = self.ui.depDescTextBox.toPlainText()
            new_dep = Department.add_department(department_name, department_description)
            self.ui.scrollAreaDepart.setText(new_dep)      

    def unCheckItem(self):

        sender_checkbox = self.sender()
        self.ui.scrollAreaItem.clear()

        if sender_checkbox == self.ui.itemAddCheckBox and self.ui.itemAddCheckBox.isChecked():
            self.ui.itemDeleteCheckBox.setChecked(False)
            self.ui.itemSearchCheckBox.setChecked(False)
            self.ui.itemNameLabel.show()
            self.ui.itemNameInput.show()
            self.ui.itemRevInput.show()
            self.ui.itemRevLabel.show()
            self.ui.itemQuantityLabel.show()
            self.ui.itemQuantInput.show()
            self.ui.itemInvFrame.hide()

        elif sender_checkbox == self.ui.itemDeleteCheckBox and self.ui.itemDeleteCheckBox.isChecked():
            self.ui.itemAddCheckBox.setChecked(False)
            self.ui.itemSearchCheckBox.setChecked(False)
            self.ui.itemNameLabel.show()
            self.ui.itemNameInput.show()
            self.ui.itemRevInput.hide()
            self.ui.itemRevLabel.hide()
            self.ui.itemQuantityLabel.hide()
            self.ui.itemQuantInput.hide()
            self.ui.itemInvFrame.hide()

        elif sender_checkbox == self.ui.itemSearchCheckBox and self.ui.itemSearchCheckBox.isChecked():
            self.ui.itemDeleteCheckBox.setChecked(False)
            self.ui.itemAddCheckBox.setChecked(False)
            self.ui.itemNameLabel.show()
            self.ui.itemNameInput.show()
            self.ui.itemRevInput.hide()
            self.ui.itemRevLabel.hide()
            self.ui.itemQuantityLabel.hide()
            self.ui.itemQuantInput.hide()
            self.ui.itemInvFrame.show()


    def showItemInfo(self):

        if self.ui.itemAddCheckBox.isChecked():
            itemName = self.ui.itemNameInput.text()
            itemRev = self.ui.itemRevInput.text()
            itemRev = float(itemRev)
            itemQuanitiy = self.ui.itemQuantInput.text()
            itemQuanitiy = int(itemQuanitiy)
            newItem = Item.add_item(itemName, itemRev, itemQuanitiy)
            self.ui.scrollAreaItem.setText(newItem)
        
        if self.ui.itemDeleteCheckBox.isChecked():
            itemName = self.ui.itemNameInput.text()
            deletedItem = Item.delete_item(itemName)
            self.ui.scrollAreaItem.setText(deletedItem)

        if self.ui.itemSearchCheckBox.isChecked():
            itemName = self.ui.itemNameInput.text()
            searchedItem = Item.search_item(itemName)
            self.ui.scrollAreaItem.setText(searchedItem)
            curr_quantity = Item.item_count(itemName)
            self.ui.invProgessBar.setValue(curr_quantity)
            if curr_quantity < 50:
                self.ui.invProgessBar.setStyleSheet(
                   "QProgressBar"
                          "{"
                          "background-color : white;"
                          "border : 1px"
                          "}"
                    "QProgressBar::chunk { background-color: red;}"
                )
            else:
                self.ui.invProgessBar.setStyleSheet(
                "QProgressBar"
                          "{"
                          "background-color : white;"
                          "border : 1px"
                          "}"
                "QProgressBar::chunk { background-color: green;}"
                )

       
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.currentUser = None

        # Connect the login button to the login function
        self.ui.login_enter.clicked.connect(self.loginFunction)
        self.ui.enterButton.clicked.connect(self.createAccountSavestoFile)
        #self.getCurrentUser()

    def loginFunction(self):
        username = self.ui.username_login.text()
        user_password = self.ui.passwordLogin.text()
        if User.searchUser(username, user_password):
            self.currentUser = username
            self.openSaleInterface(username)  # Pass the username when opening Sale Interface
            self.close()
        else:
            self.showErrorDialog('Incorrect Username or Password')
   
    def getCurrentUser(self):
        return self.currentUser

    def createAccountSavestoFile(self):
        firstName = self.ui.firstName.text()
        lastName = self.ui.lastName.text()
        email = self.ui.userEmail.text()
        username = self.ui.username.text()
        password = self.ui.userPassword.text()
        companyName = self.ui.companyName.text()
        User.createUser(firstName, lastName, email, username, password, companyName)
        self.showSuccessDialog('You have created a new account')

    def openSaleInterface(self, username):
        self.sale_interface_window = SaleInterfaceWindow(username)  # Pass the username
        self.sale_interface_window.show()

    def showErrorDialog(self, message):
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(message)

    def showSuccessDialog(self,message):
        successMessage = QMessageBox(self)
        successMessage.setWindowTitle("Success")
        successMessage.setText(message)
        successMessage.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())