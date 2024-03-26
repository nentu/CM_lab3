def clear_box(layout):
    for x in reversed(range(layout.count())):
        widget = layout.takeAt(x).widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_box(layout.takeAt(x).layout())
