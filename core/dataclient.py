# dataclient.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Classes for linking a GUI Control with a database.

Each DataClient holds details of the data displayed on a control and
provides wrappers for the underlying database functions to support scrolling
and data update in the widget.  It provides an interface allowing each widget
to define, to the data source, the function to call when data in the source
file is changed.

Each DataSource holds details of which clients are to be redisplayed when
data in the source is changed and which primary or secondary index is used
to access data.  Widgets can be added and removed from these lists at will.

Wrappers assume that bsddb functions are called; these are emulated for other
databases.

Reads on secondary indexes return (secondary key, primary key) as (key, value).
An additional read is done using the primary key so that value is always the
primary data in key:value below.
Key is the key for primary reads or (key, value) for secondary reads.
For RECNO (and QUEUE) databases the primary key is a left justified '00'
filled 4 byte string base 256 with low order byte at left when returned
in a secondary read but is an integer when the key in a primary read.

Partial key can be specified to define a key range to be returned.

List of classes:

DataNotify
_DataAccess
DataClient
DataLookup
DataSource

"""
import collections


class DataNotify(object):
    
    """Provide interface to register a callback with a DataSource.

    Use this class to get update notifications but not record and cursor
    access with subclass methods.  Use the get_data_source method to access
    records and cursors with the tools of the underlying database engine.
    
    Methods added:

    get_data_source
    register_in
    register_out
    refresh_widgets
    set_data_source
    set_named_data_sources

    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self):
        """Create null datasource and dictionary for datasource choices."""
        self.datasource = None
        self._datasources = dict()

    def get_data_source(self):
        """Return the current DataSource."""
        return self.datasource

    def register_in(self, datasource, callback):
        """Register callback with datasource for update notification.

        The current registered callback for datasource, if any, is forgotten.

        Subclasses must define any callbacks required.

        """
        if datasource:
            datasource.register_in(self, callback)

    def register_out(self, datasource):
        """Cancel registration with datasource for update notification."""
        if datasource:
            datasource.register_out(self)

    def refresh_widgets(self, instance):
        """Notify registed clients about database update for instance.

        """
        if self.datasource:
            self.datasource.refresh_widgets(instance)

    def set_data_source(self, source=None, callback=None):
        """Set current datasource and update notification callback.

        source can be a DataSource or key of an item in self._datasources.
        callback, if specified, is the method to be used by the DataSource
        instance to notify self that an update has been done.

        self.set_data_source(source=self.datasource, callback=self.callback)
        links this instance to its source and tells the source to use the
        callback method to do update notifications to self.
        self.set_data_source() cancels update notifications to self from the
        current datasource and breaks the link to the datasource.

        """
        if source in self._datasources:
            source = self._datasources[source]
        if source != self.datasource:
            try:
                self.datasource.register_out(self)
            except:
                pass
        self.datasource = source
        try:
            self.datasource.register_in(self, callback)
        except:
            pass

    def set_named_data_sources(self, sources):
        """Update dictionary of named datasources.
        
        Then set_data_source(name, ...) will set self.datasource accordingly.
        None cannot be a key of self._datasources as this is the null value
        for self.datasource.
        
        """
        if not isinstance(sources, dict):
            return
        for n in sources:
            if n not in self._datasources:
                if isinstance(sources[n], DataSource):
                    if n is not None:
                        self._datasources[n] = sources[n]
        

