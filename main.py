from PyQt5 import QtCore, QtGui, QtWidgets

#custom code start
from userInput import Ui_Dialog
from vpython import mag, sphere, vector, color, rate
import random, math
def gforce(p1, p2):
    G = 1
    r_vec = p1.pos - p2.pos
    r_mag = mag(r_vec)
    r_hat = r_vec/r_mag
    force_mag = G * p1.mass * p2.mass / r_mag ** 2
    force_vec = -force_mag * r_hat
    return force_vec

bodiesDict1 = {
    'sun': {'position': (0, 0, 0), 'radius': 1, 'color': 'yellow', 'mass': 100000, 'momentum': (0, 0, 0), 'trail':True},
    'planet1': {'position': (2, 0, 0), 'radius': 0.5, 'color': 'magenta', 'mass': 1.1, 'momentum': (0, 250, 0), 'trail':True},
    'planet2': {'position': (5, 0, 0), 'radius': 0.5, 'color': 'orange', 'mass': 3, 'momentum': (0, 430, 0), 'trail':True},
    'planet3': {'position': (10, 0, 0), 'radius': 0.5, 'color': 'red', 'mass': 6, 'momentum': (0, -600, 0), 'trail':True},
    'planet4': {'position': (20, 0, 0), 'radius': 0.5, 'color': 'green', 'mass': 12, 'momentum': (0, -900, 0), 'trail':True},
    'planet5': {'position': (30, 0, 0), 'radius': 0.5, 'color': 'purple', 'mass': 20, 'momentum': (0, -1200, 0), 'trail':True},
    'planet6': {'position': (-60, 0, 0), 'radius': 0.5, 'color': 'cyan', 'mass': 40, 'momentum': (0, -1500, 0), 'trail':True},
    'planet7': {'position': (50, 0, 0), 'radius': 0.5, 'color': 'white', 'mass': 50, 'momentum': (0, -2200, 0), 'trail':True},
    'planet8': {'position': (-10, 20, 0), 'radius': 0.3, 'color': 'white', 'mass': 0.5, 'momentum': (0, -20, 0), 'trail':True},
}
bodiesDict2 = {
    'planet1': {'position': (0, 0, 0), 'radius': 10000, 'color': 'yellow', 'mass': 1e14, 'momentum': (0, 0, 0), 'trail':True},
    'planet2': {'position': (100000, 0, 0), 'radius': 50, 'color': 'magenta', 'mass': 1e9, 'momentum': (0, 3e13, 0), 'trail':True},
    'planet3': {'position': (100200, 0, 0), 'radius': 20, 'color': 'white', 'mass': 1e5, 'momentum': (0, 3.2e9, 0), 'trail':True},
    'planet4': {'position': (-100000, 0, 0), 'radius': 50, 'color': 'magenta', 'mass': 1e9, 'momentum': (0, -3e13, 0), 'trail':True},
    'planet5': {'position': (-100200, 0, 0), 'radius': 20, 'color': 'white', 'mass': 1e5, 'momentum': (0, -3.2e9, 0), 'trail':True},
    'planet6': {'position': (0, 100000, 0), 'radius': 50, 'color': 'magenta', 'mass': 1e9, 'momentum': (3e13, 0, 0), 'trail':True},
    'planet7': {'position': (0, 100200, 0), 'radius': 20, 'color': 'white', 'mass': 1e5, 'momentum': (3.2e9, 0, 0), 'trail':True},
    'planet8': {'position': (0, -100000, 0), 'radius': 50, 'color': 'magenta', 'mass': 1e9, 'momentum': (-3e13, 0, 0), 'trail':True},
    'planet9': {'position': (0, -100200, 0), 'radius': 20, 'color': 'white', 'mass': 1e5, 'momentum': (-3.2e9, 0, 0), 'trail':True}
}
bodiesDict3 = {
    'sun1': {'position': (500, 0, 0), 'radius': 10, 'color': 'red', 'mass': 1e9, 'momentum': (0, 10e11, 0), 'trail': True},
    'sun2': {'position': (-500, 0, 0), 'radius': 10, 'color': 'red', 'mass': 1e9, 'momentum': (0, -10e11, 0), 'trail': True},
    'sun3': {'position': (0, 500, 0), 'radius': 10, 'color': 'red', 'mass': 1e9, 'momentum': (-10e11, 0, 0), 'trail': True},
    'sun4': {'position': (0, -500, 0), 'radius': 10, 'color': 'red', 'mass': 1e9, 'momentum': (10e11, 0, 0), 'trail': True},
    'planet1': {'position': (550, 0, 0), 'radius': 2, 'color': 'blue', 'mass': 1, 'momentum': (0, 5e3, 0), 'trail': True},
    'planet2': {'position': (-550, 0, 0), 'radius': 2, 'color': 'yellow', 'mass': 1, 'momentum': (0, -5e3, 0), 'trail': True},
    'planet3': {'position': (0, 550, 0), 'radius': 2, 'color': 'green', 'mass': 1, 'momentum': (-5e3, 0, 0), 'trail': True},
    'planet4': {'position': (0, -550, 0), 'radius': 2, 'color': 'purple', 'mass': 1, 'momentum': (5e3, 0, 0), 'trail': True}
}

