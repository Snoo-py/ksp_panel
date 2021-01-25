from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt


class KspMFDButton(QWidget):

    def __init__(self, parent=None, mfd=None, width=5, height=5):
        QWidget.__init__(self)
        self._out_size = 700
        self._button_size = 40
        self.setParent(parent)
        self.setFixedSize(self._out_size, self._out_size)
        self.mfd = mfd
        self._draw_buttons()


        self.mfd.setParent(self)
        self.mfd.resize(self._in_size, self._in_size)
        self.mfd.move(self._button_size, self._button_size)


    def _draw_buttons(self):
        button_offset = 2 * self._button_size
        button_count = 5
        button_gap = (self._in_size - ((2 + button_count) * self._button_size)) / (button_count - 1)
        for r in range(0, button_count):
            # Top
            self._create_button('T%s' % (r + 1), button_offset, 0)
            # Right
            self._create_button('R%s' % (r + 1), self._in_size + self._button_size, button_offset)
            # Bottom
            self._create_button('B%s' % (r + 1), button_offset, self._in_size + self._button_size)
            # Left
            self._create_button('L%s' % (r + 1), 0, button_offset)
            button_offset += self._button_size + button_gap


    def _create_button(self, button_name, x, y):
        text, handler = self.mfd.get_button_info(button_name)
        button = QPushButton(text, self)
        button.setFixedSize(self._button_size, self._button_size)
        button.move(x, y)
        try:
            button.clicked.disconnect()
        except Exception:
            pass
        if handler:
            button.setEnabled(True)
            button.setFocusPolicy(Qt.NoFocus)
            button.clicked.connect(handler)
        else:
            button.setEnabled(False)


    @property
    def _in_size(self):
        return self._out_size - 2 * self._button_size