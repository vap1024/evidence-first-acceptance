"""Validate acceptance-map completeness; never execute recorded commands."""
import argparse
from datetime import date
from pathlib import Path

HEADERS = {
    'CLAIMS': ['Claim', 'Assertion', 'Author', 'Run', 'Claimed evidence'],
    'EVIDENCE': ['Evidence', 'Claim', 'Run', 'Source', 'Command', 'Result'],
    'ACCEPTANCE': ['Claim', 'Run', 'Evidence', 'Status', 'Counterexample or reason', 'Reviewer', 'Date'],
}
STATUSES = {'accepted', 'rejected', 'partial', 'not verified'}


def filled(value):
    return value.strip().lower() not in {'', '-', '—', 'tbd', 'todo', 'n/a', 'none', 'unknown'}


def read_table(path, columns, errors):
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f'{path.name}: cannot read: {exc}')
        return []
    table = [(n, [c.strip() for c in line.strip()[1:-1].split('|')])
             for n, line in enumerate(lines, 1)
             if line.strip().startswith('|') and line.strip().endswith('|')]
    if len(table) < 2 or table[0][1] != columns:
        errors.append(f'{path.name}: missing or invalid table header')
        return []
    separator = table[1][1]
    if len(separator) != len(columns) or any(len(c.strip(':')) < 3 or set(c.strip(':')) != {'-'} for c in separator):
        errors.append(f'{path.name}: invalid table separator')
    rows = []
    for n, cells in table[2:]:
        if len(cells) != len(columns):
            errors.append(f'{path.name}:{n}: expected {len(columns)} cells, got {len(cells)}')
        else:
            rows.append(dict(zip(columns, cells)))
    if not rows:
        errors.append(f'{path.name}: no records')
    return rows


def validate(folder):
    # Recorded commands are opaque text: validation never runs them.
    folder = Path(folder)
    errors = []
    tables = {name: read_table(folder / f'{name}.md', cols, errors) for name, cols in HEADERS.items()}
    for name in ('CORRECTIONS', 'POLICY-DECISIONS'):
        try:
            if not (folder / f'{name}.md').read_text(encoding='utf-8').strip():
                errors.append(f'{name}.md: empty file')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{name}.md: cannot read: {exc}')
    claims, evidence = {}, {}
    for row in tables['CLAIMS']:
        key = (row['Claim'], row['Run'])
        label = f'CLAIMS {key}'
        for field in HEADERS['CLAIMS']:
            if not filled(row[field]):
                errors.append(f'{label}: missing {field}')
        if key in claims:
            errors.append(f'{label}: duplicate claim/run')
        claims[key] = row
    for row in tables['EVIDENCE']:
        eid = row['Evidence']
        if not filled(eid):
            errors.append('EVIDENCE: missing Evidence ID')
        if eid in evidence:
            errors.append(f'EVIDENCE {eid}: duplicate ID')
        evidence[eid] = row
        if (row['Claim'], row['Run']) not in claims:
            errors.append(f'EVIDENCE {eid}: unknown claim/run')
    for key, row in claims.items():
        linked = evidence.get(row['Claimed evidence'])
        if linked is None or (linked['Claim'], linked['Run']) != key:
            errors.append(f'CLAIMS {key}: claimed evidence missing or mismatched')
    seen = set()
    for row in tables['ACCEPTANCE']:
        key = (row['Claim'], row['Run'])
        label = f'ACCEPTANCE {key}'
        if key in seen:
            errors.append(f'{label}: duplicate verdict')
        seen.add(key)
        claim = claims.get(key)
        if claim is None:
            errors.append(f'{label}: unknown claim/run')
        status = row['Status']
        if status not in STATUSES:
            errors.append(f'{label}: invalid status {status!r}')
        if not filled(row['Reviewer']):
            errors.append(f'{label}: missing Reviewer')
        elif claim and row['Reviewer'].casefold() == claim['Author'].casefold():
            errors.append(f'{label}: reviewer must differ from author')
        try:
            parsed = date.fromisoformat(row['Date'])
            if parsed.isoformat() != row['Date']:
                raise ValueError
        except ValueError:
            errors.append(f'{label}: Date must be YYYY-MM-DD')
        linked = evidence.get(row['Evidence'])
        if filled(row['Evidence']) and (linked is None or (linked['Claim'], linked['Run']) != key):
            errors.append(f'{label}: evidence missing or mismatched')
        if status == 'accepted':
            if not filled(row['Run']):
                errors.append(f'{label}: accepted requires Run')
            if linked is None:
                errors.append(f'{label}: accepted requires Evidence')
            else:
                for field in ('Source', 'Command', 'Result'):
                    if not filled(linked[field]):
                        errors.append(f'{label}: accepted evidence missing {field}')
        if status in {'rejected', 'partial', 'not verified'} and not filled(row['Counterexample or reason']):
            errors.append(f'{label}: {status} requires counterexample or reason')
    for key in sorted(claims.keys() - seen):
        errors.append(f'CLAIMS {key}: missing acceptance verdict')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case_folder', type=Path)
    args = parser.parse_args()
    errors = validate(args.case_folder)
    if errors:
        print('FAIL: acceptance map is incomplete')
        for error in errors:
            print(f'- {error}')
        return 1
    print('PASS: map is structurally complete (not a truth or acceptance check)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