def SSS(reference):
    ref = reference
    bodies = []
    for item in ref.values():
        bodies.append( sphere( pos=vector(item['position'][0], item['position'][1], item['position'][2]), radius=item['radius'], color=getattr(color, item['color']), mass=item['mass'], momentum=vector(item['momentum'][0], item['momentum'][1], item['momentum'][2]), make_trail=item['trail'] ) )
    
    dt = 0.0001
    t = 0
    while True:
        rate(1000)
        for i in range(len(bodies)):
            bodies[i].force = vector(0, 0, 0)
            for j in range(len(bodies)):
                if i != j:
                    bodies[i].force += gforce(bodies[i], bodies[j])
        for i in range(len(bodies)):
            bodies[i].momentum += bodies[i].force * dt
        for i in range(len(bodies)):
            bodies[i].pos += bodies[i].momentum/bodies[i].mass * dt
        t += dt
#end

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.simulateButton = QtWidgets.QPushButton(self.centralwidget)
        self.simulateButton.setGeometry(QtCore.QRect(530, 440, 250, 70))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(18)
        font.setItalic(True)
        self.simulateButton.setFont(font)
        self.simulateButton.setAutoDefault(True)
        self.simulateButton.setFlat(False)
        self.simulateButton.setObjectName("simulateButton")
        self.preset1 = QtWidgets.QRadioButton(self.centralwidget)
        self.preset1.setGeometry(QtCore.QRect(660, 100, 110, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.preset1.setFont(font)
        self.preset1.setChecked(True)
        self.preset1.setObjectName("preset1")
        self.preset3 = QtWidgets.QRadioButton(self.centralwidget)
        self.preset3.setGeometry(QtCore.QRect(660, 160, 110, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.preset3.setFont(font)
        self.preset3.setObjectName("preset3")
        self.custom = QtWidgets.QRadioButton(self.centralwidget)
        self.custom.setGeometry(QtCore.QRect(660, 200, 110, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.custom.setFont(font)
        self.custom.setObjectName("custom")
        self.preset2 = QtWidgets.QRadioButton(self.centralwidget)
        self.preset2.setGeometry(QtCore.QRect(660, 130, 110, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.preset2.setFont(font)
        self.preset2.setObjectName("preset2")
        self.addBodyButton = QtWidgets.QPushButton(self.centralwidget)
        self.addBodyButton.setGeometry(QtCore.QRect(660, 280, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.addBodyButton.setFont(font)
        self.addBodyButton.setObjectName("addBodyButton")
        self.heading = QtWidgets.QLabel(self.centralwidget)
        self.heading.setGeometry(QtCore.QRect(110, 10, 500, 80))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(25)
        self.heading.setFont(font)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setObjectName("heading")
        self.bodyList = QtWidgets.QListWidget(self.centralwidget)
        self.bodyList.setGeometry(QtCore.QRect(50, 100, 600, 300))
        self.bodyList.setAutoFillBackground(True)
        self.bodyList.setObjectName("bodyList")
        self.deleteBodyButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteBodyButton.setGeometry(QtCore.QRect(660, 320, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.deleteBodyButton.setFont(font)
        self.deleteBodyButton.setObjectName("deleteBodyButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #custom code
        self.switchPreset(self.preset1)
        self.preset1.toggled.connect(lambda: self.switchPreset(self.preset1))
        self.preset2.toggled.connect(lambda: self.switchPreset(self.preset2))
        self.preset3.toggled.connect(lambda: self.switchPreset(self.preset3))
        self.custom.toggled.connect(lambda: self.switchPreset(self.custom))

        self.simulateButton.clicked.connect(self.start_sim)

        self.addBodyButton.clicked.connect(self.take_input)
        self.deleteBodyButton.clicked.connect(self.deleteItem)
        #end  

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Solar System Simulator by Faizan"))
        self.simulateButton.setText(_translate("MainWindow", "Simulate"))
        self.preset1.setText(_translate("MainWindow", "Preset 1"))
        self.preset3.setText(_translate("MainWindow", "Preset 3"))
        self.custom.setText(_translate("MainWindow", "Custom Preset"))
        self.preset2.setText(_translate("MainWindow", "Preset 2"))
        self.addBodyButton.setText(_translate("MainWindow", "Add Body"))
        self.heading.setText(_translate("MainWindow", "Solar System Simulator by Faizan Ali"))
        self.deleteBodyButton.setText(_translate("MainWindow", "Delete Body"))
    
    #custom code
    def switchPreset(self, rb):
        self.bodyList.clear()

        if self.preset1 == rb:
            for key, val in bodiesDict1.items():
                body = f"""
                Name: {key}
                Position: {val['position']}
                Momentum: {val['momentum']}
                Radius: {val['radius']}
                Mass: {val['mass']}
                Color: {val['color']}
                Trails: {val['trail']}"""
                self.bodyList.addItem(body)
            self.addBodyButton.setEnabled(False)
            self.deleteBodyButton.setEnabled(False)
        
        elif self.preset2 == rb:
            for key, val in bodiesDict2.items():
                body = f"""
                Name: {key}
                Position: {val['position']}
                Momentum: {val['momentum']}
                Radius: {val['radius']}
                Mass: {val['mass']}
                Color: {val['color']}
                Trails: {val['trail']}"""
                self.bodyList.addItem(body)
            self.addBodyButton.setEnabled(False)
            self.deleteBodyButton.setEnabled(False)
        
        elif self.preset3 == rb:
            for key, val in bodiesDict3.items():
                body = f"""
                Name: {key}
                Position: {val['position']}
                Momentum: {val['momentum']}
                Radius: {val['radius']}
                Mass: {val['mass']}
                Color: {val['color']}
                Trails: {val['trail']}"""
                self.bodyList.addItem(body)
            self.addBodyButton.setEnabled(False)
            self.deleteBodyButton.setEnabled(False)
        
        elif self.custom == rb:
            with open("custom") as f:
                bodiesDictCustom = eval(f.read())
            for key, val in bodiesDictCustom.items():
                body = f"""
                Name: {key}
                Position: {val['position']}
                Momentum: {val['momentum']}
                Radius: {val['radius']}
                Mass: {val['mass']}
                Color: {val['color']}
                Trails: {val['trail']}"""
                self.bodyList.addItem(body)
            self.addBodyButton.setEnabled(True)
            self.deleteBodyButton.setEnabled(True)
    
    def start_sim(self):
        if self.preset1.isChecked(): SSS(bodiesDict1)
        elif self.preset2.isChecked(): SSS(bodiesDict2)
        elif self.preset3.isChecked(): SSS(bodiesDict3)
        elif self.custom.isChecked():
            with open("custom") as f:
                bodiesDictCustom = eval(f.read())
            if bodiesDictCustom:
                SSS(bodiesDictCustom)
            else:
                print("Sorry, cannot simulate nothing")
    
    def deleteItem(self):
        items = self.bodyList.selectedItems()
        if not items: return
        with open('custom') as f:
            customDict = eval(f.read())
        for item in items:
            self.bodyList.takeItem(self.bodyList.row(item))
            body = item.text().split('\n')[1].strip()[6:].lower()
            del customDict[body]
        with open('custom', 'w') as f:
            f.write(str(customDict))
      
    def take_input(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
    #end


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