class _DataAccess(DataNotify):
    
    """Provide methods to access records by cursor and do update notifications.
    
    The database must be defined in an instance of a subclass of Database
    and the record definition must be an instance of a subclass of Record.

    This class should not be used directly. Use subclasses defined in this
    module.
    
    Methods added:

    get_record
    set_partial_key
    get_cursor
    get_database
    is_recno
    new_row
    new_row_for_database

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(self):
        """Extend with cursor and partial key."""
        super(_DataAccess, self).__init__()
        self.cursor = None  # should this be in DataClient?
        self.partial = None

    def get_record(self, record):
        """Return record if key matches partial key (if any)."""
        if self.partial == None:
            return record
        else:
            try:
                key, value = record
                if key.startswith(self.partial):
                    return record
            except:
                return None

    def set_partial_key(self, key=None):
        """Set partial key. None removes partial key. False matches no key."""
        if key == None:
            self.partial = None
        elif key == False:
            self.partial = False
        elif len(key):
            self.partial = key
        else:
            self.partial = None

    # Proposed wrappers for DataSource methods follow.
    # Intended as alternative implementation of NullDataSource relying on
    # self.datasource being None.
    # To be removed if idea not implemented.
    
    def get_cursor(self):
        """Return a new cursor for current datasource database."""
        if self.datasource:
            return self.datasource.get_cursor()

    def get_database(self):
        """Return current datasource database."""
        if self.datasource:
            return self.datasource.get_database()

    def is_recno(self):
        """Return True if datasource database has record number keys."""
        if self.datasource:
            return self.datasource.recno

    def new_row(self):
        """Return a row display instance for the datasource.

        The returned instance is not attached to the database.

        The row display instance must be an instance of a class that is a
        subclass of both Record and DataRow.
        
        """
        if self.datasource:
            return self.datasource.new_row()

    def new_row_for_database(self):
        """Return a row display instance for the datasource.

        The returned instance is attached to the database.

        The row display instance must be an instance of a class that is a
        subclass of both Record and DataRow.
        
        """
        if self.datasource:
            return self.datasource.new_row_for_database()


class DataClient(_DataAccess):
    
    """Provide interface to a variable set of contiguous of records on database.

    The signification of contiguous is given by the database engine.  Indexes
    define which records are neighbours and selection criteria define which
    records are seen for inclusion in the variable set.
    
    Methods added:

    clear_client_keys
    close_client_cursor
    make_client_cursor
    load_object
    refresh_cursor

    Methods overridden:

    None

    Methods extended:

    __init__
    set_partial_key
    
    """

    def __init__(self):
        """Extend _DataAccess with variable set of contiguous records.

        self.keys: the variable contiguous set of record keys
                   [(skey, pkey), ...] or [(pkey, value), ...]
        self.rows: number of records to be held in self.keys
        self.objects: the unpickled values for the records in self.keys
                   {(skey, pkey) : unpickled value, ...} or
                   {(pkey, value) : unpickled value, ...}

        """
        super(DataClient, self).__init__()
        self.keys = []
        self.rows = 0
        self.objects = dict()

    def clear_client_keys(self):
        """Delete current keys and objects."""
        self.keys[:] = []
        self.objects.clear()

    def close_client_cursor(self):
        """Close the dataclient cursor."""
        try:
            self.cursor.close()
        except:
            pass
        self.cursor = None

    def make_client_cursor(self, record=None):
        """Return current record after creating and positioning a cursor."""
        if not self.cursor:
            self.cursor = self.datasource.get_cursor()
        elif not self.cursor.database_cursor_exists():
            self.cursor = self.datasource.get_cursor()
        self.cursor.set_partial_key(self.partial)
        if record != None:
            return self.cursor.setat(record)

    def load_object(self, key):
        """Create a new row and populate it with data from record for key."""
        newrow = self.datasource.new_row()
        self.objects[key] = newrow
        newrow.load_instance(
            self.datasource.dbhome,
            self.datasource.dbset,
            self.datasource.dbname,
            key)

    def refresh_cursor(self):
        """Modify cursor data structures after database update.

        A database engine dependant action.  The called refresh_recordset
        method will do anything needed.

        """
        # The last change while this module was in rmappsup adjusted cursor
        # management to keep the cursor for a datagrid between scrolling
        # actions rather than destroy it and create a new one next time.
        # The problem was the time take to position the new cursor towards
        # the end of large recordsets in DPT.  This introduced the problem of
        # dealing with record deletion and addition because the DPT foundsets
        # may no longer agree with the existence bitmap.
        if self.cursor:
            self.cursor.refresh_recordset()

    def set_partial_key(self, key=None):
        """Set a partial key. key=None unsets partial key."""
        super(DataClient, self).set_partial_key(key)
        if self.cursor:
            self.cursor.set_partial_key(self.partial)

        
class DataLookup(_DataAccess):
    
    """Provide a variable cache of records from a database with unique keys.

    Use of this class is restricted to cases where the key is associated
    with a single value.
    
    Methods added:

    close (not sure why this exists)
    load_cache
    on_data_change (not implemented)

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(self):
        """Extend _DataAccess with variable cache of records.

        self.keys: the variable set of record keys
                   [pkey1, pkey2, ...] or [skey1, skey2, ...]
        self.rowmax: maximum number of records to be held in self.keys
        self.rowmin: number of records to be held in self.keys after
                     trimming when self.rowmax reached
        self.cache: the unpickled values for the records in self.keys
                   {pkey : unpickled value, ...} or
                   {skey : unpickled primary value, ...}

        """
        super(DataLookup, self).__init__()
        self.keys = []
        self.rowmax = 100
        self.rowmin = 10
        self.cache = dict()

    def close(self):
        """Not implemented."""
        pass

    def load_cache(self, key):
        """Return new row for record key from cache after adding if absent.

        Delete old entries if necessary to keep within cache size limits.

        """
        if key in self.cache:
            return self.cache[key]
        else:
            record = self.get_record(self.datasource.get_database().get(key))
            if record:
                value = (key, record)
            else:
                return None
            newrow = self.datasource.new_row()
            newrow.load_instance(
                self.datasource.dbhome,
                self.datasource.dsname,
                value)
            self.cache[key] = newrow
            self.keys.append(key)
            if len(self.keys) > self.rowmax:
                cache = self.cache
                for k in self.keys[:-self.rowmin]:
                    del cache[k]
                del self.keys[:-self.rowmin]
            return newrow

    def on_data_change(self, instance):
        """Not implemented.

        Object changed added or deleted
        If instance.newrecord is False then object was added.
        If instance.newrecord is None or absent then object was deleted.
        Otherwise object.newrecord replaced object.
        Exact behaviour depends on use of set_data_source method.

        Not sure of detail yet but it may be that this class maintains
        the lookup cache and controls refresh of client displays.
        
        """
        print(self, 'Lookup data change')
        print(instance)
        

