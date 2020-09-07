from PyQt5 import QtWidgets
from cxema24_com_gui import MyWin
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = MyWin()
    application.show()
    sys.exit(app.exec())

# from PyQt5 import QtCore, QtWidgets, QtSerialPort
#
# class Widget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(Widget, self).__init__(parent)
#         self.message_le = QtWidgets.QLineEdit()
#         self.send_btn = QtWidgets.QPushButton(
#             text="Send",
#             clicked=self.send
#         )
#         self.output_te = QtWidgets.QTextEdit(readOnly=True)
#         self.button = QtWidgets.QPushButton(
#             text="Connect",
#             checkable=True,
#             toggled=self.on_toggled
#         )
#         lay = QtWidgets.QVBoxLayout(self)
#         hlay = QtWidgets.QHBoxLayout()
#         hlay.addWidget(self.message_le)
#         hlay.addWidget(self.send_btn)
#         lay.addLayout(hlay)
#         lay.addWidget(self.output_te)
#         lay.addWidget(self.button)
#
#         self.serial = QtSerialPort.QSerialPort(
#             'COM17',
#             baudRate=QtSerialPort.QSerialPort.Baud115200,
#             readyRead=self.receive
#         )
#
#     @QtCore.pyqtSlot()
#     def receive(self):
#         while self.serial.canReadLine():
#             text = self.serial.readLine().data().decode()
#             text = text.rstrip('\n\r')
#             self.output_te.append(text + "\0")
#
#     @QtCore.pyqtSlot()
#     def send(self):
#         byte_str = f"{self.message_le.text()}\0".encode()
#         self.serial.write(byte_str)
#
#     @QtCore.pyqtSlot(bool)
#     def on_toggled(self, checked):
#         self.button.setText("Disconnect" if checked else "Connect")
#         if checked:
#             if not self.serial.isOpen():
#                 if not self.serial.open(QtCore.QIODevice.ReadWrite):
#                     self.button.setChecked(False)
#         else:
#             self.serial.close()
#
# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     w = Widget()
#     w.show()
#     sys.exit(app.exec_())