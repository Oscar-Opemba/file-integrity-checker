import tempfile
import unittest
from pathlib import Path
from app import analyze

class TestIntegrityEdgeCases(unittest.TestCase):
    def test_rejects_malformed_expected_digest(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sample'; path.write_text('data', encoding='utf-8')
            result = analyze({'path':str(path), 'expected':'not-a-digest'})
            self.assertIn('error', result)

if __name__ == '__main__': unittest.main()
