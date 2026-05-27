"""Graphical user interface for the calculator using PyQt6.

This module provides a GUI that uses the existing core and history modules,
demonstrating the separation of concerns in the calculator architecture.
"""

import math
import sys
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QPoint
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from calculator import core
from calculator.history import CalculationHistory


class CalculatorButton(QPushButton):
    """A styled calculator button."""

    def __init__(self, text: str, color: str = "#4a4a4a"):
        super().__init__(text)
        self.setMinimumSize(60, 60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFont(QFont("Segoe UI", 16))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {self._lighten(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken(color)};
            }}
        """)

    def _lighten(self, color: str) -> str:
        """Lighten a hex color."""
        if color == "#4a4a4a":
            return "#5a5a5a"
        elif color == "#ff9500":
            return "#ffaa33"
        elif color == "#d4d4d2":
            return "#e4e4e2"
        elif color == "#ff3b30":
            return "#ff5a50"
        elif color == "#5856d6":
            return "#6866e6"
        elif color == "#3a3a3a":
            return "#4a4a4a"
        return color

    def _darken(self, color: str) -> str:
        """Darken a hex color."""
        if color == "#4a4a4a":
            return "#3a3a3a"
        elif color == "#ff9500":
            return "#dd8000"
        elif color == "#d4d4d2":
            return "#c4c4c2"
        elif color == "#ff3b30":
            return "#dd2a20"
        elif color == "#5856d6":
            return "#4846c6"
        elif color == "#3a3a3a":
            return "#2a2a2a"
        return color


class StandardModeWidget(QWidget):
    """Widget containing the standard calculator mode UI."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        """Set up the standard mode user interface."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(10)

        self.parent.display = QLineEdit()
        self.parent.display.setReadOnly(True)
        self.parent.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.parent.display.setFont(QFont("Segoe UI", 32))
        self.parent.display.setMinimumHeight(80)
        self.parent.display.setText("0")
        self.parent.display.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        calc_layout.addWidget(self.parent.display)

        self.parent.expression_label = QLabel("")
        self.parent.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.parent.expression_label.setFont(QFont("Segoe UI", 12))
        self.parent.expression_label.setStyleSheet("color: #888; padding-right: 10px;")
        calc_layout.addWidget(self.parent.expression_label)

        button_layout = QGridLayout()
        button_layout.setSpacing(8)

        buttons = [
            ("C", 0, 0, "#ff3b30"), ("√", 0, 1, "#ff9500"), ("%", 0, 2, "#ff9500"), ("/", 0, 3, "#ff9500"),
            ("7", 1, 0, "#4a4a4a"), ("8", 1, 1, "#4a4a4a"), ("9", 1, 2, "#4a4a4a"), ("*", 1, 3, "#ff9500"),
            ("4", 2, 0, "#4a4a4a"), ("5", 2, 1, "#4a4a4a"), ("6", 2, 2, "#4a4a4a"), ("-", 2, 3, "#ff9500"),
            ("1", 3, 0, "#4a4a4a"), ("2", 3, 1, "#4a4a4a"), ("3", 3, 2, "#4a4a4a"), ("+", 3, 3, "#ff9500"),
            ("0", 4, 0, "#4a4a4a"), (".", 4, 1, "#4a4a4a"), ("^", 4, 2, "#ff9500"), ("=", 4, 3, "#ff9500"),
        ]

        for text, row, col, color in buttons:
            btn = CalculatorButton(text, color)
            btn.clicked.connect(lambda checked, t=text: self.parent._on_button_click(t))
            button_layout.addWidget(btn, row, col)

        trig_grid = QGridLayout()
        trig_grid.setSpacing(8)

        self.parent.sin_btn = CalculatorButton("sin", "#5856d6")
        self.parent.sin_btn.clicked.connect(lambda: self.parent._calculate_trig("sin"))
        trig_grid.addWidget(self.parent.sin_btn, 0, 0)

        self.parent.cos_btn = CalculatorButton("cos", "#5856d6")
        self.parent.cos_btn.clicked.connect(lambda: self.parent._calculate_trig("cos"))
        trig_grid.addWidget(self.parent.cos_btn, 1, 0)

        self.parent.tan_btn = CalculatorButton("tan", "#5856d6")
        self.parent.tan_btn.clicked.connect(lambda: self.parent._calculate_trig("tan"))
        trig_grid.addWidget(self.parent.tan_btn, 2, 0)

        self.parent.inv_btn = CalculatorButton("inv", "#5856d6")
        self.parent.inv_btn.clicked.connect(self.parent._toggle_inverse)
        trig_grid.addWidget(self.parent.inv_btn, 3, 0)

        self.parent.rad_btn = CalculatorButton("rad", "#5856d6")
        self.parent.rad_btn.clicked.connect(self.parent._toggle_degrees)
        trig_grid.addWidget(self.parent.rad_btn, 4, 0)

        button_layout.addLayout(trig_grid, 0, 4, 5, 1)

        calc_layout.addLayout(button_layout)
        main_layout.addLayout(calc_layout, stretch=2)

        history_layout = QVBoxLayout()
        history_label = QLabel("History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_label.setStyleSheet("color: white;")
        history_layout.addWidget(history_label)

        self.parent.history_list = QListWidget()
        self.parent.history_list.setFont(QFont("Segoe UI", 11))
        self.parent.history_list.setStyleSheet("""
            QListWidget {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #4a4a4a;
            }
        """)
        self.parent.history_list.itemDoubleClicked.connect(self.parent._on_history_item_clicked)
        history_layout.addWidget(self.parent.history_list)

        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.setFont(QFont("Segoe UI", 10))
        clear_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        clear_history_btn.clicked.connect(self.parent._clear_history)
        history_layout.addWidget(clear_history_btn)

        main_layout.addLayout(history_layout, stretch=1)


class ProgrammerModeWidget(QWidget):
    """Widget containing the programmer calculator mode UI."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        """Set up the programmer mode user interface."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Left side: Display panel
        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(10)

        programmer_display = QLineEdit()
        programmer_display.setReadOnly(True)
        programmer_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        programmer_display.setFont(QFont("Segoe UI", 32))
        programmer_display.setMinimumHeight(80)
        programmer_display.setText("0")
        programmer_display.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        calc_layout.addWidget(programmer_display)

        # Placeholder for future bitwise operations buttons
        calc_layout.addStretch()

        main_layout.addLayout(calc_layout, stretch=2)

        # Right side: History panel
        history_layout = QVBoxLayout()
        history_label = QLabel("History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_label.setStyleSheet("color: white;")
        history_layout.addWidget(history_label)

        programmer_history_list = QListWidget()
        programmer_history_list.setFont(QFont("Segoe UI", 11))
        programmer_history_list.setStyleSheet("""
            QListWidget {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #4a4a4a;
            }
        """)
        history_layout.addWidget(programmer_history_list)

        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.setFont(QFont("Segoe UI", 10))
        clear_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        clear_history_btn.clicked.connect(self.parent._clear_history)
        history_layout.addWidget(clear_history_btn)

        main_layout.addLayout(history_layout, stretch=1)


class ModeToolbar(QWidget):
    """Toolbar with hamburger menu for mode switching."""

    hamburger_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_open = False
        self._setup_ui()

    def _setup_ui(self):
        """Set up the toolbar UI."""
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1c1c;
                border-bottom: 1px solid #3a3a3a;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.hamburger_btn = QPushButton("☰")
        self.hamburger_btn.setFixedSize(50, 50)
        self.hamburger_btn.setFont(QFont("Segoe UI", 24))
        self.hamburger_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        self.hamburger_btn.clicked.connect(self.hamburger_clicked.emit)
        layout.addWidget(self.hamburger_btn)

        layout.addStretch()

    def set_open_state(self, is_open: bool):
        """Update hamburger button appearance based on open state."""
        self.is_open = is_open
        self.hamburger_btn.setText("×" if is_open else "☰")


class SidebarOverlay(QWidget):
    """Semi-transparent overlay that appears when sidebar is open."""

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.3);")
        self.hide()

    def mousePressEvent(self, event):
        """Emit clicked signal when overlay is clicked."""
        self.clicked.emit()
        super().mousePressEvent(event)


class ModeSidebar(QWidget):
    """Sidebar for selecting calculator mode."""

    mode_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = "standard"
        self._setup_ui()

    def _setup_ui(self):
        """Set up the sidebar UI."""
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1c1c;
                border-right: 1px solid #3a3a3a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Calculator Mode")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("""
            QLabel {
                color: white;
                padding: 20px 15px 10px 15px;
                border: none;
            }
        """)
        layout.addWidget(title)

        self.standard_btn = QPushButton("Standard")
        self.standard_btn.setFont(QFont("Segoe UI", 14))
        self.standard_btn.clicked.connect(lambda: self.mode_selected.emit("standard"))
        layout.addWidget(self.standard_btn)

        self.programmer_btn = QPushButton("Programmer")
        self.programmer_btn.setFont(QFont("Segoe UI", 14))
        self.programmer_btn.clicked.connect(lambda: self.mode_selected.emit("programmer"))
        layout.addWidget(self.programmer_btn)

        layout.addStretch()

        self.set_active_mode("standard")
        self.hide()

    def set_active_mode(self, mode: str):
        """Update button styling to highlight the active mode."""
        self.current_mode = mode

        normal_style = """
            QPushButton {
                background-color: transparent;
                color: #ccc;
                padding: 15px 20px;
                text-align: left;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """

        active_style = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                padding: 15px 20px;
                text-align: left;
                border: none;
                border-left: 3px solid #ff9500;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """

        self.standard_btn.setStyleSheet(active_style if mode == "standard" else normal_style)
        self.programmer_btn.setStyleSheet(active_style if mode == "programmer" else normal_style)


class CalculatorWindow(QMainWindow):
    """Main calculator window."""

    def __init__(self):
        super().__init__()
        self.history = CalculationHistory()
        self.current_input = ""
        self.last_result: Optional[float] = None
        self.inverse_mode = False
        self.degrees_mode = False
        self.current_mode = "standard"
        self.sidebar_visible = False
        self._setup_ui()
        self._setup_shortcuts()

    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Calculator")
        self.setMinimumSize(400, 500)
        self.setStyleSheet("background-color: #2d2d2d;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add toolbar
        self.toolbar = ModeToolbar()
        self.toolbar.hamburger_clicked.connect(self._toggle_sidebar)
        main_layout.addWidget(self.toolbar)

        # Add mode container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)

        self.mode_stack = QStackedWidget()
        self.standard_widget = StandardModeWidget(self)
        self.programmer_widget = ProgrammerModeWidget(self)
        self.mode_stack.addWidget(self.standard_widget)
        self.mode_stack.addWidget(self.programmer_widget)
        container_layout.addWidget(self.mode_stack)

        main_layout.addWidget(container)

        # Add overlay (initially hidden, positioned absolutely)
        self.overlay = SidebarOverlay(central_widget)
        self.overlay.clicked.connect(self._toggle_sidebar)
        self.overlay.setGeometry(0, 50, self.width(), self.height() - 50)

        # Add sidebar (initially hidden, positioned absolutely)
        self.sidebar = ModeSidebar(central_widget)
        self.sidebar.mode_selected.connect(self._on_mode_selected)
        self.sidebar.setGeometry(-200, 50, 200, self.height() - 50)

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        QShortcut(QKeySequence("Return"), self, self._calculate)
        QShortcut(QKeySequence("Enter"), self, self._calculate)
        QShortcut(QKeySequence("Escape"), self, self._clear)

    def _on_button_click(self, text: str):
        """Handle button clicks."""
        if text == "C":
            self._clear()
        elif text == "=":
            self._calculate()
        elif text == "√":
            self._calculate_sqrt()
        else:
            self._append_to_input(text)

    def _append_to_input(self, text: str):
        """Append text to the current input."""
        if self.current_input == "0" and text.isdigit():
            self.current_input = text
        else:
            self.current_input += text
        self._update_display()

    def _update_display(self):
        """Update the display with current input."""
        display_text = self.current_input if self.current_input else "0"
        self.display.setText(display_text)

    def _clear(self):
        """Clear the current input."""
        self.current_input = ""
        self.expression_label.setText("")
        self._update_display()

    def _calculate(self):
        """Evaluate the current expression."""
        if not self.current_input:
            return

        expr = self.current_input
        try:
            result = self._evaluate_expression(expr)
            self.expression_label.setText(f"{expr} =")
            self.display.setText(self._format_result(result))
            self.history.add(expr, result)
            self._update_history_list()
            self.current_input = str(result)
            self.last_result = result
        except ValueError as e:
            self.display.setText("Error")
            self.expression_label.setText(str(e))
            self.current_input = ""

    def _calculate_sqrt(self):
        """Calculate square root of current input."""
        if not self.current_input:
            return

        try:
            n = float(self.current_input)
            result = core.square_root(n)
            expr = f"√({self.current_input})"
            self.expression_label.setText(f"{expr} =")
            self.display.setText(self._format_result(result))
            self.history.add(expr, result)
            self._update_history_list()
            self.current_input = str(result)
            self.last_result = result
        except ValueError as e:
            self.display.setText("Error")
            self.expression_label.setText(str(e))
            self.current_input = ""

    def _calculate_trig(self, func: str):
        """Calculate trigonometric function of current input."""
        if not self.current_input:
            return

        try:
            n = float(self.current_input)
            if self.inverse_mode:
                func_name = f"a{func}"
                trig_funcs = {"asin": core.asin, "acos": core.acos, "atan": core.atan}
                result = trig_funcs[func_name](n)
                if self.degrees_mode:
                    result = math.degrees(result)
            else:
                func_name = func
                trig_funcs = {"sin": core.sin, "cos": core.cos, "tan": core.tan}
                if self.degrees_mode:
                    n = math.radians(n)
                result = trig_funcs[func_name](n)

            unit = "°" if self.degrees_mode else ""
            expr = f"{func_name}({self.current_input}{unit})"
            self.expression_label.setText(f"{expr} =")
            self.display.setText(self._format_result(result))
            self.history.add(expr, result)
            self._update_history_list()
            self.current_input = str(result)
            self.last_result = result
        except ValueError as e:
            self.display.setText("Error")
            self.expression_label.setText(str(e))
            self.current_input = ""

    def _toggle_inverse(self):
        """Toggle inverse mode for trig functions."""
        self.inverse_mode = not self.inverse_mode
        if self.inverse_mode:
            self.sin_btn.setText("asin")
            self.cos_btn.setText("acos")
            self.tan_btn.setText("atan")
            self.inv_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7876f6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #8886ff;
                }
                QPushButton:pressed {
                    background-color: #6866e6;
                }
            """)
        else:
            self.sin_btn.setText("sin")
            self.cos_btn.setText("cos")
            self.tan_btn.setText("tan")
            self.inv_btn.setStyleSheet("""
                QPushButton {
                    background-color: #5856d6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #6866e6;
                }
                QPushButton:pressed {
                    background-color: #4846c6;
                }
            """)

    def _toggle_degrees(self):
        """Toggle between radians and degrees mode."""
        self.degrees_mode = not self.degrees_mode
        if self.degrees_mode:
            self.rad_btn.setText("deg")
            self.rad_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7876f6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #8886ff;
                }
                QPushButton:pressed {
                    background-color: #6866e6;
                }
            """)
        else:
            self.rad_btn.setText("rad")
            self.rad_btn.setStyleSheet("""
                QPushButton {
                    background-color: #5856d6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #6866e6;
                }
                QPushButton:pressed {
                    background-color: #4846c6;
                }
            """)

    def _evaluate_expression(self, expr: str) -> float:
        """Evaluate a simple binary expression."""
        operators = ["+", "-", "*", "/", "^", "%"]

        for op in operators:
            if op in expr:
                parts = expr.rsplit(op, 1)
                if len(parts) == 2 and parts[0] and parts[1]:
                    a = float(parts[0])
                    b = float(parts[1])

                    operations = {
                        "+": core.add,
                        "-": core.subtract,
                        "*": core.multiply,
                        "/": core.divide,
                        "^": core.power,
                        "%": core.modulo,
                    }
                    return operations[op](a, b)

        return float(expr)

    def _format_result(self, result: float) -> str:
        """Format a result for display."""
        if result == int(result):
            return str(int(result))
        return f"{result:.10g}"

    def _update_history_list(self):
        """Update the history list widget."""
        self.history_list.clear()
        for entry in self.history.get_all():
            self.history_list.addItem(str(entry))
        self.history_list.scrollToBottom()

    def _on_history_item_clicked(self, item):
        """Handle double-click on history item to reuse result."""
        text = item.text()
        if "=" in text:
            result = text.split("=")[-1].strip()
            self.current_input = result
            self._update_display()

    def _clear_history(self):
        """Clear the calculation history."""
        self.history.clear()
        self.history_list.clear()

    def _switch_mode(self, mode: str):
        """Switch between calculator modes."""
        if mode == self.current_mode:
            return

        self.current_mode = mode
        self.history.clear()
        self.current_input = ""
        self.last_result = None

        if mode == "standard":
            self.mode_stack.setCurrentIndex(0)
            self.history_list.clear()
            self.display.setText("0")
            self.expression_label.setText("")
        elif mode == "programmer":
            self.mode_stack.setCurrentIndex(1)
            self.history_list.clear()

    def _toggle_sidebar(self):
        """Toggle sidebar visibility with animation."""
        self.sidebar_visible = not self.sidebar_visible
        self.toolbar.set_open_state(self.sidebar_visible)

        # Create animation for sidebar
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"pos")
        self.sidebar_animation.setDuration(200)

        if self.sidebar_visible:
            # Show sidebar and overlay
            self.overlay.show()
            self.sidebar.show()
            self.sidebar_animation.setStartValue(QPoint(-200, 50))
            self.sidebar_animation.setEndValue(QPoint(0, 50))
        else:
            # Hide sidebar and overlay
            self.sidebar_animation.setStartValue(QPoint(0, 50))
            self.sidebar_animation.setEndValue(QPoint(-200, 50))
            self.sidebar_animation.finished.connect(self._on_sidebar_close_finished)

        self.sidebar_animation.start()

    def _on_sidebar_close_finished(self):
        """Called when sidebar close animation finishes."""
        if not self.sidebar_visible:
            self.sidebar.hide()
            self.overlay.hide()

    def _on_mode_selected(self, mode: str):
        """Handle mode selection from sidebar."""
        self._switch_mode(mode)
        self.sidebar.set_active_mode(mode)
        if self.sidebar_visible:
            self._toggle_sidebar()

    def resizeEvent(self, event):
        """Handle window resize to reposition overlay and sidebar."""
        super().resizeEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(0, 50, self.width(), self.height() - 50)
        if hasattr(self, 'sidebar'):
            x = 0 if self.sidebar_visible else -200
            self.sidebar.setGeometry(x, 50, 200, self.height() - 50)

    def keyPressEvent(self, event):
        """Handle keyboard input."""
        # Close sidebar on Escape if open
        if event.key() == Qt.Key.Key_Escape and self.sidebar_visible:
            self._toggle_sidebar()
            return

        key = event.text()
        if key.isdigit() or key in "+-*/.^%":
            self._append_to_input(key)
        elif event.key() == Qt.Key.Key_Backspace:
            self.current_input = self.current_input[:-1]
            self._update_display()
        else:
            super().keyPressEvent(event)


def main():
    """Entry point for the calculator GUI."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
