from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
import sys
#import ra_dec_2_alt_az



class inputdialog(QWidget):
    def __init__(self, parent = None):
        
        super(inputdialog, self).__init__(parent)
        
        #initializing form
        layout = QFormLayout()
        
        #calculate button
        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.clicked.connect(self.calculate)
        
        self.txt1 = QLineEdit()
        self.txt1.getDouble()
        self.txt1.setMaxLength(6)
        
        
        self.txt2 = QLineEdit()
        self.txt2.getDouble()
        self.txt2.setMaxLength(6)
        
    def calculate(self):
        
        print("This function needs to be written")

def main():

    app = QApplication(sys.argv)
    ex = inputdialog()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


