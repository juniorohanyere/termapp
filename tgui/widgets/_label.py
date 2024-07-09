"""Label module.
"""

import curses
from curses import panel

from ._widget import Widget


class Label(Widget):
    def __init__(self, layout, **kwargs):
        """None means to fit content (curses.window.resize is called).
        0 means to fill parent.
        anchor depends on master (the current layout in view/use).
        text, multiline, and align works together.

        Args:
            layout (obj): layout object, can't be a Nonetype object.
            kwargs (dict): variable length keyworded arguments.
                text = None
                -> text = str(value)

                multiline = bool(x)

                align = str(pos)

                size = None
                -> size = (int(height), int(width))

                anchor = None
                -> anchor = (int(y), int(x))

                color = None
                -> color = (int(fg), int(bg))

                padding = int(value)
                -> padding = (int(left), int(right), int(top), int(bottom))
        """

        kw = {'text': None, 'multiline': False, 'align': 'left', 'size': None,
              'anchor': None, 'color': None, 'padding': 1}

        for key, value in kwargs.items():
            if key not in kw.keys():
                err = 'Label.__init__() got an unexpected keyword argument '
                err += f"'{key}'"
                raise TypeError(err)

                return 1    # XXX kinda buggy

            kw[key] = value

        super().__init__(**kw)

        # TODO check if layout is a valid layout object
        self._layout = layout

        # now create a new label widget
        self._create_label()

    def set_anchor(self, y, x):
        """Set anchor for the label.
        """
