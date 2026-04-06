import sys
import os
import json
import csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QListWidget, QListWidgetItem,
    QFrame, QStatusBar, QSizePolicy, QGroupBox, QSplitter,
    QMenuBar, QMenu, QToolBar, QMainWindow, QSpacerItem, QLineEdit,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog, QScrollArea,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QSize, QStandardPaths
from PySide6.QtGui import QFont, QIcon, QAction, QPixmap, QColor, QPalette
from birddata import BirdManager

# ─── Config paths ──────────────────────────────────────────────────────────────
CONFIG_FILE = "birdlist_config.json"
BIRDS_FILE  = "birds.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"username": "Tom"}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

# ─── Shared stylesheet: classic Windows XP / Oracle enterprise look ───────────
GLOBAL_STYLE = """
QMainWindow, QWidget {
    background-color: #ECE9D8;
    font-family: "Tahoma", "MS Sans Serif", sans-serif;
    font-size: 11px;
    color: #000000;
}

/* ---------- Buttons ---------- */
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF, stop:0.45 #ECECEC, stop:0.5 #D8D8D8, stop:1 #C8C8C8);
    color: #000000;
    border: 2px solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
    padding: 4px 12px;
    min-height: 22px;
    font-family: "Tahoma", sans-serif;
    font-size: 11px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFF8C0, stop:0.5 #FFE880, stop:1 #D4B800);
}
QPushButton:pressed {
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #C0C0C0, stop:1 #E0E0E0);
    padding-top: 5px;
    padding-left: 13px;
}
QPushButton:disabled {
    color: #808080;
    border-color: #D0D0D0 #D0D0D0 #D0D0D0 #D0D0D0;
}

/* ---------- The big "Enter" button on welcome screen ---------- */
QPushButton#enterBtn {
    font-size: 13px;
    font-weight: bold;
    min-width: 120px;
    min-height: 30px;
    padding: 6px 24px;
}

/* ---------- List ---------- */
QListWidget {
    background-color: #FFFFFF;
    border: 2px solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    font-family: "Tahoma", sans-serif;
    font-size: 11px;
    alternate-background-color: #F0F4FF;
    outline: none;
}
QListWidget::item {
    padding: 3px 6px;
    border-bottom: 1px solid #E8E8E8;
}
QListWidget::item:selected {
    background-color: #316AC5;
    color: #FFFFFF;
}
QListWidget::item:hover:!selected {
    background-color: #D8E4FF;
}

/* ---------- Group boxes ---------- */
QGroupBox {
    border: 2px solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    margin-top: 10px;
    padding-top: 6px;
    font-weight: bold;
    font-size: 11px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 4px;
    left: 8px;
}

/* ---------- Frames / separators ---------- */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #808080;
}

/* ---------- Status bar ---------- */
QStatusBar {
    background-color: #ECE9D8;
    border-top: 1px solid #808080;
    font-size: 10px;
}
QStatusBar::item {
    border: 1px inset #808080;
    border-right: none;
}

/* ---------- Menu ---------- */
QMenuBar {
    background-color: #ECE9D8;
    border-bottom: 1px solid #ACA899;
}
QMenuBar::item {
    padding: 3px 8px;
    background: transparent;
}
QMenuBar::item:selected {
    background-color: #316AC5;
    color: white;
}
QMenu {
    background-color: #FFFFFF;
    border: 1px solid #808080;
}
QMenu::item {
    padding: 4px 20px 4px 24px;
}
QMenu::item:selected {
    background-color: #316AC5;
    color: white;
}
QMenu::separator {
    height: 1px;
    background: #D0D0D0;
    margin: 2px 4px;
}

/* ---------- Toolbar ---------- */
QToolBar {
    background-color: #ECE9D8;
    border-bottom: 1px solid #ACA899;
    spacing: 2px;
    padding: 2px;
}
QToolBar::separator {
    width: 1px;
    background: #ACA899;
    margin: 3px 4px;
}

/* ---------- ComboBox ---------- */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    padding: 1px 4px;
    font-size: 11px;
    min-height: 20px;
}
QComboBox::drop-down {
    border: none;
    width: 16px;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #808080;
    selection-background-color: #316AC5;
    selection-color: white;
}

/* ---------- Table ---------- */
QTableWidget {
    background-color: #FFFFFF;
    border: 2px solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    gridline-color: #D0D0D0;
    font-size: 10px;
}
QTableWidget::item:selected {
    background-color: #316AC5;
    color: white;
}
QHeaderView::section {
    background-color: #D4D0C8;
    border: 1px solid #ACA899;
    padding: 2px 4px;
    font-size: 10px;
    font-weight: bold;
}
"""

