# test_callbackexception.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""callbackexception tests"""

import unittest

from .. import callbackexception


class CallbackException(unittest.TestCase):
    def setUp(self):
        self.callbackexception = callbackexception.CallbackException()

        def m():
            pass

        self.m = m

    def tearDown(self):
        pass

    def test_001_report_exception_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "report_exception\(\) takes from 1 to 4 positional ",
                    "arguments but 5 were given",
                )
            ),
            self.callbackexception.report_exception,
            *(None, None, None, None),
        )

    def test_001_report_exception_002(self):
        try:
            x
        except:
            self.assertRaisesRegex(
                NameError,
                "name 'x' is not defined",
                self.callbackexception.report_exception,
            )

    def test_002_try_command_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "try_command\(\) missing 2 required positional ",
                    "arguments: 'method' and 'widget'",
                )
            ),
            self.callbackexception.try_command,
        )

    def test_002_try_command_002(self):
        self.assertEqual(
            self.callbackexception.try_command(self.m, "w") is self.m, True
        )

    def test_003_try_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "try_event\(\) missing 1 required positional ",
                    "argument: 'method'",
                )
            ),
            self.callbackexception.try_event,
        )

    def test_003_try_command_002(self):
        self.assertEqual(
            self.callbackexception.try_event(self.m) is self.m, True
        )

    def test_004_try_thread_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "try_thread\(\) missing 2 required positional ",
                    "arguments: 'method' and 'widget'",
                )
            ),
            self.callbackexception.try_thread,
        )

    def test_004_try_thread_002(self):
        self.assertEqual(
            self.callbackexception.try_thread(self.m, "w") is self.m, True
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(CallbackException))
