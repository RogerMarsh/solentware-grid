# sqlite3datasource.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Emulate DPT record sets and provide bsddb style access.

Typical use is:
Build a dictionary representing a record set.  Call set_recordset(<dictionary>)
to give the cursor a sorted record set.  The DBDataSource instance links the
sorted record set to a grid control (GUI) to display the records in a
scrollable list.

List of classes

Sqlite3DataSource
CursorRS

"""

from basesup.api.database import Cursor

from ..core.dataclient import DataSource


class Sqlite3DataSource(DataSource):
    
    """Define an interface between a database and GUI controls.
    
    The database is an instance of a subclass of ./dbapi.DBapi.
    
    Methods added:

    set_recordset

    Methods overridden:

    get_cursor

    Methods extended:

    __init__
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Define an interface between DPT database and GUI controls.
        
        See superclass for description of arguments.

        """
        super(Sqlite3DataSource, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.keymap = dict()
        self.recordset = []
        
    def get_cursor(self):
        """Return cursor on the record set associated with datasource."""
        return CursorRS(self.keymap, self.recordset)

    def set_recordset(self, records):
        """Set self.recordset to sorted records (a dictionary)."""
        records.sort()
        self.recordset = records
        self.keymap.clear()
        for k, v in self.recordset:
            self.keymap[k] = len(self.keymap)


class CursorRS(Cursor):
    
    """A Cursor cursor that does not implement partial keys.
    
    If a subset of the records on self.recordset is needed do more selection
    to get the subset and pass this to the cursor.

    Methods added:

    database_cursor_exists

    Methods overridden:

    close
    count_records
    first
    get_partial
    get_record_at_position
    last
    set_partial_key
    nearest
    next
    prev
    setat

    Methods extended:

    __init__
    
    """

    def __init__(self, keymap, recordset):
        """Define a cursor to access recordset in the order given in keymap."""
        super(CursorRS, self).__init__(None)

        self.current = None
        self.direct = keymap
        self.records = recordset

    def close(self):

        self.current = None
        self.direct = None
        self.records = None

    def count_records(self):
        """return record count or None"""
        try:
            return len(self.records)
        except:
            return None

    def database_cursor_exists(self):
        """Return True if self.records is not None and False otherwise

        Simulates existence test for a database cursor.

        """
        # The cursor methods are defined in this class and operate on
        # self.records if it is a list so do that test here as well.
        return self.records is not None

    def first(self):
        """Return first record."""
        if self.records is None:
            return None
        if len(self.records):
            self.current = 0
            return self.records[self.current]

    def get_position_of_record(self, record=None):
        """return position of record in file or 0 (zero)"""
        try:
            return self.records.index(record)
        except ValueError:
            return 0

    def get_record_at_position(self, position=None):
        """return record for positionth record in file or None"""
        try:
            return self.records[position]
        except IndexError:
            return None
        except TypeError:
            if position is None:
                return None
            raise

    def last(self):
        """Return last record."""
        if self.records is None:
            return None
        if len(self.records):
            self.current = len(self.records) - 1
            return self.records[self.current]

    def set_partial_key(self, partial):
        """Set partial key to None.  Always.
        
        Always set to None because the recordset oand keymap should be trimmed
        to the required records before passing to the cursor.
        
        """
        self._partial = None
        
    def nearest(self, key):
        """Return nearest record."""
        if self.records is not None:
            if key in self.direct:
                n = self.direct[key]
                if n < len(self.records):
                    self.current = n
                    return self.records[n]
        return None

    def next(self):
        """Return next record."""
        if self.records is None:
            return None
        if self.current is None:
            return self.first()
        elif self.current == len(self.records) - 1:
            return None
        else:
            self.current += 1
        return self.records[self.current]

    def prev(self):
        """Return previous record."""
        if self.records is None:
            return None
        if self.current is None:
            return self.last()
        elif self.current == 0:
            return None
        else:
            self.current -= 1
        return self.records[self.current]

    def setat(self, record):
        """Return record after positioning cursor at record."""
        if self.records is not None:
            k, v = record
            if k in self.direct:
                n = self.direct[k]
                if n < len(self.records):
                    self.current = n
                    return self.records[n]
        return None

    def get_partial(self):
        """Return self._partial"""
        return self._partial

