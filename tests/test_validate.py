import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.case = Path(self.temp.name) / 'case'
        shutil.copytree(ROOT / 'examples/a-notification', self.case)

    def replace(self, file, old, new):
        path = self.case / file
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding='utf-8')

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / 'validate.py'), *map(str, args)],
            capture_output=True, text=True,
        )

    def test_examples(self):
        for case in sorted((ROOT / 'examples').iterdir()):
            with self.subTest(case=case.name):
                result = self.run_cli(case)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('PASS:', result.stdout)

    def test_required_accepted_fields(self):
        for old, field in [('probe.py: fixed_delivery and retry check', 'Source'),
                           ('python3 probe.py v2', 'Command'),
                           ('retry counterexample closed; retryable=True; exit 0', 'Result')]:
            with self.subTest(field=field):
                path = self.case / 'EVIDENCE.md'
                original = path.read_text()
                self.replace('EVIDENCE.md', old, '')
                result = self.run_cli(self.case)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f'accepted evidence missing {field}', result.stdout)
                path.write_text(original)

    def test_missing_run(self):
        for name in ('CLAIMS', 'EVIDENCE', 'ACCEPTANCE'):
            self.replace(name + '.md', '| v2 |', '|  |')
        self.assertTrue(any('requires Run' in e for e in validate(self.case)))

    def test_missing_evidence(self):
        self.replace('ACCEPTANCE.md', '| v2 | E2 |', '| v2 | absent |')
        self.assertTrue(any('requires Evidence' in e for e in validate(self.case)))

    def test_mismatched_evidence(self):
        self.replace('ACCEPTANCE.md', '| v2 | E2 |', '| v2 | E1 |')
        self.assertTrue(any('mismatched' in e for e in validate(self.case)))

    def test_refusal_requires_reason(self):
        for status in ('rejected', 'partial'):
            with self.subTest(status=status):
                p = self.case / 'ACCEPTANCE.md'
                original = p.read_text()
                lines = original.splitlines()
                for i, line in enumerate(lines):
                    if '| rejected |' in line:
                        cells = line.split('|')
                        cells[4], cells[5] = f' {status} ', ' '
                        lines[i] = '|'.join(cells)
                p.write_text('\n'.join(lines))
                self.assertTrue(any(f'{status} requires' in e for e in validate(self.case)))
                p.write_text(original)

    def test_self_review(self):
        self.replace('ACCEPTANCE.md', 'Synthetic reviewer Birch', 'Synthetic implementer Cedar')
        self.assertTrue(any('differ from author' in e for e in validate(self.case)))

    def test_invalid_status(self):
        self.replace('ACCEPTANCE.md', '| accepted |', '| green |')
        self.assertTrue(any('invalid status' in e for e in validate(self.case)))

    def test_missing_verdict(self):
        p = self.case / 'ACCEPTANCE.md'
        p.write_text('\n'.join(line for line in p.read_text().splitlines() if '| v2 |' not in line))
        self.assertTrue(any('missing acceptance verdict' in e for e in validate(self.case)))

    def test_duplicate_evidence(self):
        p = self.case / 'EVIDENCE.md'
        text = p.read_text()
        row = next(line for line in text.splitlines() if line.startswith('| E2 |'))
        p.write_text(text + row + '\n')
        self.assertTrue(any('duplicate ID' in e for e in validate(self.case)))

    def test_missing_file_and_cli_failure(self):
        (self.case / 'EVIDENCE.md').unlink()
        result = subprocess.run([sys.executable, str(ROOT / 'validate.py'), str(self.case)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('EVIDENCE.md: cannot read', result.stdout)
        self.assertIn('accepted requires Evidence', result.stdout)

    def test_cli_success(self):
        result = subprocess.run([sys.executable, str(ROOT / 'validate.py'), str(self.case)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('structurally complete', result.stdout)

    def test_malformed_table(self):
        self.replace('EVIDENCE.md', '| E2 | N1 |', '| E2 | EXTRA | N1 |')
        self.assertTrue(any('expected 6 cells' in e for e in validate(self.case)))

    def test_invalid_table_separator(self):
        self.replace('EVIDENCE.md', '| --- | --- | --- | --- | --- | --- |', '| -- | --- | --- | --- | --- | --- |')
        self.assertTrue(any('invalid table separator' in e for e in validate(self.case)))

    def test_evidence_unknown_claim_run(self):
        self.replace('EVIDENCE.md', '| E2 | N1 | v2 |', '| E2 | absent | v2 |')
        self.assertTrue(any('unknown claim/run' in e for e in validate(self.case)))

    def test_not_verified(self):
        self.replace('ACCEPTANCE.md', '| accepted |', '| not verified |')
        self.assertEqual(validate(self.case), [])

    def test_commands_are_never_executed(self):
        marker = self.case / 'executed.txt'
        command = f'{sys.executable} -c "from pathlib import Path; Path({str(marker)!r}).touch()"'
        self.replace('EVIDENCE.md', 'python3 probe.py v2', command)
        result = self.run_cli(self.case)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(marker.exists())

    def test_cli_usage_errors(self):
        for args in ((), ('--unknown-option',), (self.case, 'extra')):
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertIn('usage:', result.stderr)

    def test_dates(self):
        path = self.case / 'ACCEPTANCE.md'
        original = path.read_text(encoding='utf-8')
        for value in ('', '2026-02-30', '13.11.2026', '20260115'):
            with self.subTest(value=value):
                path.write_text(original.replace('2026-01-15', value), encoding='utf-8')
                self.assertTrue(any('Date must be YYYY-MM-DD' in e for e in validate(self.case)))

    def test_duplicate_claim_and_verdict(self):
        for name, message in (('CLAIMS', 'duplicate claim/run'), ('ACCEPTANCE', 'duplicate verdict')):
            with self.subTest(name=name):
                path = self.case / f'{name}.md'
                original = path.read_text(encoding='utf-8')
                row = next(line for line in original.splitlines() if '| v2 |' in line)
                path.write_text(original + row + '\n', encoding='utf-8')
                self.assertTrue(any(message in e for e in validate(self.case)))
                path.write_text(original, encoding='utf-8')

    def test_all_five_files_required(self):
        for name in ('CLAIMS', 'EVIDENCE', 'ACCEPTANCE', 'CORRECTIONS', 'POLICY-DECISIONS'):
            with self.subTest(name=name):
                path = self.case / f'{name}.md'
                original = path.read_bytes()
                path.unlink()
                result = self.run_cli(self.case)
                self.assertEqual(result.returncode, 1)
                self.assertIn(f'{name}.md: cannot read', result.stdout)
                path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
