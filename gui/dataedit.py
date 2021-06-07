# dataedit.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Record and dialogue support for edit record classes.

List of classes:

RecordEdit - record edit and data update notification
DataEdit - record edit and insert dialogue

"""

import Tkinter

from gridsup.core.dataclient import DataClient

# minimum_width and mininimum_height arguments for wm_minsize() calls
# maybe candidate arguments for DataControl.edit_dialog() calls elsewhere
minimum_width = 800
minimum_height = 300


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
        super(RecordEdit, self).__init__()
        self.rows = 1
        self.newobject = newobject
        self.oldobject = oldobject
        self.newobject.newrecord = False
        self.blockchange = False

    def edit(self, commit=True):
        """Edit the record and refresh widgets

        The datasource must be set by a call to set_data_source (inherited
        from DataClient) to allow edit to happen.  That call should also
        specify on_data_change as the update notification callback to prevent
        edit proceeding if the record is changed elsewhere first.

        """
        self.datasource.dbhome.make_internal_cursors()
        self.oldobject.edit_record(
            self.datasource.dbhome,
            self.datasource.dbset,
            self.datasource.dbname,
            self.newobject)
        if commit:
            self.datasource.dbhome.commit()
        self.datasource.dbhome.close_internal_cursors()
        self.datasource.refresh_widgets(self.oldobject)
        
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
        
    def put(self, commit=True):
        """Insert the record and refresh widgets"""
        self.datasource.dbhome.make_internal_cursors()
        self.newobject.put_record(
            self.datasource.dbhome,
            self.datasource.dbset)
        if commit:
            self.datasource.dbhome.commit()
        self.datasource.dbhome.close_internal_cursors()
        self.datasource.refresh_widgets(self.newobject)
        

class DataEdit(RecordEdit):
    
    """Provide an edit and insert record dialogue
    
    Methods added:

    dialog_clear_error_markers
    dialog_ok
    dialog_on_cancel
    dialog_on_ok

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(
        self,
        newobject,
        parent,
        oldobject,
        newview,
        title,
        oldview=None,
        ):
        """Extend RecordEdit with dialogue widgets for edit objects."""
        super(DataEdit, self).__init__(newobject, oldobject)
        self.parent = parent
        parent.wm_title(title)
        parent.wm_minsize(width=minimum_width, height=minimum_height)
        if oldview:
            oldview.get_top_widget().pack(
                fill=Tkinter.BOTH, expand=Tkinter.TRUE)
            oldview.get_top_widget().pack_propagate(False)
            oldview.takefocus_widget.configure(takefocus=Tkinter.TRUE)
        newview.get_top_widget().pack(fill=Tkinter.BOTH, expand=Tkinter.TRUE)
        newview.get_top_widget().pack_propagate(False)
        newview.takefocus_widget.configure(takefocus=Tkinter.TRUE)
        newview.takefocus_widget.focus_set()
        self.status = Tkinter.Label(parent)
        self.status.pack(side=Tkinter.BOTTOM)
        self.buttons = Tkinter.Frame(parent)
        self.buttons.pack(
            fill=Tkinter.X,
            expand=Tkinter.FALSE,
            side=Tkinter.TOP)
        self.ok = Tkinter.Button(
            master=self.buttons,
            text='Ok',
            command=self.try_command(self.dialog_on_ok, self.buttons))
        self.ok.pack(expand=Tkinter.TRUE, side=Tkinter.LEFT)
        self.cancel = Tkinter.Button(
            master=self.buttons,
            text='Cancel',
            command=self.try_command(self.dialog_on_cancel, self.buttons))
        self.cancel.pack(expand=Tkinter.TRUE, side=Tkinter.LEFT)
        self.newview = newview

    def dialog_clear_error_markers(self):
        """Set status report to ''."""
        self.status.configure(text='')

    def dialog_on_cancel(self):
        """Destroy dialogue on Cancel response in dialogue."""
        self.parent.destroy()
        self.set_data_source()
        
    def dialog_status(self):
        """Return widget used to display status reports and error messages."""
        return self.status

    def on_data_change(self, instance):
        """Block record deletion if instance is record being deleted.

        Implication is that record has been modified separately and it is
        not correct to delete based on the record as held in self.
        
        """
        super(DataEdit, self).on_data_change(instance)
        if self.blockchange:
            if self.ok:
                self.ok.destroy()
                self.ok = None

    def dialog_on_ok(self):
        """Update record and destroy dialogue on Ok response.

        Update is not allowed if the record has been changed since start
        of update action or the database has been closed since then.

        """
        self.dialog_clear_error_markers()
        if self.blockchange:
            self.status.configure(
                text=' '.join((
                    'Cannot delete because the record has',
                    'been changed since this dialogue opened.',
                    )))
            self.ok.destroy()
            self.ok = None
            return
        dok = self.dialog_ok()
        if dok:
            self.parent.destroy()
            self.set_data_source()
        elif dok is False:
            pass
        elif self.oldobject is None:
            self.status.configure(
                text=' '.join((
                    'Record inserted.  Start another dialogue to continue',
                    'editing the record.',
                    )))
        else:
            self.status.configure(
                text=' '.join((
                    'Edit applied.  Start another dialogue to continue',
                    'editing the record.',
                    )))
        
    def dialog_ok(self):
        """Update record and return update action response (True for updated).

        Check that database is open and is same one as update action was
        started.

        """
        if self.datasource.dbhome.get_database(
            self.datasource.dbset, self.datasource.dbset) is None:
            self.status.configure(
                text='Cannot update because original database was closed')
            if self.ok:
                self.ok.destroy()
                self.ok = None
            self.blockchange = True
            return False
        if self.oldobject is not None:
            if self.newobject == self.oldobject:
                self.status.configure(text='No changes to record')
                return False
            self.edit()
            return True
        else:
            self.newobject.set_database(self.datasource.dbhome)
            self.newobject.key.game = 0
            self.put()
            return True
