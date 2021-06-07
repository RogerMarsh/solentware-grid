# dptdatasource.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides the DPTDataSource class using the dptdb package to
access a DPT database.

"""

from dptdb import dptapi

from ..core.dataclient import DataSource


class DPTDataSource(DataSource):
    
    """Provide bsddb3 style cursor access to recordset of arbitrary records.
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Delegate to superclass then set the recordset attribute to None,
        indicating this datasource is not associated with a recordset.

        """
        super(DPTDataSource, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.recordset = None
        self._fieldvalue = dptapi.APIFieldValue()
        self.dbhome.database_definition[self.dbset]._sources[self] = None
        
    def close(self):
        """Destroy the APIRecordSet created by DPT to implement recordset."""
        if self.recordset is not None:
            try:
                del self.dbhome.database_definition[self.dbset]._sources[self]
            except:
                pass
            self.dbhome.database_definition[self.dbset].get_database(
                ).DestroyRecordSet(self.recordset)
            self.recordset = None

    def get_cursor(self):
        """Create and return cursor on this datasource's recordset."""
        if self.recordset:
            c = self.dbhome.create_recordset_cursor(
                self.dbset, self.dbname, self.recordset)
        else:
            c = self.dbhome.create_recordset_cursor(
                self.dbset,
                self.dbname,
                self.dbhome.get_database(self.dbset, self.dbname
                                         ).CreateRecordList())
        if c:
            self.dbhome.database_definition[self.dbset]._clientcursors[c] = True
        return c

    def join_field_occurrences(self, record, field):
        """Return concatenated occurrences of field.

        The record value, a repr(<python object>), is held as multiple
        occurrences of a field in a record on a DPT file.  Each occurrence is
        a maximum of 256 bytes (in Python terminology) so a Python object is
        split into multiple occurrences of a field for storage.
        """
        i = 1
        v = []
        while record.GetFieldValue(field, self._fieldvalue, i):
            v.append(self._fieldvalue.ExtractString())
            i += 1
        return ''.join(v)

    def set_recordset(self, records):
        """Set recordset as this datasource's recordset if the recordset and
        this datasource are associated with the same database identity."""
        if self.recordset:
            self.dbhome.get_database(
                self.dbset, self.dbname).DestroyRecordSet(self.recordset)
        self.recordset = records
