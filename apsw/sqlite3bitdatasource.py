# sqlite3bitdatasource.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

# Build this module like dptdatasource.py
# See use of CreateRecordList and DestroyRecordSet methods, whose analogues
# will be sibling methods of 'self.dbhome.get_database(...)'
# It is possible this will become datasource class for recordsets and that
# sqlite3datasource.py will become similar for sorted recordsets.
"""Emulate DPT record sets and provide bsddb style access.

Typical use is:
Build a dictionary representing a record set.  Call set_recordset(<dictionary>)
to give the cursor a sorted record set.  The DBDataSource instance links the
sorted record set to a grid control (GUI) to display the records in a
scrollable list.

List of classes

Sqlite3bitDataSource
CursorRS

"""

from basesup.api.database import Cursor, Recordset
from basesup.api.constants import (
    DB_SEGMENT_SIZE,
    SQLITE_VALUE_COLUMN,
    )

from ..core.dataclient import DataSource


class Sqlite3bitDataSource(DataSource):
    
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
        super(Sqlite3bitDataSource, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.recordset = None
        # Not sure if equivalent of this (from dptdatasource) is needed
        #self.dbhome.get_dptfiles()[self.dbset]._sources[self] = None
        # which would imply that the close() method be transplanted as well.
        
    def get_cursor(self):
        """Return cursor on the record set associated with datasource."""
        if self.recordset:
            if self.dbidentity == self.recordset.dbidentity:
                c = CursorRS(recordset=self.recordset)
            else:
                raise DBapiError(
                    'Recordset and DataSource are for different databases')
        else:
            self.recordset = Recordset(self.dbhome, self.dbset)
            c = CursorRS(recordset=self.recordset)
        if c:
            self.recordset._clientcursors[c] = True
        return c

    def set_recordset(self, recordset):
        """Set self.recordset to sorted records (a dictionary)."""
        if self.recordset:
            if self.recordset.dbidentity == recordset.dbidentity:
                self.recordset.close()
                self.recordset = recordset
            else:
                raise DBapiError(
                    'New and existing Recordsets are for different databases')
        elif self.dbidentity == recordset.dbidentity:
            self.recordset = recordset
        else:
            raise DBapiError(
                'New Recordset and DataSource are for different databases')


# This class uses a CursorDB to get the record associated with a recordset item.
# Maybe the superclass should be DBRecordset
# (and put the <key, value> getter as an attribute of that class)
# <key, value>s are unique so DB methods can do the job.
class CursorRS(Cursor):
    
    """A Cursor cursor that does not implement partial keys.
    
    If a subset of the records on self.recordset is needed do more selection
    to get the subset and pass this to the cursor.

    Methods added:

    _get_record

    Methods overridden:

    close
    count_records
    database_cursor_exists
    first
    get_partial
    get_position_of_record
    get_record_at_position
    last
    nearest
    next
    prev
    setat
    set_partial_key

    Methods extended:

    __init__

    Properties:

    recordset
    
    """

    def __init__(self, recordset):
        """Define a cursor to access recordset in the order given in keymap."""
        super(CursorRS, self).__init__(recordset)#.dbset)

    @property
    def recordset(self):
        """"""
        return self._dbset

    def close(self):
        """Delete record set cursor"""
        try:
            del self._dbset._clientcursors[self]
        except:
            pass
        self._dbset = None

    def count_records(self):
        """return record count or None"""
        try:
            return self._dbset.count_records()
        except TypeError:
            return None
        except AttributeError:
            return None

    def database_cursor_exists(self):
        """Return True if self.records is not None and False otherwise

        Simulates existence test for a database cursor.

        """
        # The cursor methods are defined in this class and operate on
        # self.records if it is a list so do that test here as well.
        return self._dbset is not None

    def first(self):
        """Return first record."""
        if len(self._dbset):
            try:
                #return self._dbset.get_record(self._dbset.first()[1])
                return self._get_record(self._dbset.first()[1])
            except TypeError:
                return None
            except:
                raise

    def get_position_of_record(self, record=None):
        """return position of record in file or 0 (zero)"""
        try:
            return self._dbset.get_position_of_record_number(record[0])
        except ValueError:
            return 0
        except TypeError:
            return 0

    def get_record_at_position(self, position=None):
        """return record for positionth record in file or None"""
        try:
            if position < 0:
                position = self._dbset.count_records() + position
            return self._get_record(
                self._dbset.get_record_number_at_position(position))
        except IndexError:
            return None
        except TypeError:
            if position is None:
                return None
            raise

    def last(self):
        """Return last record."""
        if len(self._dbset):
            try:
                return self._get_record(self._dbset.last()[1])
            except TypeError:
                return None
            except:
                raise

    def set_partial_key(self, partial):
        """Set partial key to None.  Always.
        
        Always set to None because the recordset oand keymap should be trimmed
        to the required records before passing to the cursor.
        
        """
        self._partial = None
        
    def nearest(self, key):
        """Return nearest record. An absent record has no nearest record.

        Perhaps get_record_at_position() is the method to use.
        
        The recordset is created with arbitrary criteria.  The selected records
        are displayed in record number order for consistency.  Assumption is
        that all records on the recordset are equally near the requested record
        if it is not in the recordset itself, so whatever is already displayed
        is as near as any other records that might be chosen.

        """
        if len(self._dbset):
            try:
                return self._get_record(self._dbset.setat(key)[1])
            except TypeError:
                return None
            except:
                raise

    def next(self):
        """Return next record."""
        if len(self._dbset):
            try:
                return self._get_record(self._dbset.next()[1])
            except TypeError:
                return None
            except:
                raise

    def prev(self):
        """Return previous record."""
        if len(self._dbset):
            try:
                return self._get_record(self._dbset.prev()[1])
            except TypeError:
                return None
            except:
                raise

    def setat(self, record):
        """Return record after positioning cursor at record."""
        if len(self._dbset):
            try:
                return self._get_record(
                    self._dbset.setat(record[0])[1])
            except TypeError:
                return None
            except:
                raise

    def get_partial(self):
        """Return self._partial"""
        return self._partial

    # Hack to get round self._dbset._database being a Sqlite.Cursor which means
    # the Recordset.get_record method does not work here because it does:
    # record = self._database.get(record_number)
    # All self._dbset.get_record(..) calls replaced by self._get_record(..) in
    # this module (hope no external use for now).
    # Maybe Recordset should not have a get_record method.
    def _get_record(self, record_number, use_cache=False):
        """Return record_number from database using cache if requested"""
        dbset = self._dbset
        primary = dbset._dbhome._sqtables[
            dbset._dbhome._associate[dbset._dbset][dbset._dbset]]._fd_name
        if use_cache:
            record = dbset.record_cache.get(record_number)
            if record is not None:
                return record # maybe (record_number, record)
        segment, recnum = divmod(record_number, DB_SEGMENT_SIZE)
        if segment not in dbset._rs_segments:
            return # maybe raise
        if recnum not in dbset._rs_segments[segment]:
            return # maybe raise
        statement = ' '.join((
            'select',
            SQLITE_VALUE_COLUMN,
            'from',
            primary,
            'where',
            primary, '== ?',
            'limit 1',
            ))
        values = (record_number,)
        record = dbset._database.cursor(
            ).execute(statement, values).fetchone()[0]
        # maybe raise if record is None (if not, None should go on cache)
        if use_cache:
            dbset.record_cache[record_number] = record
            dbset.record.deque.append(record_number)
        return (record_number, record)

