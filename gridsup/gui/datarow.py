# datarow.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Define basic interface for setting properties of a row in a datagrid.

DataRow provides methods to set background colour of row to match selection
state.  Subclasses will supply methods appropriate to application.

List of classes:

DataRowError - Exceptions
DataHeader
DataRow

"""

import Tkinter

NULL_COLOUR = '#d9d9d9' # system backgound
SELECTION_COLOUR = '#76d9d9' # a light blue
BOOKMARK_COLOUR = '#86d929' # a light green
SELECTION_CYCLE_COLOUR = '#eb3010' # a dark orange
SELECTION_AND_BOOKMARK_COLOUR = '#e0f113' # a pale yellow

# keys for header and row specification dictionaries
GRID_COLUMNCONFIGURE = 1
GRID_CONFIGURE = 2
WIDGET_CONFIGURE = 3
WIDGET = 4
ROW = 5

_widget_configure = set((
    'background', 'font'))


class DataRowError(StandardError):
    pass


class DataHeader(object):
    
    """Provide methods to create a new header and configure its widgets.

    Methods added:

    grid_header_row
    make_header_widgets

    Methods overridden:

    None

    Methods extended:

    __init__

    """
    def __init__(self):
        """Extend with placeholder for header specification."""
        super(DataHeader, self).__init__()
        self.header_specification = ()

    # Not necessarily best but minimum change to get this out of DataRow
    # Now we are there: is this method needed at all?
    def grid_header_row(self, specification):
        """Return (<method>)

        master for header row widget is not known when header created.
        
        """
        self.header_specification = specification
        return (self.make_header_widgets)

    def make_header_widgets(self, widget, parent):
        """Create a header widget for columns with titles from items.

        widget - widget pool manager
        parent - master for row widget

        """
        # Maybe return dictionary of widgets with (row, col) as keys?
        # If spec per instance set spec[TEXT] in grid_row() call?
        row = []
        for spec in self.header_specification:
            wconf = spec[WIDGET_CONFIGURE].copy()
            w = widget(spec[WIDGET])
            if w is None:
                w = spec[WIDGET](master=parent)
            w.configure(background=NULL_COLOUR, **wconf)
            w.grid_configure(spec[GRID_CONFIGURE])
            parent.grid_columnconfigure(
                spec[GRID_CONFIGURE]['column'],
                spec[GRID_COLUMNCONFIGURE])
            row.append((w, spec[GRID_CONFIGURE]))
        return (row,)


class DataRow(object):
    
    """Provide methods to create a new row and set background colour of a row.

    Set row properties based on selection status.
    Subclass must override methods grid_row.
    
    Typical use is
    class FooRecord(Record):
        ...
    class FooRow(FooRecord, DataRow):
        ...

    Methods added:

    set_background - Set row background colour
    set_background_bookmark - Set background colour for bookmarked row
    set_background_bookmarked_selection - Set background colour for selected
    bookmarked row
    set_background_normal - Set default background colour for row
    set_background_selection - Set background colour for active selected row
    set_background_selection_cycle - Set background colour for selected rows
    form_row - raise DataRow error 'form_row not implemented'
    grid_row
    grid_row_bookmark - Return new row with bookmarked background colour
    grid_row_bookmarked_selection - Return new row with selected bookmarked
    background colour
    grid_row_normal - Return new row with default background colour
    grid_row_selection - Return new row with active selection background colour
    grid_row_selection_cycle - Return new row with selcted background colour
    make_row_widgets

    Methods overridden:

    None

    Methods extended:

    None
    
    """
    # background argument to be put in kargs throughout.
    # This becomes obvious thing to do with removal of row widget

    def set_background(self, widgets, background):
        """Set background colour of widgets.

        widgets - list((widget, specification), ...).
        background - the background colour.

        Each element of widgets will have been created by make_row_widgets()
        or DataHeader.make_header_widgets() and reused by DataGrid instance
        in a data row.

        """
        for w in widgets:
            w[0].configure(background=background)

    def set_background_bookmark(self, widgets):
        self.set_background(widgets, BOOKMARK_COLOUR)

    def set_background_bookmarked_selection(self, widgets):
        self.set_background(widgets, SELECTION_AND_BOOKMARK_COLOUR)

    def set_background_normal(self, widgets):
        self.set_background(widgets, NULL_COLOUR)

    def set_background_selection(self, widgets):
        self.set_background(widgets, SELECTION_COLOUR)

    def set_background_selection_cycle(self, widgets):
        self.set_background(widgets, SELECTION_CYCLE_COLOUR)

    def form_row(self, parent, rowsizer):
        '''Not implemented.'''
        # Arguments unchanged from wxPython revisions
        raise DataRowError, 'form_row not implemented'

    def grid_row(self, textitems=(), **kargs):
        """Subclasses return (<row maker method>, <data items>, <configuration>)
        """
        configure = dict()
        for attr in kargs:
            if attr in _widget_configure:
                configure[attr] = kargs[attr]
        return (self.make_row_widgets, textitems, configure)

    def grid_row_bookmark(self, **kargs):
        return self.grid_row(background=BOOKMARK_COLOUR, **kargs)

    def grid_row_bookmarked_selection(self, **kargs):
        return self.grid_row(background=SELECTION_AND_BOOKMARK_COLOUR, **kargs)

    def grid_row_normal(self, **kargs):
        return self.grid_row(background=NULL_COLOUR, **kargs)

    def grid_row_selection(self, **kargs):
        return self.grid_row(background=SELECTION_COLOUR, **kargs)

    def grid_row_selection_cycle(self, **kargs):
        return self.grid_row(background=SELECTION_CYCLE_COLOUR, **kargs)

    def make_row_widgets(self, widget, parent, items, **kargs):
        """Create row of widgets with data for each column from items.

        widget - function that returns an existing available widget or None
        parent - master for row of widgets
        items - tuple of text option values for widget configure command.
        **kargs - widget configure options to override spec for all row widgets

        """
        # Maybe return dictionary of widgets with (row, col) as keys?
        # If spec per instance set spec[TEXT] in grid_row() call?
        row = []
        for item, spec in zip(items, self.row_specification):
            wconf = spec[WIDGET_CONFIGURE].copy()
            for attr in kargs:
                if attr not in wconf:
                    wconf[attr] = kargs[attr]
            w = widget(spec[WIDGET])
            if w is None:
                w = spec[WIDGET](master=parent)
            # populate_widget is Tkinter.Label.configure by default
            # Typical subclass override is populate and format the Text widget
            # passed as w argument from the item passed as text argument.
            self.populate_widget(w, text=item, **wconf)
            row.append((w, spec[GRID_CONFIGURE]))
        return (row,)

    populate_widget = Tkinter.Label.configure

