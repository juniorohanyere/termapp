import curses
from curses import panel

from ._widget import Widget


class Label(Widget):
    def __init__(self, master, **kwargs):
        """None means to fit content (curses.window.resize is called)
        0 means to fill parent
        pos_y and pos_x depends on master (the current layout in use)

        padding can be an integer or tuple of integers:
        padding = padding
        padding = (padding_left, padding_right, padding_top, padding_bottom)

        Multiline and alignment works together.
        """

        kw = {'text': None, 'multiline': False, 'size': None, 'anchor': None,
              'color': None, 'padding': 1}

        for key, value in kwargs.items():
            if key not in kw.keys():
                error = 'Label.__init__() got an unexpected keyword argument '
                error += f"'{key}'"
                raise TypeError(error)

                return 1

            kw[key] = value

        super(Label, self).__init__(kw)

        self._master = master

        # now create a new widget as label
        self._win, self._pan = self._create_label()

    def set_anchor(self, anchor_y, anchor_x):
        """Set anchor for the label.
        """
        # if isinstance(self.master, LinearLayout):