# ─── Profile / Username Dialog ─────────────────────────────────────────────────
class ProfileDialog(QDialog):
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Profile")
        self.setFixedSize(320, 160)
        self.setStyleSheet(GLOBAL_STYLE)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel(" User Profile")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        outer.addWidget(title_bar)

        form = QWidget()
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(16, 16, 16, 8)
        form_layout.setSpacing(10)

        info = QLabel("Your name appears throughout the application as the default observer.")
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 10px; color: #444444;")
        form_layout.addWidget(info)

        row = QHBoxLayout()
        lbl = QLabel("Display Name:")
        lbl.setFixedWidth(90)
        lbl.setStyleSheet("font-weight: bold; font-size: 10px;")
        self.name_input = QLineEdit(current_name)
        self.name_input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #808080 #FFFFFF #FFFFFF #808080;
            padding: 1px 4px;
            font-size: 11px;
        """)
        row.addWidget(lbl)
        row.addWidget(self.name_input)
        form_layout.addLayout(row)
        outer.addWidget(form, 1)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ACA899;")
        outer.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 8)
        btn_row.addStretch()
        ok_btn = QPushButton("  Save  ")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def get_name(self):
        return self.name_input.text().strip() or "User"


# ─── New Country Dialog ────────────────────────────────────────────────────────
class NewCountryDialog(QDialog):
    def __init__(self, existing_countries, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start New Life List")
        self.setFixedSize(380, 200)
        self.setStyleSheet(GLOBAL_STYLE)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel(" Start a New Life List")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        outer.addWidget(title_bar)

        form = QWidget()
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(16, 14, 16, 8)
        form_layout.setSpacing(10)

        info = QLabel("No bird records found. Choose a country/region to begin your life list:")
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 10px; color: #444444;")
        form_layout.addWidget(info)

        row = QHBoxLayout()
        lbl = QLabel("Country/Region:")
        lbl.setFixedWidth(100)
        lbl.setStyleSheet("font-weight: bold; font-size: 10px;")

        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("e.g. Australia, New Zealand, UK...")
        self.country_input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #808080 #FFFFFF #FFFFFF #808080;
            padding: 1px 4px;
            font-size: 11px;
        """)
        row.addWidget(lbl)
        row.addWidget(self.country_input)
        form_layout.addLayout(row)
        outer.addWidget(form, 1)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ACA899;")
        outer.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 8)
        btn_row.addStretch()
        ok_btn = QPushButton("  Create List  ")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Exit")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def get_country(self):
        return self.country_input.text().strip()


