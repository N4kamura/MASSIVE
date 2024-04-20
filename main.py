from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QErrorMessage,QProgressBar
from PyQt5.QtCore import QDir
import warnings
from interface import Ui_MainWindow
from massive import start_changes
import sys

warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.open_file)
        self.ui.pushButton_2.clicked.connect(self.start)
        self.ui.progressBar = QProgressBar()

    def open_file(self):
        self.folder = QFileDialog.getExistingDirectory(self, "Open Folders", QDir.homePath())
        if self.folder:
            self.ui.lineEdit.setText(self.folder)

    def start(self):
        try:
            start_changes(self.folder, self.ui.progressBar)
        except Exception as inst:
            error = QErrorMessage(self)
            return error.showMessage(str(inst))
    
def main():
    app = QApplication(sys.argv)
    app.processEvents()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()