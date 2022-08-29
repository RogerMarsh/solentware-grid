# test_dataregister.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dataregister tests"""

import unittest

from .. import dataregister


class DataRegister(unittest.TestCase):
    def setUp(self):
        class Datasource:
            def __init__(self):
                self.dbhome = "dbhome"
                self.dbset = "dbset"
                self.dbname = "dbname"

        class Client:
            datasource = Datasource()

            def load_new_index(self):
                pass

            def callback(*a):
                pass

        self.Client = Client
        self.client = self.Client()
        self.dataregister = dataregister.DataRegister()
        cds = self.client.datasource
        self.key = (cds.dbhome, cds.dbset, cds.dbname)
        self.datasources = {}
        self.datasources[self.key] = {self.client: self.client.callback}

    def tearDown(self):
        pass

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            dataregister.DataRegister,
            *(None,),
        )

    def test_002_refresh_at_start_of_file_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"refresh_at_start_of_file\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.dataregister.refresh_at_start_of_file,
            *(None,),
        )

    def test_002_refresh_at_start_of_file_002(self):
        self.dataregister.datasources["key"] = [self.Client()]
        self.assertEqual(self.dataregister.refresh_at_start_of_file(), None)

    def test_002_refresh_at_start_of_file_003(self):
        self.assertEqual(self.dataregister.datasources, {})
        self.assertEqual(self.dataregister.refresh_at_start_of_file(), None)

    def test_003_refresh_after_update_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"refresh_after_update\(\) missing 2 required positional ",
                    "arguments: 'dskey' and 'instance'",
                )
            ),
            self.dataregister.refresh_after_update,
        )

    def test_003_refresh_after_update_002(self):
        self.dataregister.datasources = self.datasources
        self.assertEqual(
            self.dataregister.refresh_after_update(self.key, None), None
        )

    def test_003_refresh_after_update_003(self):
        self.dataregister.datasources = self.datasources
        self.assertEqual(
            self.dataregister.refresh_after_update(None, None), None
        )

    def test_004_register_in_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"register_in\(\) missing 2 required positional ",
                    "arguments: 'client' and 'callback'",
                )
            ),
            self.dataregister.register_in,
        )

    def test_004_register_in_002(self):
        self.assertEqual(self.dataregister.datasources, {})
        self.assertEqual(
            self.dataregister.register_in(self.client, self.client.callback),
            None,
        )
        self.assertEqual(
            self.dataregister.datasources[self.key][self.client],
            self.client.callback,
        )

    def test_005_register_out_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"register_out\(\) missing 1 required positional ",
                    "argument: 'client'",
                )
            ),
            self.dataregister.register_out,
        )

    def test_005_register_in_002(self):
        self.dataregister.datasources = {None: None}
        self.assertEqual(self.dataregister.register_out(None), None)
        self.assertEqual(self.dataregister.datasources, {})

    def test_005_register_in_003(self):
        self.dataregister.datasources = self.datasources
        self.assertEqual(self.dataregister.register_out(self.client), None)
        self.assertEqual(self.dataregister.datasources, {})


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DataRegister))
