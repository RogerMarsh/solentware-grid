# dataedit.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Record and dialogue support for edit record classes.

List of classes:

RecordEdit - record edit and data update notification
DataEdit - tab management for record edit widgets (not implemented)

"""

from gridsup.core.dataclient import DataClient


class RecordEdit(DataClient):

    """Edit or insert a DB record.
    
    Methods added:

    edit - edit record if instance attached to database
    on_data_change - block update if record for instance changed elsewhere
    put - insert record

    Methods overridden:

    None

    Methods extended:

    __init__ - extend DataClient identifying instance being edited or inserted
    
    """

    def __init__(self, newobject, oldobject):
        """Extend DataClient to identify instance being edited or inserted.

        self.rows: DataClient provides one record
        self.newobject: the record to be inserted or the replacement record
        self.oldobject: the record being replaced or None if insertion
        self.newobject.newrecord: this is new or replacement record
        self.blockchange: True means prevent deletion when requested

        """
        DataClient.__init__(self)
        self.rows = 1
        self.newobject = newobject
        self.oldobject = oldobject
        self.newobject.newrecord = False
        self.blockchange = False

    def edit(self):
        """Return True if record is edited

        The datasource must be set by a call to set_data_source (inherited
        from DataClient) to allow edit to happen.  That call should also
        specify on_data_change as the update notification callback to prevent
        edit proceeding if the record is changed elsewhere first.

        """
        self.datasource.dbhome.make_internal_cursors()
        r = self.oldobject.edit_record(
            self.datasource.dbhome,
            self.datasource.dbset,
            self.datasource.dbname,
            self.newobject)
        self.datasource.dbhome.close_internal_cursors()
        self.datasource.refresh_widgets(self.oldobject)
        return r
        
    def on_data_change(self, instance):
        """Block record edit if instance is record being edited.

        Implication is that record has been modified separately and it is
        not correct to edit based on the record as held in self.
        
        """
        try:
            if instance == self.oldobject:
                self.blockchange = True
        except AttributeError:
            pass
        
    def put(self):
        """Return key of inserted record"""
        self.datasource.dbhome.make_internal_cursors()
        r = self.newobject.put_record(
            self.datasource.dbhome,
            self.datasource.dbset)
        self.datasource.dbhome.close_internal_cursors()
        self.datasource.refresh_widgets(self.newobject)
        return r
        

class DataEdit(RecordEdit):
    
    """Provide tab management for edit dialog
    
    Methods added:

    destroy_children - does nothing
    tab_focus - cannot work, still wxWidgets calls

    Methods overridden:

    None

    Methods extended:

    __init__ - extend RecordDelete identifying parent widget
    
    """

    def __init__(self, newobject, parent, oldobject, showinitial=True):
        """Extend RecordEdit with parent widget."""
        RecordEdit.__init__(self, newobject, oldobject)
        self.parent = parent
        self.showinitial = showinitial
        self.tab = []

    def destroy_children(self, item, parentsizer=None):
        """Destroy redundant widgets on deletion request."""
        # not sure what Tkinter version should do or if it is needed
        # parentsizer is a relic from wxWidgets version
        pass

    def tab_focus(self, event=None):
        """Tab management.

        ????????????
        The SetFocus event handler is expected to ensure that the control
        receiving focus is in the visible portion of the widget.
        """
        
        if event == None:
            if len(self.tab):
                self.tab[0].SetFocus()
            return

        if event.AltDown() or event.ControlDown() or event.MetaDown():
            return

        if self.parent.FindFocus() not in self.tab:
            if len(self.tab):
                self.tab[0].SetFocus()
            return

        if event.ShiftDown():
            self.tab.insert(0, self.tab.pop(-1))
        else:
            self.tab.append(self.tab.pop(0))
        self.tab[0].SetFocus()
