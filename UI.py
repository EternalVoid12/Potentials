from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, \
    QLineEdit, QVBoxLayout, QWidget, QMenu, \
    QCheckBox, QComboBox, QPushButton, QGraphicsTextItem, QGraphicsScene, QGraphicsView, QTextEdit

from PyQt6.QtGui import QIcon, QPixmap, QAction, QTextCursor, QCursor

import sys
import os
from Potentials.Potentials import Nernst, Equations

#file_1 = os.path.join(os.getcwd(), 'pH=0.txt')
#file_2 = os.path.join(os.getcwd(), 'pH=14')
f_1 = open("pH=0.txt")
f_2 = open("pH=14.txt")
A0 = []
B0 = []
for line in f_1:
    A0.append(line)
for line in f_2:
    B0.append(line)
# t = get_t("Term.txt")
g = open("Term.txt")
t = dict()
for line in g:
    lst = line.split()
    sub = lst[0]
    t[sub] = dict()
    if "gas" in lst:
        idx = lst.index("gas")
        t[sub]["gas"] = (lst[idx + 1], lst[idx + 2])
    if "liq" in lst:
        idx = lst.index("liq")
        t[sub]["liq"] = (lst[idx + 1], lst[idx + 2])
    if "cr" in lst:
        idx = lst.index("cr")
        t[sub]["cr"] = (lst[idx + 1], lst[idx + 2])


class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()

        self.create_menu()

        self.setWindowTitle("Potentials 1.1")
        self.setWindowIcon(QIcon('ICON.png'))

        self.Main()

    def create_menu (self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("Main")
        editMenu = menuBar.addMenu("Data")
        helpMenu = menuBar.addMenu("Help")

        # Help menu action
        open_window_action = QAction('About', self)
        open_window_action.triggered.connect(self.open_window)
        helpMenu.addAction(open_window_action)

        # Main menu actions
        open_main_action = QAction('Half-reactions', self)
        open_main_action.triggered.connect(self.Main)
        fileMenu.addAction(open_main_action)

        open_main_action2 = QAction('Reactions', self)
        open_main_action2.triggered.connect(self.main2)
        fileMenu.addAction(open_main_action2)

        open_edit_action = QAction('Half-reactions', self)
        open_edit_action.triggered.connect(self.Edit_window)
        editMenu.addAction(open_edit_action)

    def open_window (self):
        self.text_label = QLabel()
        self.setCentralWidget(self.text_label)
        self.text_label.setText("Help")

    def Edit_window (self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setText("".join(A0))

        # Создание виджета QLineEdit для поиска текста
        self.search_edit = QLineEdit(self)
        # self.search_edit.setPlaceholderText("Поиск текста...")
        # self.search_edit.textChanged.connect(self.search_text)

        # Создание вертикального контейнера и добавление виджетов в него
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        # layout.addWidget(self.search_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search_text (self):
        text = self.search_edit.text()
        print(text)
        found = self.text_edit.find(text)
        print(found)

        if found:
            cursor = self.text_edit.textCursor()
            cursor.select(QTextCursor, )
            self.text_edit.setTextCursor(cursor)
        else:
            cursor = self.text_edit.textCursor()

            cursor.clearSelection()
            self.text_edit.setTextCursor(cursor)

    #            self.text_edit.moveCursor(QTextCursor.atStart)

    def search_in_txt (self):
        txt_to_search = self.search_edit.text()
        try:
            result = self.text_edit.find(txt_to_search)

            if result == False:
                # move cursor to the beginning and restart search
                self.text_edit.moveCursor(QTextCursor.atStart)
                self.text_edit.find(txt_to_search)
        except:
            self.text_edit.moveCursor(QTextCursor.atEnd)
        return

    def main2 (self):
        self.Intro = QLabel("Enter components :")
        self.Intro_T = QLabel("Enter T, K:")
        self.state = QLabel("Enter physical state :")

        self.input = QLineEdit("H2 + O2 = H2O2 ")
        self.input_state = QLineEdit("gas gas liq")
        self.inputT = QLineEdit("293")

        # setting text widget
        self.scene = QGraphicsScene()
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.Intro)
        layout.addWidget(self.input)
        layout.addWidget(self.state)
        layout.addWidget(self.input_state)
        layout.addWidget(self.Intro_T)
        layout.addWidget(self.inputT)
        layout.addWidget(self.text_edit)

        # Button 2
        button = QPushButton("Calculate")
        button.clicked.connect(self.button_clicked_2)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def button_clicked_2 (self):
        try:
            comps = Equations(self.input.text() + " 0")
        except ValueError:
            self.text_edit.setText("Error")
            return
        try:
            states = self.input_state.text().split(" ")
        except ValueError:
            self.text_edit.setText("Error")
        T = float(self.inputT.text())
        try:
            self.text_edit.setText(comps.calc2(T, states, t))
        except KeyError:
            self.text_edit.setText("Error: wrong state or data for this state don't exist")
            return
            # self.state.setText(i)
            # layout = QVBoxLayout()
            # layout.addWidget(self.state)

    #        self.text_edit.setText(Equations.calc(T, eq, p))
    #        T=self.inputT.text()
    #        eq=self.input.text()

    #        p=self.iput_state.text()
    #        if is_number(T):
    #            T=float(T)

    #        self.text_edit.setText(Gibbs(T,eq,p))

    def Main (self):
        self.Intro = QLabel("Input components with space :")
        self.Intro_pH = QLabel("Input pH:")

        self.input = QLineEdit("Cl- H2O2")
        self.inputpH = QLineEdit("0")
        # setting text widget
        self.scene = QGraphicsScene()
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.Intro)
        layout.addWidget(self.input)
        layout.addWidget(self.Intro_pH)
        layout.addWidget(self.inputpH)
        layout.addWidget(self.text_edit)

        # Чекбокс
        self.mod = QCheckBox("Only reactions with с ΔE>0 (ΔG<0)")
        #       mod.setCheckState(Qt.CheckState.Checked)
        #        self.mod.stateChanged.connect(self.show_state)
        layout.addWidget(self.mod)

        # Чекбокс
        self.Check = QCheckBox("Only reactions")
        #       mod.setCheckState(Qt.CheckState.Checked)
        #        self.mod.stateChanged.connect(self.show_state)
        layout.addWidget(self.Check)

        # module switcher
        #        self.switch = QComboBox()
        #        self.switch.addItems(["Nernst", "Gibbs"])
        #        self.switch.activated.connect(self.index_changed)
        #        layout.addWidget(self.switch)

        # Button
        button = QPushButton("Calculate")
        button.clicked.connect(self.button_was_clicked)
        layout.addWidget(button)
        #        QMetaObject.connectSlotsByName(button,self.reactant)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def button_was_clicked (self):
        C = self.Check.checkState()
        #        S = bool(self.switch.activated)
        M = self.mod.checkState()
        B = self.input.text()
        pH = self.inputpH.text()
        if is_number(pH):
            pH = float(self.inputpH.text())
        else:
            self.text_edit.setPlainText("pH - число, десятичную часть записывать через точку.")
            return
        if pH < 7:
            A = A0
        elif pH > 7:
            A = B0
        else:
            A = A0 + B0
        self.text_edit.setText(Nernst(A, B, pH, M, C))


def is_number (str):
    try:
        float(str)
        return True
    except ValueError:
        return False


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