# ─── Add Country Dialog ────────────────────────────────────────────────────────
class AddCountryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Country/Region")
        self.setFixedSize(320, 130)
        self.setStyleSheet(GLOBAL_STYLE)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel("Add Country / Region")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        outer.addWidget(title_bar)

        form = QWidget()
        form_layout = QHBoxLayout(form)
        form_layout.setContentsMargins(16, 14, 16, 8)
        lbl = QLabel("Country/Region:")
        lbl.setFixedWidth(100)
        lbl.setStyleSheet("font-weight: bold; font-size: 10px;")
        self.input = QLineEdit()
        self.input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #808080 #FFFFFF #FFFFFF #808080;
            padding: 1px 4px;
            font-size: 11px;
        """)
        form_layout.addWidget(lbl)
        form_layout.addWidget(self.input)
        outer.addWidget(form, 1)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ACA899;")
        outer.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 8)
        btn_row.addStretch()
        ok_btn = QPushButton("  Add  ")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def get_country(self):
        return self.input.text().strip()


# ─── CSV Column Mapper Dialog ──────────────────────────────────────────────────
class CSVMapperDialog(QDialog):
    """Shows a preview of the CSV and lets the user map columns to bird fields."""

    FIELDS = [
        ("name",       "Common Name"),
        ("scientific", "Scientific Name"),
        ("family",     "Family"),
        ("location",   "Location"),
        ("date",       "Date Sighted"),
        ("observer",   "Observer"),
        ("notes",      "Notes"),
    ]

    def __init__(self, csv_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CSV Column Mapping")
        self.setMinimumSize(620, 460)
        self.setStyleSheet(GLOBAL_STYLE)
        self.csv_path = csv_path
        self.headers = []
        self.preview_rows = []
        self._load_csv_preview()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Title bar
        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel("CSV Import — Map Columns to Bird Record Fields")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        outer.addWidget(title_bar)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(12, 10, 12, 8)
        body_layout.setSpacing(8)

        # Preview table
        preview_lbl = QLabel("CSV Preview (first 5 rows):")
        preview_lbl.setStyleSheet("font-weight: bold; font-size: 10px;")
        body_layout.addWidget(preview_lbl)

        self.preview_table = QTableWidget()
        self.preview_table.setMaximumHeight(140)
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        body_layout.addWidget(self.preview_table)
        self._populate_preview()

        # Mapping section
        map_lbl = QLabel("Map each bird record field to a CSV column:")
        map_lbl.setStyleSheet("font-weight: bold; font-size: 10px; margin-top: 4px;")
        body_layout.addWidget(map_lbl)

        hint = QLabel('Select "— Skip —" to leave a field blank for all imported records.')
        hint.setStyleSheet("font-size: 10px; color: #555555;")
        body_layout.addWidget(hint)

        # Grid of field → combo
        grid_frame = QFrame()
        grid_frame.setStyleSheet("""
            QFrame {
                background-color: #F4F2EC;
                border: 1px solid #ACA899;
            }
        """)
        grid = QFormLayout(grid_frame)
        grid.setContentsMargins(12, 8, 12, 8)
        grid.setSpacing(6)
        grid.setLabelAlignment(Qt.AlignRight)

        skip_option = "— Skip —"
        combo_options = [skip_option] + self.headers

        self.combos = {}
        for key, label in self.FIELDS:
            combo = QComboBox()
            combo.addItems(combo_options)
            # Auto-match header names case-insensitively
            for i, h in enumerate(self.headers):
                if h.lower().replace(" ", "") in (label.lower().replace(" ", ""),
                                                   key.lower()):
                    combo.setCurrentIndex(i + 1)
                    break
            lbl_w = QLabel(label + ":")
            lbl_w.setStyleSheet("font-size: 10px; font-weight: bold;")
            grid.addRow(lbl_w, combo)
            self.combos[key] = combo

        body_layout.addWidget(grid_frame)
        body_layout.addStretch()
        outer.addWidget(body, 1)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ACA899;")
        outer.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 8)
        btn_row.addStretch()
        ok_btn = QPushButton("  Import  ")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def _load_csv_preview(self):
        try:
            with open(self.csv_path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
            if rows:
                self.headers = [f"Col {i+1}: {h}" if h else f"Col {i+1}" 
                                for i, h in enumerate(rows[0])]
                self.raw_headers = rows[0]
                self.preview_rows = rows[1:6]
            else:
                self.headers = []
                self.raw_headers = []
                self.preview_rows = []
        except Exception:
            self.headers = []
            self.raw_headers = []
            self.preview_rows = []

    def _populate_preview(self):
        if not self.headers:
            return
        self.preview_table.setColumnCount(len(self.headers))
        self.preview_table.setHorizontalHeaderLabels(self.headers)
        self.preview_table.setRowCount(len(self.preview_rows))
        for r, row in enumerate(self.preview_rows):
            for c, val in enumerate(row):
                self.preview_table.setItem(r, c, QTableWidgetItem(val))

    def get_mapping(self):
        """Returns dict: field_key -> column_index (0-based), or -1 to skip."""
        skip_label = "— Skip —"
        mapping = {}
        for key, _ in self.FIELDS:
            text = self.combos[key].currentText()
            if text == skip_label:
                mapping[key] = -1
            else:
                # Find index in headers list
                idx = self.combos[key].currentIndex() - 1  # -1 because index 0 = skip
                mapping[key] = idx
        return mapping


# ─── Welcome Screen ────────────────────────────────────────────────────────────
class WelcomeScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        cfg = load_config()
        self.username = cfg.get("username", "Tom")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Title banner
        banner = QFrame()
        banner.setFixedHeight(80)
        banner.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1C3F7A, stop:0.6 #2B5FC2, stop:1 #1C3F7A);
            }
        """)
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(20, 0, 20, 0)

        banner_text = QLabel("Bird Life List")
        banner_text.setStyleSheet("""
            color: #FFFFFF;
            font-size: 22px;
            font-weight: bold;
            font-family: "Tahoma", sans-serif;
            background: transparent;
        """)
        banner_layout.addWidget(banner_text)
        banner_layout.addStretch()

        version = QLabel("Version 2.1.4")
        version.setStyleSheet("color: #A8C0E8; font-size: 10px; background: transparent;")
        banner_layout.addWidget(version, alignment=Qt.AlignBottom)
        outer.addWidget(banner)

        stripe = QFrame()
        stripe.setFixedHeight(4)
        stripe.setStyleSheet("background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #F0A000, stop:0.5 #FFD000, stop:1 #F0A000);")
        outer.addWidget(stripe)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(16)

        dialog_panel = QFrame()
        dialog_panel.setFixedSize(380, 240)
        dialog_panel.setStyleSheet("""
            QFrame {
                background-color: #ECE9D8;
                border: 2px solid;
                border-color: #FFFFFF #808080 #808080 #FFFFFF;
            }
        """)
        dp_layout = QVBoxLayout(dialog_panel)
        dp_layout.setContentsMargins(20, 20, 20, 20)
        dp_layout.setSpacing(12)

        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
                border: none;
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel("Bird Life List — Welcome")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        tb_layout.addStretch()
        for ch in ["_", "□", "✕"]:
            b = QPushButton(ch)
            b.setFixedSize(16, 16)
            b.setStyleSheet("""
                QPushButton {
                    background-color: #D0D0D0; color:black;
                    border: 1px solid #606060; font-size:9px;
                    padding:0; min-height:0;
                }
            """)
            tb_layout.addWidget(b)
        dp_layout.addWidget(title_bar)

        spacer = QLabel()
        spacer.setFixedHeight(8)
        dp_layout.addWidget(spacer)

        self.welcome_lbl = QLabel(f"Welcome, {self.username}!")
        self.welcome_lbl.setAlignment(Qt.AlignCenter)
        self.welcome_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #1C3F7A;")
        dp_layout.addWidget(self.welcome_lbl)

        sub_lbl = QLabel("Comprehensive bird record and list management system\nfor the serious birder.")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setStyleSheet("font-size: 10px; color: #444444;")
        dp_layout.addWidget(sub_lbl)

        dp_layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        enter_btn = QPushButton("  Enter  ")
        enter_btn.setObjectName("enterBtn")
        enter_btn.clicked.connect(switch_callback)
        btn_row.addWidget(enter_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(QApplication.quit)
        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        dp_layout.addLayout(btn_row)

        content_layout.addWidget(dialog_panel, alignment=Qt.AlignCenter)
        outer.addWidget(content, 1)

        bottom = QFrame()
        bottom.setFixedHeight(22)
        bottom.setStyleSheet("background-color: #D4D0C8; border-top: 1px solid #808080;")
        bl = QHBoxLayout(bottom)
        bl.setContentsMargins(6, 0, 6, 0)
        bl.addStretch()
        bl.addWidget(QLabel("© 2025 IRRATIONAL TECHNOLOGY Pty Ltd."))
        outer.addWidget(bottom)


# ─── Add Bird Dialog ───────────────────────────────────────────────────────────
class AddBirdDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Bird")
        self.setFixedSize(380, 340)
        self.setStyleSheet(GLOBAL_STYLE)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel("Add New Bird Record")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        outer.addWidget(title_bar)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(16, 12, 16, 12)
        form_layout.setSpacing(8)

        self.name_val     = self._add_field(form_layout, "Common Name:")
        self.sci_val      = self._add_field(form_layout, "Scientific:")
        self.family_val   = self._add_field(form_layout, "Family:")
        self.location_val = self._add_field(form_layout, "Location:")
        self.date_val     = self._add_field(form_layout, "Date Sighted:")
        self.observer_val = self._add_field(form_layout, "Observer:")
        self.notes_val    = self._add_field(form_layout, "Notes:")

        outer.addWidget(form_widget, 1)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ACA899;")
        outer.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 8)
        btn_row.addStretch()
        ok_btn = QPushButton("  OK  ")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def _add_field(self, layout, label_text):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setFixedWidth(90)
        lbl.setStyleSheet("font-weight: bold; font-size: 10px;")
        val = QLineEdit()
        val.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #808080 #FFFFFF #FFFFFF #808080;
            padding: 1px 4px;
            font-size: 10px;
        """)
        row.addWidget(lbl)
        row.addWidget(val)
        layout.addLayout(row)
        return val

    def get_data(self):
        return {
            "name":       self.name_val.text().strip(),
            "scientific": self.sci_val.text().strip(),
            "family":     self.family_val.text().strip(),
            "location":   self.location_val.text().strip(),
            "date":       self.date_val.text().strip(),
            "observer":   self.observer_val.text().strip(),
            "notes":      self.notes_val.text().strip(),
        }


# ─── Search Dialog ─────────────────────────────────────────────────────────────
class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search")
        self.setFixedSize(320, 120)
        self.setStyleSheet(GLOBAL_STYLE)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        title_bar = QFrame()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1C3F7A, stop:1 #6A8FD0);
            }
        """)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(6, 2, 4, 2)
        tb_title = QLabel("Search Bird Records")
        tb_title.setStyleSheet("color:white; font-size:11px; font-weight:bold; background:transparent;")
        tb_layout.addWidget(tb_title)
        outer.addWidget(title_bar)

        form = QWidget()
        form_layout = QHBoxLayout(form)
        form_layout.setContentsMargins(12, 12, 12, 8)
        form_layout.setSpacing(8)

        lbl = QLabel("Search:")
        lbl.setStyleSheet("font-weight: bold; font-size: 10px;")
        lbl.setFixedWidth(46)
        form_layout.addWidget(lbl)

        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #808080 #FFFFFF #FFFFFF #808080;
            padding: 1px 4px;
            font-size: 10px;
        """)
        self.search_input.setPlaceholderText("Enter bird name...")
        form_layout.addWidget(self.search_input)
        outer.addWidget(form)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ACA899;")
        outer.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 8)
        btn_row.addStretch()
        ok_btn = QPushButton("  Search  ")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def get_query(self):
        return self.search_input.text().strip().lower()


# ─── Main Bird List Screen ─────────────────────────────────────────────────────
class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.manager = BirdManager()
        cfg = load_config()
        self.username = cfg.get("username", "Tom")

        # Ensure birds.json exists; if not, prompt for first country
        self._ensure_birds_file()

        self.current_country = self._pick_initial_country()

        # ── Toolbar ──────────────────────────────────────────────────
        toolbar_frame = QFrame()
        toolbar_frame.setFixedHeight(36)
        toolbar_frame.setStyleSheet("""
            QFrame {
                background-color: #ECE9D8;
                border-bottom: 1px solid #ACA899;
            }
        """)
        tb_layout = QHBoxLayout(toolbar_frame)
        tb_layout.setContentsMargins(4, 3, 4, 3)
        tb_layout.setSpacing(4)

        self.country_combo = QComboBox()
        self.country_combo.setFixedWidth(140)
        self.country_combo.setToolTip("Switch country / life list")
        self._refresh_country_combo()
        self.country_combo.currentTextChanged.connect(self.on_country_changed)
        tb_layout.addWidget(self.country_combo)

        add_country_btn = QPushButton("+")
        add_country_btn.setFixedSize(22, 22)
        add_country_btn.setToolTip("Add new country / region list")
        add_country_btn.setStyleSheet("""
            QPushButton {
                font-size: 13px; font-weight: bold; padding: 0;
                background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #FFFFFF, stop:1 #D8D8D8);
                border: 1px solid #ACA899;
            }
            QPushButton:hover { background-color: #C8D8FF; border-color: #316AC5; }
        """)
        add_country_btn.clicked.connect(self.add_country)
        tb_layout.addWidget(add_country_btn)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFixedWidth(6)
        sep.setStyleSheet("color: #ACA899;")
        tb_layout.addWidget(sep)

        # Save / Search buttons
        for icon, tip in [("💾", "Save"), ("🔍", "Search")]:
            btn = QPushButton(icon)
            btn.setFixedSize(28, 26)
            btn.setToolTip(tip)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 13px; padding: 0;
                    background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                        stop:0 #FFFFFF, stop:1 #D8D8D8);
                    border: 1px solid #ACA899;
                }
                QPushButton:hover { background-color: #C8D8FF; border-color: #316AC5; }
                QPushButton:pressed { background-color: #A0B8E8; }
            """)
            if tip == "Save":
                btn.clicked.connect(self.save_current_bird)
            if tip == "Search":
                btn.clicked.connect(self.search_birds)
            tb_layout.addWidget(btn)

        tb_layout.addStretch()

        self.lifelist_lbl = QLabel("Life List: 0")
        self.lifelist_lbl.setStyleSheet("font-size: 10px; color: #000000;")
        tb_layout.addWidget(self.lifelist_lbl)

        # ── Profile button (top right) ───────────────────────────────
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setFixedWidth(6)
        sep2.setStyleSheet("color: #ACA899;")
        tb_layout.addWidget(sep2)
        
        self.profile_btn = QPushButton(f" {self.username}")
        self.profile_btn.setFixedHeight(26)
        self.profile_btn.setToolTip("Edit user profile / display name")
        self.profile_btn.setStyleSheet("""
            QPushButton {
                font-size: 10px; padding: 0 8px;
                background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #FFFFFF, stop:1 #D8D8D8);
                border: 1px solid #ACA899;
            }
            QPushButton:hover { background-color: #C8D8FF; border-color: #316AC5; }
        """)
        self.profile_btn.clicked.connect(self.open_profile)
        tb_layout.addWidget(self.profile_btn)

        layout.addWidget(toolbar_frame)

        # ── Main splitter ─────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(5)
        splitter.setStyleSheet("QSplitter::handle { background-color: #ACA899; }")

        # ── Left: Bird list ──────────────────────────────────────────
        left_panel = QFrame()
        left_panel.setMinimumWidth(220)
        lp_layout = QVBoxLayout(left_panel)
        lp_layout.setContentsMargins(6, 6, 3, 6)
        lp_layout.setSpacing(4)

        self.list_group = QGroupBox("Bird List")
        lg_layout = QVBoxLayout(self.list_group)
        lg_layout.setContentsMargins(4, 8, 4, 4)
        lg_layout.setSpacing(4)

        self.bird_list = QListWidget()
        self.bird_list.setAlternatingRowColors(True)
        self.bird_list.blockSignals(True)
        self.load_birds()
        self.bird_list.setCurrentRow(0)
        self.bird_list.blockSignals(False)
        lg_layout.addWidget(self.bird_list)
        lp_layout.addWidget(self.list_group)

        clear_btn = QPushButton("✕ Clear Search")
        clear_btn.setFixedHeight(20)
        clear_btn.setStyleSheet("""
            QPushButton {
                font-size: 10px; padding: 0 6px;
                background-color: #D4D0C8;
                border: 1px solid #ACA899;
            }
        """)
        clear_btn.clicked.connect(self.clear_search)
        lp_layout.addWidget(clear_btn)

        summary_frame = QFrame()
        summary_frame.setStyleSheet("QFrame { background-color: #D4D0C8; border: 1px inset #808080; }")
        sf_layout = QVBoxLayout(summary_frame)
        sf_layout.setContentsMargins(6, 4, 6, 4)
        sf_layout.setSpacing(2)
        self.selected_lbl = self._small_label("Selected: None")
        sf_layout.addWidget(self.selected_lbl)
        lp_layout.addWidget(summary_frame)

        splitter.addWidget(left_panel)

        # ── Right: Details + Actions ─────────────────────────────────
        right_panel = QFrame()
        rp_layout = QVBoxLayout(right_panel)
        rp_layout.setContentsMargins(3, 6, 6, 6)
        rp_layout.setSpacing(8)

        details_group = QGroupBox("Record Details")
        dg_layout = QVBoxLayout(details_group)
        dg_layout.setContentsMargins(8, 8, 8, 8)
        dg_layout.setSpacing(6)

        self.common_val = self._create_detail_row(dg_layout, "Common Name:")
        self.sci_val    = self._create_detail_row(dg_layout, "Scientific:")
        self.date_val   = self._create_detail_row(dg_layout, "Date Sighted:")
        self.loc_val    = self._create_detail_row(dg_layout, "Location:")
        self.notes_val  = self._create_detail_row(dg_layout, "Notes:")

        # Photo section
        photo_divider = QFrame()
        photo_divider.setFrameShape(QFrame.HLine)
        photo_divider.setStyleSheet("color: #ACA899;")
        dg_layout.addWidget(photo_divider)

        photo_row = QHBoxLayout()
        self.photo_toggle_btn = QPushButton("▶  Photo")
        self.photo_toggle_btn.setFixedHeight(20)
        self.photo_toggle_btn.setStyleSheet("""
            QPushButton {
                text-align: left; padding-left: 4px;
                font-size: 10px; font-weight: bold;
                background: transparent; border: none; color: #1C3F7A;
            }
            QPushButton:hover { color: #316AC5; }
        """)
        self.photo_toggle_btn.clicked.connect(self.toggle_photo_panel)
        photo_row.addWidget(self.photo_toggle_btn)
        photo_row.addStretch()
        dg_layout.addLayout(photo_row)

        self.photo_panel = QFrame()
        self.photo_panel.setVisible(False)
        self.photo_panel.setStyleSheet("""
            QFrame {
                background-color: #D4D0C8;
                border: 2px solid;
                border-color: #808080 #FFFFFF #FFFFFF #808080;
            }
        """)
        pp_layout = QVBoxLayout(self.photo_panel)
        pp_layout.setContentsMargins(6, 6, 6, 6)
        pp_layout.setSpacing(4)

        self.photo_label = QLabel()
        self.photo_label.setFixedHeight(160)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("""
            QLabel {
                background-color: #000000;
                border: 2px solid;
                border-color: #808080 #FFFFFF #FFFFFF #808080;
                color: #888888; font-size: 10px;
            }
        """)
        self.photo_label.setText("No photo on record.")
        pp_layout.addWidget(self.photo_label)
        dg_layout.addWidget(self.photo_panel)

        # Map section
        map_divider = QFrame()
        map_divider.setFrameShape(QFrame.HLine)
        map_divider.setStyleSheet("color: #ACA899;")
        dg_layout.addWidget(map_divider)

        map_row = QHBoxLayout()
        self.map_toggle_btn = QPushButton("▶  Map")
        self.map_toggle_btn.setFixedHeight(20)
        self.map_toggle_btn.setStyleSheet("""
            QPushButton {
                text-align: left; padding-left: 4px;
                font-size: 10px; font-weight: bold;
                background: transparent; border: none; color: #1C3F7A;
            }
            QPushButton:hover { color: #316AC5; }
        """)
        self.map_toggle_btn.clicked.connect(self.toggle_map_panel)
        map_row.addWidget(self.map_toggle_btn)
        map_row.addStretch()
        dg_layout.addLayout(map_row)

        self.map_panel = QFrame()
        self.map_panel.setVisible(False)
        self.map_panel.setStyleSheet("""
            QFrame {
                background-color: #D4D0C8;
                border: 2px solid;
                border-color: #808080 #FFFFFF #FFFFFF #808080;
            }
        """)
        mp_layout = QVBoxLayout(self.map_panel)
        mp_layout.setContentsMargins(6, 6, 6, 6)
        mp_layout.setSpacing(4)

        self.map_view = QWebEngineView()
        self.map_view.setFixedHeight(200)
        mp_layout.addWidget(self.map_view)
        dg_layout.addWidget(self.map_panel)

        self.bird_list.currentItemChanged.connect(self.update_details)

        # Actions group
        actions_group = QGroupBox("Actions")
        ag_layout = QVBoxLayout(actions_group)
        ag_layout.setContentsMargins(8, 8, 8, 8)
        ag_layout.setSpacing(6)

        action_buttons = [
            (" Add New Bird",    True),
            (" Delete Record",   True),
            ("SEP", False),
            (" Add Photo",       True),
            (" View on Map",     True),
            ("SEP", False),
            (" Export to CSV",   True),
            (" Import from CSV", True),
        ]

        for label, enabled in action_buttons:
            if label == "SEP":
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setStyleSheet("color: #ACA899;")
                ag_layout.addWidget(sep)
            else:
                btn = QPushButton(label)
                if label == " Add New Bird":
                    btn.clicked.connect(self.add_new_bird)
                elif label == " Delete Record":
                    btn.clicked.connect(self.delete_current_bird)
                elif label == " Add Photo":
                    btn.clicked.connect(self.add_photo)
                elif label == " Export to CSV":
                    btn.clicked.connect(self.export_csv)
                elif label == " Import from CSV":
                    btn.clicked.connect(self.import_csv)
                elif label == " View on Map":
                    btn.clicked.connect(self.toggle_map_panel)
                btn.setEnabled(enabled)
                btn.setFixedHeight(24)
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding-left: 8px;
                        font-size: 11px;
                    }
                """)
                ag_layout.addWidget(btn)

        rp_layout.addWidget(details_group)
        rp_layout.addWidget(actions_group)
        rp_layout.addStretch()

        splitter.addWidget(right_panel)
        splitter.setSizes([280, 420])
        layout.addWidget(splitter, 1)

        # ── Status bar ───────────────────────────────────────────────
        status_frame = QFrame()
        status_frame.setFixedHeight(22)
        status_frame.setStyleSheet("background-color: #D4D0C8; border-top: 1px solid #808080;")
        sl = QHBoxLayout(status_frame)
        sl.setContentsMargins(0, 0, 0, 0)
        sl.setSpacing(0)

        self.status_cells = {}
        for key, text, w in [("status", "Ready", 140), ("db", "Database: birds.json", 180), ("user", f"User: {self.username}", 120)]:
            cell = QFrame()
            cell.setFixedWidth(w)
            cell.setStyleSheet("border-right: 1px solid #808080; border-left: 1px solid #FFFFFF;")
            cl = QHBoxLayout(cell)
            cl.setContentsMargins(4, 0, 4, 0)
            lbl = self._small_label(text)
            cl.addWidget(lbl)
            sl.addWidget(cell)
            self.status_cells[key] = lbl

        sl.addStretch()
        sl.addWidget(self._small_label("  Bird Life List v2.1.4  "))
        layout.addWidget(status_frame)

    # ── Helpers ──────────────────────────────────────────────────────

    def _ensure_birds_file(self):
        """Create an empty birds.json if none exists."""
        if not os.path.exists(BIRDS_FILE):
            with open(BIRDS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

    def _pick_initial_country(self):
        """Return the first country in birds.json, or prompt to create one."""
        countries = self.manager.get_countries()
        if countries:
            return countries[0]
        # No countries yet — prompt
        dlg = NewCountryDialog([], self)
        if dlg.exec() == QDialog.Accepted:
            country = dlg.get_country()
            if country:
                self.manager.save_birds(country, [])
                return country
        # User cancelled — create a default
        self.manager.save_birds("My List", [])
        return "My List"

    def _refresh_country_combo(self):
        self.country_combo.blockSignals(True)
        self.country_combo.clear()
        countries = self.manager.get_countries()
        for c in countries:
            self.country_combo.addItem(c)
        if hasattr(self, "current_country") and self.current_country in countries:
            self.country_combo.setCurrentText(self.current_country)
        self.country_combo.blockSignals(False)

    def _small_label(self, text, bold=False):
        lbl = QLabel(text)
        style = "font-size: 10px;"
        if bold:
            style += " font-weight: bold;"
        lbl.setStyleSheet(style)
        return lbl

    def _create_detail_row(self, layout, label_text):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setFixedWidth(90)
        lbl.setStyleSheet("font-weight: bold; font-size: 10px;")
        val = QLineEdit("")
        val.setStyleSheet("background-color: #FFFFFF; border: 1px solid; border-color: #808080 #FFFFFF #FFFFFF #808080; padding: 1px 4px; font-size: 10px;")
        val.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row.addWidget(lbl)
        row.addWidget(val)
        layout.addLayout(row)
        return val

    # ── Country switching ─────────────────────────────────────────────

    def on_country_changed(self, country):
        if country and country != self.current_country:
            self.current_country = country
            self.bird_list.blockSignals(True)
            self.load_birds()
            self.bird_list.setCurrentRow(0)
            self.bird_list.blockSignals(False)
            # Trigger detail update for first item
            if self.bird_list.count() > 0:
                self.update_details(self.bird_list.item(0), None)

    def add_country(self):
        dlg = AddCountryDialog(self)
        if dlg.exec() == QDialog.Accepted:
            country = dlg.get_country()
            if not country:
                return
            existing = self.manager.get_countries()
            if country in existing:
                QMessageBox.information(self, "Already Exists",
                    f"A list for '{country}' already exists.")
                return
            self.manager.save_birds(country, [])
            self._refresh_country_combo()
            self.country_combo.setCurrentText(country)

    # ── Profile ───────────────────────────────────────────────────────

    def open_profile(self):
        dlg = ProfileDialog(self.username, self)
        if dlg.exec() == QDialog.Accepted:
            new_name = dlg.get_name()
            self.username = new_name
            cfg = load_config()
            cfg["username"] = new_name
            save_config(cfg)
            # Update UI
            self.profile_btn.setText(f" {new_name}")
            self.status_cells["user"].setText(f"User: {new_name}")

    # ── Bird list ─────────────────────────────────────────────────────

    def clear_search(self):
        for i in range(self.bird_list.count()):
            self.bird_list.item(i).setHidden(False)

    def load_birds(self):
        self.bird_list.clear()
        birds = self.manager.get_birds(self.current_country)
        for bird in birds:
            item = QListWidgetItem(bird["name"])
            item.setData(Qt.UserRole, bird)
            item.setToolTip(bird.get("scientific", ""))
            self.bird_list.addItem(item)
        self.lifelist_lbl.setText(f"Life List: {len(birds)}")
        self.list_group.setTitle(f"Bird Life List — {self.current_country}: {len(birds)}")

    def update_details(self, current, previous):
        if not current:
            return
        bird = current.data(Qt.UserRole)
        self.common_val.setText(bird.get("name", ""))
        self.sci_val.setText(bird.get("scientific", ""))
        self.date_val.setText(bird.get("date", ""))
        self.loc_val.setText(bird.get("location", ""))
        self.notes_val.setText(bird.get("notes", ""))
        self.selected_lbl.setText(f"Selected: {bird.get('name', 'Unknown')}")

        photo_path = bird.get("photo", "")
        self._load_photo(photo_path)
        if photo_path:
            self.photo_panel.setVisible(True)
            self.photo_toggle_btn.setText("▼  Photo")
        else:
            self.photo_panel.setVisible(False)
            self.photo_toggle_btn.setText("▶  Photo")
            self.map_panel.setVisible(False)
            self.map_toggle_btn.setText("▶  Map")

    def save_current_bird(self):
        current = self.bird_list.currentItem()
        if not current:
            return
        bird = current.data(Qt.UserRole)
        bird["name"]       = self.common_val.text()
        bird["scientific"] = self.sci_val.text()
        bird["date"]       = self.date_val.text()
        bird["location"]   = self.loc_val.text()
        bird["notes"]      = self.notes_val.text()
        current.setData(Qt.UserRole, bird)
        current.setText(bird["name"])

        all_birds = [self.bird_list.item(i).data(Qt.UserRole) for i in range(self.bird_list.count())]
        self.manager.save_birds(self.current_country, all_birds)
        self.selected_lbl.setText(f"Selected: {bird['name']}")

    def add_new_bird(self):
        dialog = AddBirdDialog(self)
        if dialog.exec() == QDialog.Accepted:
            bird = dialog.get_data()
            if not bird["name"]:
                return
            # Default observer to current username if blank
            if not bird["observer"]:
                bird["observer"] = self.username
            all_birds = [self.bird_list.item(i).data(Qt.UserRole) for i in range(self.bird_list.count())]
            all_birds.append(bird)
            self.manager.save_birds(self.current_country, all_birds)
            self.load_birds()
            self.bird_list.setCurrentRow(self.bird_list.count() - 1)

    def delete_current_bird(self):
        current = self.bird_list.currentItem()
        if not current:
            return
        bird = current.data(Qt.UserRole)
        name = bird.get("name", "this record")
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Confirm Delete")
        confirm.setText(f"Are you sure you want to delete '{name}'?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        confirm.setStyleSheet(GLOBAL_STYLE)
        if confirm.exec() != QMessageBox.Yes:
            return
        all_birds = [self.bird_list.item(i).data(Qt.UserRole)
                     for i in range(self.bird_list.count())
                     if self.bird_list.item(i) != current]
        self.manager.save_birds(self.current_country, all_birds)
        self.load_birds()
        self.bird_list.setCurrentRow(0)

    # ── Photo ─────────────────────────────────────────────────────────

    def toggle_photo_panel(self):
        visible = self.photo_panel.isVisible()
        self.photo_panel.setVisible(not visible)
        self.photo_toggle_btn.setText("▼  Photo" if not visible else "▶  Photo")

    def add_photo(self):
        current = self.bird_list.currentItem()
        if not current:
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if not path:
            return
        bird = current.data(Qt.UserRole)
        bird["photo"] = path
        current.setData(Qt.UserRole, bird)
        all_birds = [self.bird_list.item(i).data(Qt.UserRole) for i in range(self.bird_list.count())]
        self.manager.save_birds(self.current_country, all_birds)
        self._load_photo(path)
        self.photo_panel.setVisible(True)
        self.photo_toggle_btn.setText("▼  Photo")

    def _load_photo(self, path):
        if path and os.path.exists(path):
            pixmap = QPixmap(path)
            scaled = pixmap.scaled(
                self.photo_label.width(), self.photo_label.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(scaled)
            self.photo_label.setText("")
        else:
            self.photo_label.setPixmap(QPixmap())
            self.photo_label.setText("No photo on record.")

    # ── CSV export / import ───────────────────────────────────────────

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "birds.csv", "CSV Files (*.csv)")
        if not path:
            return
        fields = ["name", "scientific", "family", "date", "location", "observer", "notes"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for i in range(self.bird_list.count()):
                writer.writerow(self.bird_list.item(i).data(Qt.UserRole))
        QMessageBox.information(self, "Export Complete",
            f"Successfully exported {self.bird_list.count()} records to:\n{path}")

    def import_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import from CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        # Open the column mapper dialog first
        mapper = CSVMapperDialog(path, self)
        if mapper.exec() != QDialog.Accepted:
            return

        mapping = mapper.get_mapping()

        # Read the full CSV and apply the mapping
        existing_names = set()
        for i in range(self.bird_list.count()):
            existing_names.add(self.bird_list.item(i).data(Qt.UserRole).get("name", "").lower())

        all_birds = [self.bird_list.item(i).data(Qt.UserRole) for i in range(self.bird_list.count())]
        imported = 0
        skipped  = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header row
            for row in reader:
                bird = {
                    "name": "", "scientific": "", "family": "",
                    "date": "", "location": "", "observer": "", "notes": "",
                }
                for key, col_idx in mapping.items():
                    if col_idx >= 0 and col_idx < len(row):
                        bird[key] = row[col_idx].strip()

                if not bird["name"]:
                    skipped += 1
                    continue
                if bird["name"].lower() in existing_names:
                    skipped += 1
                    continue
                if not bird["observer"]:
                    bird["observer"] = self.username
                all_birds.append(bird)
                existing_names.add(bird["name"].lower())
                imported += 1

        self.manager.save_birds(self.current_country, all_birds)
        self.load_birds()
        QMessageBox.information(self, "Import Complete",
            f"Imported: {imported} records\nSkipped (duplicate or invalid): {skipped}")

    # ── Search ────────────────────────────────────────────────────────

    def search_birds(self):
        dialog = SearchDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return
        query = dialog.get_query()
        if not query:
            for i in range(self.bird_list.count()):
                self.bird_list.item(i).setHidden(False)
            return
        first_match = None
        for i in range(self.bird_list.count()):
            item = self.bird_list.item(i)
            bird = item.data(Qt.UserRole)
            match = (
                query in bird.get("name", "").lower() or
                query in bird.get("scientific", "").lower() or
                query in bird.get("location", "").lower() or
                query in bird.get("family", "").lower()
            )
            item.setHidden(not match)
            if match and first_match is None:
                first_match = item
        if first_match:
            self.bird_list.setCurrentItem(first_match)
        else:
            QMessageBox.information(self, "No Results",
                f"No birds found matching '{query}'.")

    # ── Map ───────────────────────────────────────────────────────────

    def toggle_map_panel(self):
        visible = self.map_panel.isVisible()
        if not visible:
            current = self.bird_list.currentItem()
            if current:
                bird = current.data(Qt.UserRole)
                self._load_map(bird.get("location", ""), bird)
        self.map_panel.setVisible(not visible)
        self.map_toggle_btn.setText("▼  Map" if not visible else "▶  Map")

    def _load_map(self, location, bird):
        lat = bird.get("lat")
        lng = bird.get("lng")
        if not lat or not lng:
            if not location:
                self._render_map(0, 0, "Unknown Location", zoom=2)
                return
            try:
                from geopy.geocoders import Nominatim
                geolocator = Nominatim(user_agent="toms_bird_list")
                result = geolocator.geocode(location, timeout=5)
                if result:
                    lat = result.latitude
                    lng = result.longitude
                    current = self.bird_list.currentItem()
                    if current:
                        bird["lat"] = lat
                        bird["lng"] = lng
                        current.setData(Qt.UserRole, bird)
                else:
                    self._render_map(0, 0, location, zoom=2)
                    return
            except Exception:
                self._render_map(0, 0, location, zoom=2)
                return
        self._render_map(lat, lng, location)

    def _render_map(self, lat, lng, label, zoom=13):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>body {{ margin:0; padding:0; }} #map {{ width:100%; height:200px; }}</style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([{lat}, {lng}], {zoom});
                L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors © CARTO',
                    subdomains: 'abcd', maxZoom: 19
                }}).addTo(map);
                {"L.marker([" + str(lat) + ", " + str(lng) + "]).addTo(map).bindPopup('" + label.replace("'", "\\'") + "').openPopup();" if zoom != 2 else ""}
            </script>
        </body>
        </html>
        """
        self.map_view.setHtml(html)


