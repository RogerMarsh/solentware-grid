# datadelete.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Record and dialogue support for delete record classes.

List of classes:

RecordDelete - record deletion and data update notification
DataDelete - tab management for record deletion widgets (not implemented)

"""

from gridsup.core.dataclient import DataClient


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
        DataClient.__init__(self)
        self.rows = 1
        self.object = instance
        self.object.newrecord = None
        self.blockchange = False

    def delete(self):
        """Return True if record is deleted

        The datasource must be set by a call to set_data_source (inherited
        from DataClient) to allow delete to happen.  That call should also
        specify on_data_change as the update notification callback to prevent
        deletion proceeding if the record is changed elsewhere first.

        """
        if self.datasource is not None:
            self.datasource.dbhome.make_internal_cursors()
            self.object.delete_record(
                self.datasource.dbhome,
                self.datasource.dbset)
            self.datasource.dbhome.close_internal_cursors()
            self.datasource.refresh_widgets(self.object)
            return True

    def on_data_change(self, instance):
        """Block record deletion if instance is record being deleted.

        Implication is that record has been modified separately and it is
        not correct to delete based on the record as held in self.
        
        """
        if instance == self.object:
            self.blockchange = True
        

class DataDelete(RecordDelete):
    
    """Provide tab management for delete dialog
    
    Methods added:

    destroy_children - does nothing

    Methods overridden:

    None

    Methods extended:

    __init__ - extend RecordDelete identifying parent widget
    
    """

    def __init__(self,
                 instance,
                 parent):
        """Extend RecordDelete with parent widget."""
        RecordDelete.__init__(self, instance)
        self.parent = parent
        
    def destroy_children(self, item, parentsizer=None):
        """Destroy redundant widgets on deletion request."""
        # not sure what Tkinter version should do or if it is needed
        # parentsizer is a relic from wxWidgets version
        pass
