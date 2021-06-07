# datadelete.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Record and dialogue support for delete record classes.

List of classes:

RecordDelete - record deletion and data update notification
DataDelete - record delete dialogue

"""

import Tkinter

from gridsup.core.dataclient import DataClient

# minimum_width and mininimum_height arguments for wm_minsize() calls
# maybe candidate arguments for DataControl.edit_dialog() calls elsewhere
minimum_width = 600
minimum_height = 200


class RecordDelete(DataClient):
    
    """Delete a DB record.
    
    Methods added:

    delete - delete record if instance attached to database
    on_data_change - block update if record for instance changed elsewhere

    Methods overridden:

    None

    Methods extended:

    __init__ - extend DataClient identifying instance being deleted
    
    """

    def __init__(self, instance):
        """Extend DataClient to identify instance being deleted.

        self.rows: DataClient provides one record
        self.object: the record to be deleted
        self.object.newrecord: no new object
        self.blockchange: allow deletion unless on_data_change blocks it

        """
        super(RecordDelete, self).__init__()
        self.rows = 1
        self.object = instance
        self.object.newrecord = None
        self.blockchange = False

    def delete(self, commit=True):
        """Delete the record and refresh widgets

        The datasource must be set by a call to set_data_source (inherited
        from DataClient) to allow delete to happen.  That call should also
        specify on_data_change as the update notification callback to prevent
        deletion proceeding if the record is changed elsewhere first.

        """
        self.datasource.dbhome.make_internal_cursors()
        self.object.delete_record(
            self.datasource.dbhome,
            self.datasource.dbset)
        if commit:
            self.datasource.dbhome.commit()
        self.datasource.dbhome.close_internal_cursors()
        self.datasource.refresh_widgets(self.object)

    def on_data_change(self, instance):
        """Block record deletion if instance is record being deleted.

        Implication is that record has been modified separately and it is
        not correct to delete based on the record as held in self.
        
        """
        if instance == self.object:
            self.blockchange = True
        

class DataDelete(RecordDelete):
    
    """Provide a delete record dialogue
    
    Methods added:

    dialog_clear_error_markers
    dialog_on_cancel
    dialog_on_ok
    dialog_status

    Methods overridden:

    None

    Methods extended:

    __init__
    on_data_change
    
    """

    def __init__(self, instance, parent, oldview, title):
        """Extend RecordDelete with dialogue widgets for delete instance."""
        super(DataDelete, self).__init__(instance)
        oldview.get_top_widget().pack(fill=Tkinter.BOTH, expand=Tkinter.TRUE)
        oldview.get_top_widget().pack_propagate(False)
        oldview.takefocus_widget.configure(takefocus=Tkinter.TRUE)
        oldview.takefocus_widget.focus_set()
        self.parent = parent
        parent.wm_title(title)
        parent.wm_minsize(width=minimum_width, height=minimum_height)
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
        super(DataDelete, self).on_data_change(instance)
        if self.blockchange:
            if self.ok:
                self.ok.destroy()
                self.ok = None

    def dialog_ok(self):
        """Delete record and return delete action response (True for deleted).

        Check that database is open and is same one as deletion action was
        started.

        """
        if self.datasource is not None:
            if self.datasource.dbhome.get_database(
                self.datasource.dbset, self.datasource.dbset):
                self.delete()
                return True
            else:
                self.status.configure(
                    text='Cannot delete because original database was closed')
                if self.ok:
                    self.ok.destroy()
                    self.ok = None
                self.blockchange = True
                return False

    def dialog_on_ok(self):
        """Delete record and destroy dialogue on Ok response.

        Deletion is not allowed if the record has been changed since start
        of delete action or the database has been closed since then.

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
        else:
            self.status.configure(
                text='Cannot delete because not connected to a database')