# ─── Main Window ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bird Life List — Record & List Management System")
        self.resize(760, 540)

        menu_bar = self.menuBar()
        for menu_name, items in [
            ("&File",    ["&New Record\tCtrl+N", "&Open Database...", "&Save\tCtrl+S", "---", "&Print...\tCtrl+P", "---", "E&xit"]),
            ("&Edit",    ["&Add Bird", "&Edit Record\tF2", "&Delete Record\tDel", "---", "&Find...\tCtrl+F"]),
            ("&View",    ["&Refresh\tF5", "---", "&Sort by Name", "Sort by &Date", "---", "&Column Settings..."]),
            ("&Reports", ["&Species Summary", "&Sighting Log", "---", "&Export to CSV...", "&Export to PDF..."]),
            ("&Tools",   ["&Preferences...", "---", "&Database Backup...", "&Import Records..."]),
            ("&Help",    ["&Help Topics\tF1", "---", "&About Bird Life List..."]),
        ]:
            menu = menu_bar.addMenu(menu_name)
            for item in items:
                if item == "---":
                    menu.addSeparator()
                else:
                    menu.addAction(QAction(item.replace("\t", "    "), self))

        self.stack = QStackedWidget()
        self.welcome = WelcomeScreen(self.go_to_main)
        self.main = None
        self.stack.addWidget(self.welcome)
        self.setCentralWidget(self.stack)
        self.setStyleSheet(GLOBAL_STYLE)

    def go_to_main(self):
        if self.main is None:
            self.main = MainScreen()
            self.stack.addWidget(self.main)
        self.stack.setCurrentWidget(self.main)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())