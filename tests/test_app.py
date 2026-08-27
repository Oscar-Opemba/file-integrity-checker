import hashlib
import tempfile
import unittest
from pathlib import Path
from app import analyze

class TestIntegrity(unittest.TestCase):
    def test_hash_and_verify(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sample.txt'; path.write_text('hello', encoding='utf-8')
            digest = hashlib.sha256(b'hello').hexdigest()
            result = analyze({'path':str(path), 'expected':digest})
            self.assertTrue(result['matches_expected'])

if __name__ == '__main__': unittest.main()
