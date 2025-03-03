# ========== HELPER FUNCS ==========
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


def change_opacity(widget: QWidget, value: float):
    op = QGraphicsOpacityEffect(widget)
    op.setOpacity(value)
    widget.setGraphicsEffect(op)
    widget.setAutoFillBackground(True)