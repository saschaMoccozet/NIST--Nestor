import sys
import csv
import PyQt5.QtWidgets as Qw
from PyQt5 import QtCore as Qc
from PyQt5.QtGui import QIcon
from PyQt5 import uic

# from app.taggingUI.selectCSVHeadersUI_skeleton import Ui_MainWindow_selectCSVHeaders
qtDesignerFile_selectCSVHeaders = 'selectCSVHeadersUI.ui'
Ui_MainWindow_selectCSVHeaders, QtBaseClass_selectCSVHeaders = uic.loadUiType(qtDesignerFile_selectCSVHeaders)


class MySelectCsvHeadersWindow(Qw.QMainWindow, Ui_MainWindow_selectCSVHeaders):

    def __init__(self, iconPath= None, closeFunction=None):
        Qw.QMainWindow.__init__(self)
        Ui_MainWindow_selectCSVHeaders.__init__(self)
        self.setupUi(self)
        self.closeFunction = closeFunction

        if iconPath:
            self.setWindowIcon(QIcon(iconPath))

        self.buttonGroup_CSVHeaders = Qw.QButtonGroup()
        self.buttonGroup_CSVHeaders.setExclusive(False)

        self.pushButton_selectCSVHeaders_uncheckAll.clicked.connect(
            lambda: self.onClick_check(False))
        self.pushButton_selectCSVHeaders_checkAll.clicked.connect(
            lambda: self.onClick_check(True))

    def set_checkBoxesValues(self, headers):
        """
        create the list of checkbox based on the header attribute
        the header is created using the method set_CSVHeader
        :return:
        """
        self.headers = headers

        y_headerColumn = 0
        x = 0

        self.label_selectCSVHeaders_headerColumn = Qw.QLabel(self.centralwidget)
        self.label_selectCSVHeaders_headerColumn.setObjectName("label_selectCSVHeaders_headerColumn")
        self.label_selectCSVHeaders_headerColumn.setText("Your CSV header\n(check if you want to tag it)")
        self.gridLayout_selectCSVHeaders_editor.addWidget(self.label_selectCSVHeaders_headerColumn, x,y_headerColumn,1,1 )

        x += 1

        self.line1 = Qw.QFrame(self.centralwidget)
        self.line1.setFrameShape(Qw.QFrame.HLine)
        self.line1.setFrameShadow(Qw.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.gridLayout_selectCSVHeaders_editor.addWidget(self.line1, x,y_headerColumn , 1, 1)


        for header in self.headers:
            x += 1

            checkBox = Qw.QCheckBox(self.centralwidget)
            checkBox.setObjectName(f'checkBox_{header}')
            checkBox.setText(header)
            self.gridLayout_selectCSVHeaders_editor.addWidget(checkBox, x, y_headerColumn, 1, 1)
            self.buttonGroup_CSVHeaders.addButton(checkBox)

    def onClick_check(self, check):
        """
        called when we want to set the checkbox to check:True of uncheck:False
        :param check: True: check/ False:uncheck
        :return:
        """
        for button in self.buttonGroup_CSVHeaders.buttons():
            button.setChecked(check)


    def get_checkedButton(self):
        """
        return a list of the text in the button checked
        :return:
        """
        checked = []
        for button in self.buttonGroup_CSVHeaders.buttons():
            if button.isChecked():
                checked.append(button.text())
        return checked

    def set_config(self, config):
        """
        add to the window the values from the config dict
        :param config
        :return:
        """
        if config['file']['filePath_OriginalCSV']['headers'] is not None:
            for button in self.buttonGroup_CSVHeaders.buttons():
                if button.text() in config['file']['filePath_OriginalCSV']['headers']:
                    button.setChecked(True)


    def get_config(self, config):
        """
        replace the given config dict with a new one based on the window values

        it is call when we save the view
        :param config:
        :return:
        """
        checked = []
        for button in self.buttonGroup_CSVHeaders.buttons():
            if button.isChecked():
                checked.append(button.text())

        if checked:
            config['file']['filePath_OriginalCSV']['headers'] = checked
            return True, config
        else:
            Qw.QMessageBox.about(self, 'Can\'t save', "You might want to select at least 1 value")
            return False, None

    # def closeEvent(self, event):
    #     """
    #     trigger when we close the window
    #     :param event:
    #     :return:
    #     """
    #     self.closeFunction(self)

if __name__ == "__main__":
    app = Qw.QApplication(sys.argv)
    window = MySelectCsvHeadersWindow("/Users/sam11/Git/ml-py/app/taggingUI/csv/app_vocab.csv")
    window.show()
    sys.exit(app.exec_())