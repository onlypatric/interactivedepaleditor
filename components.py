
import sys
from typing import Dict, List, Tuple
from PyQt6.QtCore import Qt, QSettings, QDate
from PyQt6.QtGui import QKeySequence, QIcon, QPixmap, QTextOption, QAction, QColor, QTextCharFormat, QFont, QTextCursor, QIntValidator,QDoubleValidator,QValidator
from PyQt6.QtWidgets import *

class Title(QLabel):
    def __init__(self, text,bold:bool=True,fontSize:int=24):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"font-size: {fontSize}px;{'font-weight:bold;' if bold else ''}")

class IntRow(QWidget):
    def __init__(self, label:str, default:int=0, isPos:bool=False,validator:QValidator=QDoubleValidator()):
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10,10,10,10)
        self.setLayout(self.main_layout)

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        self.main_layout.addStretch()

        if isPos:
            self.pos_label = QLabel("N°")
            self.pos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.pos_label)

        self.input = QLineEdit(str(default))
        self.input.setValidator(validator)
        self.main_layout.addWidget(self.input)
        if isPos:
            self.input.setFixedWidth(100)
        # Set the background color for this widget
        self.setStyleSheet("QWidget#IntRow { background-color: rgb(139,180,224);border:1px solid black }")
        # Set the object name for this widget
        self.setObjectName("IntRow")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    def get(self) -> int:
        if self.input.text() == "":
            return 0
        return int(self.input.text())
    

class StringRow(QWidget):
    def __init__(self, label: str, default: str = "SPECIFICHE DEPALETIZZATORE", fontSize: int = 24, fixed: bool = True):
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        self.main_layout.addStretch()

        self.input = QLineEdit(str(default))
        self.input.setFixedWidth(300 if fixed else 0)
        self.main_layout.addWidget(self.input)
        # Set the background color for this widget
        self.setStyleSheet(
            "QWidget#StringRow { background-color: rgb(139,180,224);border:1px solid black }")
        # Set the object name for this widget
        self.setObjectName("StringRow")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def get(self) -> int:
        return self.input.text()

class GroupLineEdits(QWidget):
    def __init__(self,label:str,lineEditCount:int=4):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.label = QLabel(label)
        self.main_layout.addWidget(self.label)

        self.lineedit_layout = QVBoxLayout()
        self.lineedit_layout.setContentsMargins(0, 0, 0, 0)

        self.lineEdits = []
        for i in range(lineEditCount):
            d = QLineEdit()
            self.lineEdits.append(d)
            self.lineedit_layout.addWidget(d)
        self.main_layout.addLayout(self.lineedit_layout)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Set the background color for this widget
        self.setStyleSheet("QWidget#GroupLineEdits { background-color: rgb(139,180,224);border:1px solid black }")
        # Set the object name for this widget
        self.setObjectName("GroupLineEdits")
    def get(self) -> list:
        return [e.text() for e in self.lineEdits]
    

class DynamicTable(QWidget):
    def __init__(self, title: str, rows: int, columns: int, column_headers: list, cell_types: list):
        super().__init__()

        # Set up the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        # Create and style the title label
        title_label = Title(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(title_label)

        # Create the table widget
        self.table_widget = QTableWidget(rows, columns)
        self.main_layout.addWidget(self.table_widget)

        # Set column headers
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        # Set up the cell types
        self.cell_types = cell_types

        # Populate the table with the specified cell types
        for row in range(rows):
            for col in range(columns):
                item = self.create_table_item(cell_types[col].lower(),row,col)
                self.table_widget.setItem(row, col, item)
        self.setObjectName("DynamicTable")
        self.setStyleSheet(
            "QWidget#DynamicTable { background-color: rgb(139,180,224); border: 1px solid black; padding:5px }")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def create_table_item(self, cell_type: str,row:int,col:int) -> QTableWidgetItem:
        if cell_type.startswith("checkbox"):
            item = QTableWidgetItem(cell_type.split(":")[1])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            return item
        elif cell_type.startswith("combobox"):
            item = QTableWidgetItem()
            combobox = QComboBox()
            combobox.addItems(cell_type.split(":")[1].split(","))
            self.table_widget.setCellWidget(row, col, combobox)
            return item
        elif cell_type == "lineedit":
            item = QTableWidgetItem()
            item.setData(Qt.ItemDataRole.DisplayRole, "")
            return item
        elif cell_type == "label":
            item = QTableWidgetItem()
            item.setData(Qt.ItemDataRole.DisplayRole, "Label Text")
            return item

    def get(self) -> list:
        result = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    if isinstance(item, QTableWidgetItem):
                        row_data.append(item.text())
                    elif isinstance(item, QCheckBox):
                        row_data.append(item.isChecked())
            result.append(row_data)
        return result

    def get_value(self, row: int, col: int):
        item = self.table_widget.item(row, col)
        if item:
            if isinstance(item, QTableWidgetItem):
                return item.text()
            elif isinstance(item, QCheckBox):
                return item.isChecked()
        return None

class StringsInput(QWidget):
    def __init__(self, label: str, count:int=4):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.label)

        self.main_layout.addStretch()

        self.lines = []
        for i in range(count):
            l = QLineEdit()
            self.main_layout.addWidget(l)
            self.lines.append(l)
        # Set the background color for this widget
        self.setStyleSheet(
            "QWidget#StringsInput { background-color: rgb(139,180,224);border:1px solid black }")
        # Set the object name for this widget
        self.setObjectName("StringsInput")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def get(self) -> int:
        return [e.text() for e in self.lines]

class PresenceRow(QWidget):
    def __init__(self,mainLabel:str,
                 miniLabels:List[str],
                 rowCount:int,
                 chechBoxText:str="Presente",
                 editable=True):
        super().__init__()

        # Set up the main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(4, 0, 4, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Create and style the title label
        if editable:
            self.title_label = QLineEdit(mainLabel)
            self.main_layout.addWidget(self.title_label)
        else:
            self.title_label = QLabel(mainLabel)
            self.title_label.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
            self.main_layout.addWidget(self.title_label)
            self.main_layout.addStretch()

        self.presence_layout = QVBoxLayout()
        self.presence_layout.setContentsMargins(0,0,0,0)
        self.presence_layout.setSpacing(0)
        self.main_layout.addLayout(self.presence_layout)

        self.lines = []
        self.checkboxes = []

        for i in range(rowCount):
            presence_w = QWidget()
            presence_l = QHBoxLayout()
            presence_l.setContentsMargins(0, 0, 0, 0)
            presence_l.setSpacing(0)
            presence_w.setLayout(presence_l)
            self.presence_layout.addWidget(presence_w)
            lbl = QLineEdit(miniLabels[i] if len(miniLabels) > i else "")
            lbl.setStyleSheet("padding:5px;background-color:azure;margin:0px")
            chbx = QCheckBox(chechBoxText)
            chbx.setStyleSheet("padding:5px;background-color:white;margin:0px")

            presence_l.addWidget(lbl)
            presence_l.addWidget(chbx)
            self.lines.append(lbl)
            self.checkboxes.append(chbx)

        self.setObjectName("PresenceRow")
        self.setStyleSheet(
            "QWidget#PresenceRow { background-color: rgb(139,180,224); border: 1px solid black; padding:5px }")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    def get(self) -> Dict[str,bool]:
        return {l.text():c.isChecked() for l,c in zip(self.lines,self.checkboxes)}