from PyQt5 import QtWidgets, QtSerialPort, QtCore
from cxema24_com_init import Ui_MainWindow


class MyWin(QtWidgets.QMainWindow):
    param_gps = {
        'mode': "GPS",
        'freq_min': 4070000,
        'freq_max': 4090000,
        'freq_step': 50
    }

    param_glo = {
        'mode': "GLO",
        'freq_min': 717941,
        'freq_max': 737941,
        'freq_step': 50
    }

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.freq_min.setValue(self.param_gps['freq_min'])
        self.ui.freq_max.setValue(self.param_gps['freq_max'])
        self.ui.freq_step.setValue(self.param_gps['freq_step'])

        self.ui.radio_btn_gps.clicked.connect(self.reinit_values)
        self.ui.radio_btn_glo.clicked.connect(self.reinit_values)
        self.ui.freq_min.editingFinished.connect(self.reinit_param)
        self.ui.freq_max.editingFinished.connect(self.reinit_param)
        self.ui.freq_step.editingFinished.connect(self.reinit_param)
        # self.ui.freq_min.valueChanged.connect(self.reinit_param)
        # self.ui.freq_max.valueChanged.connect(self.reinit_param)
        # self.ui.freq_step.valueChanged.connect(self.reinit_param)
        self.ui.tx_btn.clicked.connect(self.tx_btn_clicked)
        self.ui.refresh_btn.clicked.connect(self.refresh_ports)
        self.setFixedSize(self.size())

        self.refresh_ports()
        self.ser_port = QtSerialPort.QSerialPort("COM0", readyRead=self.receive)

        self.msg = []

    def tx_btn_clicked(self):
        param = self.param_gps if self.ui.radio_btn_gps.isChecked() else self.param_glo
        param['freq_min'] = int(self.ui.freq_min.text())
        param['freq_max'] = int(self.ui.freq_max.text())
        param['freq_step'] = int(self.ui.freq_step.text())
        print(self.ui.ports_box.currentText())
        for key, value in param.items():
            print(f"{key}:", value)
        print("-" * 10)

        self.ser_port.setPortName(self.ui.ports_box.currentText())
        self.ser_port.setBaudRate(self.ser_port.Baud115200)
        self.ser_port.setDataBits(self.ser_port.Data8)
        self.ser_port.setFlowControl(self.ser_port.NoFlowControl)
        self.ser_port.setParity(self.ser_port.NoParity)
        self.ser_port.setStopBits(self.ser_port.OneStop)
        self.ser_port.open(QtCore.QIODevice.ReadWrite)
        self.ser_port.clearError()
        self.ser_port.clear()
        for value in param.values():
            byte_str = bytearray(f"{str(value)}\n".encode('utf-8'))
            self.ser_port.write(byte_str)
        self.ser_port.flush()

        self.msg = []
        # self.ser_port.close()

    def reinit_values(self):
        param = self.param_gps if self.ui.radio_btn_gps.isChecked() else self.param_glo
        param['mode'] = "GPS" if self.ui.radio_btn_gps.isChecked() else "GLO"
        self.ui.freq_min.setValue(param['freq_min'])
        self.ui.freq_max.setValue(param['freq_max'])
        self.ui.freq_step.setValue(param['freq_step'])

    def reinit_param(self):
        param = self.param_gps if self.ui.radio_btn_gps.isChecked() else self.param_glo
        param['mode'] = "GPS" if self.ui.radio_btn_gps.isChecked() else "GLO"
        param['freq_min'] = int(self.ui.freq_min.text())
        param['freq_max'] = int(self.ui.freq_max.text())
        param['freq_step'] = int(self.ui.freq_step.text())

    def refresh_ports(self):
        ports = QtSerialPort.QSerialPortInfo().availablePorts()
        ports_names = []
        for i, port in enumerate(ports):
            ports_names.append(port.portName())

        self.ui.ports_box.clear()
        self.ui.ports_box.addItems(ports_names)

    def receive(self):
        from parser_data import ParserData
        prs_data = ParserData()
        while self.ser_port.canReadLine():
            data_frame = self.ser_port.readLine().data().decode('utf-8')[:-1]
            if data_frame == "":
                if self.msg[-1][0:1] == "g":
                    mode = self.param_gps['mode']
                elif self.msg[-1][0:1] == "l":
                    mode = self.param_glo['mode']
                else:
                    mode = ""
                prs_data.parse_msg(self.msg, mode)
                prs_data.paint_window(mode)
                break
            self.msg.append(data_frame)
            print(data_frame)
