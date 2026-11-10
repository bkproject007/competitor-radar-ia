import unittest
from src.monitor import normalize_html, fingerprint

class MonitorTests(unittest.TestCase):
    def test_extract_text(self):
        self.assertEqual(normalize_html('<h1>Hello</h1><script>bad()</script><p>World</p>'),'Hello World')
    def test_fingerprint_is_stable(self):
        self.assertEqual(fingerprint('a'),fingerprint('a'))
        self.assertNotEqual(fingerprint('a'),fingerprint('b'))

if __name__=='__main__': unittest.main()
