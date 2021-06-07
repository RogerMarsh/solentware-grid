# testdataclient.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Test classes for linking a GUI Control with a database."""


if __name__=='__main__':

    import basesup.api.database

    from gridsup.core.dataclient import DataClient, DataSource
    
    d = basesup.api.database.Database()
    c = DataClient()
    print d
    print c
    s = DataSource(d, '', '')
    c.set_data_source(s)
    print s
