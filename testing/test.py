from unittest import TestCase

class Test(TestCase):
    def testAlwaysPasse(self):
        self.assertTrue(True)

    def testAlwaysFails(self):
        self.assertTrue(False)