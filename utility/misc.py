## @file misc.py
## @brief Miscellaneous helper functions
##
## Contains utility functions used across the application.

from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

## @brief Changes the opacity of a widget
## @param widget The Qt widget to modify
## @param value Opacity value between 0.0 (fully transparent) and 1.0 (fully opaque)
## @return None
def change_opacity(widget: QWidget, value: float):
    op = QGraphicsOpacityEffect(widget)
    op.setOpacity(value)
    widget.setGraphicsEffect(op)
    widget.setAutoFillBackground(True)