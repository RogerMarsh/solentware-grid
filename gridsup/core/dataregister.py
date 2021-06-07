# dataregister.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide a way to link Controls to the database updates of interest.

These classes are designed to work with the classes in dataclient.py

List of classes:

DataRegister

"""


class DataRegister(object):
    
    """Register the interest of a DataControl in updates to an index.
    
    Maintain a dictionary of callback methods:
    self._datasources[(db, file, index)][control] = callback
    Notify updates by refresh_after_update(updated index, updated instance).
    The instance may contain data for several indexes that have been updated
    with the update being driven from a control using one of these. This
    dictionary allows the indexes to be cross referenced so that all controls
    that may be displaying the updated instance get a chance to refresh.
    
    Methods added:

    refresh_at_start_of_file
    refresh_after_update
    register_in
    register_out

    Methods overridden:

    None
    
    Methods extended:

    __init__
    
    """

    def __init__(self, **kargs):
        """Create an empty register of datasources"""
        super(DataRegister, self).__init__()
        self.datasources = dict()

    def refresh_at_start_of_file(self):
        """Refresh all registered data clients and position at start of file.

        Clear all selections on all clients (subclasses of
        _DataAccess) in self._datasources and position datagrid for
        client at start of file.
        Sample use after updating and deleting many records in one
        transaction to remove references to deleted records and index
        values.
        
        """
        sources = self.datasources
        clients = set()
        for key in sources:
            for c in sources[key]:
                clients.add(c)
        for c in clients:
            c.load_new_index()

    def refresh_after_update(self, dskey, instance):
        """Call registered callbacks for updates to dskey index by instance.
        
        instance can be None which the callback will likely interpret as
        refresh as close as possible to existing display.
        
        """
        if dskey in self.datasources:
            for client in self.datasources[dskey]:
                self.datasources[dskey][client](instance)

    def register_in(self, client, callback):
        """Register callback for updates to current DataSource of client."""
        source = client.datasource
        key = (source.dbhome, source.dbset, source.dbname)
        if key not in self.datasources:
            self.datasources[key] = dict()
        self.datasources[key][client] = callback

    def register_out(self, client):
        """Remove callbacks for current DataSource of client from register.
        
        Clear the register if client is None.
        
        """
        if client is None:
            self.datasources.clear()
            return
        source = client.datasource
        key = (source.dbhome, source.dbset, source.dbname)
        if key in self.datasources:
            if client in self.datasources[key]:
                del self.datasources[key][client]
                if not len(self.datasources[key]):
                    del self.datasources[key]

