import sys
from typing import Dict
from PyQt6.QtCore import Qt,QSettings,QDate
from PyQt6.QtGui import QKeySequence, QIcon, QPixmap, QTextOption, QAction, QColor, QTextCharFormat, QFont, QTextCursor, QIntValidator
from PyQt6.QtWidgets import *
from components import *

APP_DETAILS = {
    "title": "Zeta2 Specifiche",
    "author": "Patric Pintescul",
    "version": "1.0",
    "app-name": "z2-doc-creator",
}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("main-window")

        self.settings = QSettings(APP_DETAILS["author"], APP_DETAILS["app-name"])

        self.restoreGeometry(self.settings.value("geometry", self.saveGeometry()))

        self.setWindowTitle(APP_DETAILS["title"])
        self.setContentsMargins(0,0,0,0)

        self.setMinimumSize(900,700)

        self.setCentralWidget(CentralWidget(self))

    def closeEvent(self, close_event) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(close_event)


class CentralWidget(QWidget):
    def __init__(self, parent: MainWindow | None = None) -> None:
        super().__init__(parent)
        self.p = parent
        self.setObjectName("central-widget")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(QVBoxLayout())

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.init_ui()

    def init_ui(self):
        # RULLIERE START
        self.rulliere_title = Title("Rulliere")
        self.rulliere_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.rulliere_horizontal_1 = QHBoxLayout()
        self.num_rulliere = IntRow("Numero rulliere", 0, True, validator=QIntValidator(0,1000))
        self.num_fotocellule = IntRow("Numero di fotocellule per rulliera", 0, True, validator=QIntValidator(0, 1000))
        self.num_fotocellule_aggiuntive = IntRow("Numero di fotocellule aggiuntive", 0, True, validator=QIntValidator(0, 1000))
        self.util_fot_agg = StringsInput("Specificare utilità fotocellule aggiuntive",8)
        self.tbl1 = DynamicTable("Posizione rulliera, KW motore e tipo di comando",16,5,["Bidirezionale","Comando","Posizione","Presenza freno","Kw/Tipo"],["checkbox:Si","lineedit","lineedit","checkbox:Presente","lineedit"])
        self.tbl1.setMinimumHeight(500)
        self.blocco_pallet_lat = PresenceRow("Blocco pallet laterale",["1 valvola bistabile","1 Reed di indietro"],2)
        self.blocco_pallet_frontale = PresenceRow("Blocco pallet frontale",["1 valvola bistabile","1 Reed di basso, 1 Reed di alto"],2)
        self.rulliere_horizontal_1.addWidget(self.num_rulliere)
        self.rulliere_horizontal_1.addWidget(self.num_fotocellule)
        self.scroll_widget.layout().addWidget(self.rulliere_title)
        self.scroll_widget.layout().addLayout(self.rulliere_horizontal_1)
        self.scroll_widget.layout().addWidget(self.num_fotocellule_aggiuntive)
        self.scroll_widget.layout().addWidget(self.util_fot_agg)
        self.scroll_widget.layout().addWidget(self.tbl1)
        self.scroll_widget.layout().addWidget(self.blocco_pallet_lat)
        self.scroll_widget.layout().addWidget(self.blocco_pallet_frontale)
        # RULLIERE END

        # TRASPORTO START
        self.trasporto_title = Title("Trasporto")
        self.trasporto_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tbl2 = DynamicTable("Dettagli", 20, 6, [
                                "Tipo di trasporto", "Presenza", "Comando", "Presenza freno", "Note", "Kw"],
                                ["lineedit", "checkbox:Presente", "combobox:,diretto,inverter", "checkbox:Si", "lineedit", "lineedit"])
        self.tbl2.setMinimumHeight(500)
        self.fot_sens_valv_aggiuntive = StringsInput("Specificare fotocellule, sensori o valvole aggiuntive",10)
        self.scroll_widget.layout().addWidget(self.trasporto_title)
        self.scroll_widget.layout().addWidget(self.tbl2)
        self.scroll_widget.layout().addWidget(self.fot_sens_valv_aggiuntive)
        # TRASPORTO END

        # ASCENSORE START
        self.ascensore_title = Title("Ascensore")
        self.ascensore_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tbl3 = DynamicTable("Specifiche", 1, 5, [
                                "Motore ascensore", "Comando", "Freno", "Bidirezionale", "Kw"],
                                ["checkbox:Presente", "combobox:,diretto,inverter", "checkbox:Si", "checkbox:Si", "lineedit"])
        self.sens_ascensore = PresenceRow("Sensori ascensore", [
            "Fotocellula livello lattine", "Proximity limite basso",
            "Proximity limite alto", "Fotocellula presenza pallet",
            "Encoder:RETE O DIGITALE (MARCA:)","2 proximity in serie, rottura catena"], 10)
        self.pinza_presa_falda = PresenceRow("Pinza Presa Falda", [
            "1 Valvola bistabile", "Reed di indietro"], 3)
        self.pareti = PresenceRow("Pareti", [
            "1 Valvola bistabile", "Reed di aperto"], 3)

        self.scroll_widget.layout().addWidget(self.ascensore_title)
        self.scroll_widget.layout().addWidget(self.tbl3)
        self.scroll_widget.layout().addWidget(self.sens_ascensore)
        self.scroll_widget.layout().addWidget(self.pinza_presa_falda)
        self.scroll_widget.layout().addWidget(self.pareti)
        # ASCENSORE END

        # TRASLATORE START
        self.traslatore_title = Title("Traslatore")
        self.traslatore_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.h_traslatore_layout = QHBoxLayout()
        self.tbl4 = DynamicTable("Specifiche", 1, 5, [
            "Motore traslatore", "Comando", "Freno", "Bidirezionale", "Kw"],
            ["checkbox:Presente", "combobox:,diretto,inverter", "checkbox:Si", "checkbox:Si", "lineedit"])
        self.left_traslatore_l = QVBoxLayout()
        self.sens_traslatore = PresenceRow("Sensori traslatore", [
            "Proximity avanti","Proximity indietro","Encoder:RETE O DIGITALE (MARCA:)", "Sensore magazzino falde pieno"], 12)
        self.pinza_aspira_falda = PresenceRow("Pinze Aspira Falda", [
            "1 valvola bistabile","6 reed in serie di pinze basse","Fotocellula presenza falda"], 3)
        self.pinza_presa_cornice = PresenceRow("Pinze Presa Cornice", [
            "2 Valvole bistabile",
            "4 reed in serie di aperto",
            "4 reed in serie di alto"], 3)
        self.pressori_laterali = PresenceRow("Pressori laterali", [
            "1 Valvola bistabile",
            "2 reed in serie di aperto"], 3)
        self.pressore_frontale = PresenceRow("Pressore frontale", [
            "1 Valvola bistabile",
            "1 reed di aperto",
            "1 reed di chiuso"], 3)
        self.scroll_widget.layout().addWidget(self.traslatore_title)
        self.scroll_widget.layout().addWidget(self.tbl4)
        self.h_traslatore_layout.addWidget(self.sens_traslatore)
        self.left_traslatore_l.addWidget(self.pinza_aspira_falda)
        self.left_traslatore_l.addWidget(self.pinza_presa_falda)
        self.left_traslatore_l.addWidget(self.pressori_laterali)
        self.left_traslatore_l.addWidget(self.pressore_frontale)
        self.h_traslatore_layout.addLayout(self.left_traslatore_l)
        self.scroll_widget.layout().addLayout(self.h_traslatore_layout)
        # TRASLATORE END

        # MAGAZZINO PALLET START
        self.magpallet_title = Title("Magazzino pallet")
        self.magpallet_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tbl4 = DynamicTable("Specifiche", 1, 5, [
            "Motore traslatore", "Comando", "Freno", "Bidirezionale", "Kw"],
            ["checkbox:Presente", "combobox:,diretto,inverter", "checkbox:Si", "checkbox:Si", "lineedit"])
        self.sens_magpallet = PresenceRow("Sensori traslatore", [
            "Proximity limite alto",
            "Proximity limite basso",
            "Proximity posizione intermedia",
            "Encoder",
            "Reed braccia aperte",
            "Valvola bistabile braccia",
            "Fotocellula magazzino pieno"], 10)

        self.scroll_widget.layout().addWidget(self.traslatore_title)
        self.scroll_widget.layout().addWidget(self.tbl4)
        self.scroll_widget.layout().addWidget(self.sens_magpallet)
        # MAGAZZINO PALLET END

        # SCAMBIO INFO START
        self.scambioinfo_title = Title("Scambio info")
        self.scambioinfo_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.scambioinfo_h = QHBoxLayout()
        self.scambioinfo_1_v = QVBoxLayout()
        self.scambioinfo_2_v = QVBoxLayout()
        self.tipo_scambioinfo_linea = PresenceRow("Tipo di scambio info con linea", [
            "Rete",
            "Cablato"], 2)
        self.scambioinfo_linea = PresenceRow("Scambio info con linea", [
            "2 segnali uscita",
            "1 segnale in ingresso"], 2)
        self.tipo_scambioinfo_linea_con = PresenceRow("Tipo di scambio info con XXXXX", [
            "Rete",
            "Cablato"], 2, editable=True)
        self.scambioinfo_linea_con = PresenceRow("Tipo di scambio info con XXXXX", [
            "2 segnali uscita",
            "1 segnale in ingresso"], 2,editable=True)

        self.scroll_widget.layout().addWidget(self.scambioinfo_title)
        self.scambioinfo_1_v.addWidget(self.tipo_scambioinfo_linea)
        self.scambioinfo_1_v.addWidget(self.scambioinfo_linea)
        self.scambioinfo_2_v.addWidget(self.tipo_scambioinfo_linea_con)
        self.scambioinfo_2_v.addWidget(self.scambioinfo_linea_con)
        self.scambioinfo_h.addLayout(self.scambioinfo_1_v)
        self.scambioinfo_h.addLayout(self.scambioinfo_2_v)
        self.scroll_widget.layout().addLayout(self.scambioinfo_h)
        # SCAMBIO INFO END

        # BOX START
        self.boxtitle = Title("Box")
        self.boxtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.boxuscitapallet = StringsInput(
            "Box uscita pallet", 8)  # horizontal with boxmagazzinopallet
        self.boxmagazzinopallet = StringsInput(
            "Box magazzino pallet", 8)  # horizontal with boxuscitapallet
        self.boxemg1 = StringsInput(
            "Box emergenza 1", 8) # horizontal with boxemg2
        self.boxemg2 = StringsInput(
            "Box emergenza 2", 8)  # horizontal with boxemg1
        self.boxcaricopallet = StringsInput(
            "Box carico pallet", 8)
        self.boxuscita_magazzino_l = QHBoxLayout()
        self.boxuscita_magazzino_l.addWidget(self.boxuscitapallet)
        self.boxuscita_magazzino_l.addWidget(self.boxmagazzinopallet)
        self.boxemg_l = QHBoxLayout()
        self.boxemg_l.addWidget(self.boxemg1)
        self.boxemg_l.addWidget(self.boxemg2)
        self.scroll_widget.layout().addWidget(self.boxtitle)
        self.scroll_widget.layout().addLayout(self.boxuscita_magazzino_l)
        self.scroll_widget.layout().addLayout(self.boxemg_l)
        self.scroll_widget.layout().addWidget(self.boxcaricopallet)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())