class DataSource(object):
    
    """Provide interface to database records and update notifications.
    
    This class is designed to work with records defined by subclasses of
    Record accesed via subclasses of DataNotify.
    
    Methods added:

    get_cursor
    get_database
    new_row
    new_row_for_database
    register_in
    register_out
    refresh_widgets

    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        
        """Define a DataSource on a database.

        dbhome = instance of a subclass of Database.
        dbset = name of set of associated databases in dbhome to be accessed.
        dbname = name of database in dbset to be accessed.
        newrow = class used to generate new records in dbname database.
        
        """
        self.clients = {}
        if dbhome.exists(dbset, dbname):
            self.dbhome = dbhome
            self.dbset = dbset
            self.dbname = dbname
            self.primary = dbhome.is_primary(dbset, dbname)
            self.recno = dbhome.is_recno(dbset, dbname)
        else:
            self.dbhome = None
            self.dbset = None
            self.dbname = None
            self.primary = None
            self.recno = None
        self.newrow = newrow
        
    def get_cursor(self):
        """Create and return a cursor on the database."""
        return self.dbhome.database_cursor(self.dbset, self.dbname)

    def get_database(self):
        """Return database currently attached to datasource."""
        return self.dbhome.get_database(self.dbset, self.dbname)

    def new_row(self):
        """Return a new row but do not attach it to database."""
        return self.newrow()

    def new_row_for_database(self):
        """Return a new row after attaching it to database.

        Rows are usually created by new_row in association with
        unpickle and the database attachment made then.  Sometimes
        a row is created that needs the database information, a
        header row or a new record perhaps, as part of setup.
        
        """
        newrow = self.newrow()
        newrow.set_database(self.dbhome)
        newrow.dbname = self.dbname
        return newrow

    def register_in(self, client, callback):
        """Register client for update notification using callback."""
        if isinstance(callback, collections.Callable):
            self.clients[client] = callback

    def register_out(self, client):
        """Cancel registration of client for update notification."""
        if client in self.clients:
            del self.clients[client]

    def refresh_widgets(self, instance):
        """Notify registered clients about database update for instance."""
        for w in self.clients:
            self.clients[w](instance)

    @property
    def dbidentity(self):
        """"""
        return id(self.dbhome.get_database(self.dbset, self.dbset))

