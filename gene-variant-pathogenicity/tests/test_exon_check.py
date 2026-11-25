"""exon_check.py regression tests (offline fixtures, no network)."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from exon_check import check

FIX = json.loads((ROOT / 'tests/fixtures/exon-check-jag1.json').read_text(encoding='utf-8'))


class Jag1RegressionTests(unittest.TestCase):
    def test_jag1_exon2_is_306_nt(self):
        card = check('NM_000214.3', 2, genbank_text=FIX['genbank'], ensembl_data=FIX['ensembl'])
        self.assertEqual(card['status'], 'PASS')
        self.assertEqual(card['ncbi']['length'], 306)
        self.assertEqual(card['ncbi']['c_start'], 82)
        self.assertEqual(card['ncbi']['c_end'], 387)
        self.assertEqual(card['ncbi']['mod3'], 0)
        self.assertEqual(card['ncbi']['phase'], 0)
        self.assertEqual(card['ncbi']['aa_start'], 28)
        self.assertEqual(card['ncbi']['aa_end'], 129)
        self.assertEqual(card['ensembl']['length'], 306)
        self.assertIn('in-frame', card['ncbi']['frame'])

    def test_off_by_one_is_mismatch(self):
        ens = copy.deepcopy(FIX['ensembl'])
        for transcript in ens['Transcript']:
            if transcript.get('id') != 'ENST00000254958':
                continue
            for exon in transcript['Exon']:
                if int(exon['start']) == 10672701:
                    exon['end'] = int(exon['end']) + 1
                    break
        card = check('NM_000214.3', 2, genbank_text=FIX['genbank'], ensembl_data=ens)
        self.assertEqual(card['status'], 'MISMATCH')
        self.assertFalse(card['cross_check']['passed'])
        messages = ' '.join(card['cross_check']['messages'])
        self.assertIn('306', messages)
        self.assertIn('307', messages)


GENBANK = '''LOCUS       NM_TEST.1                 300 bp    mRNA    linear   PRI 01-JAN-2026
VERSION     NM_TEST.1
FEATURES             Location/Qualifiers
     source          1..300
     gene            1..300
                     /gene="TESTG"
     exon            1..51
     exon            52..151
     exon            152..300
     CDS             1..300
ORIGIN
//
'''

ENSEMBL = {'Transcript': [{
    'id': 'ENSTTEST', 'strand': 1, 'is_canonical': 1,
    'Translation': {'length': 100},
    'Exon': [
        {'start': 1001, 'end': 1051},
        {'start': 2001, 'end': 2100},
        {'start': 3001, 'end': 3149},
    ],
}]}


class SyntheticTests(unittest.TestCase):
    def test_synthetic_pass_and_frame(self):
        card = check('NM_TEST.1', 2, genbank_text=GENBANK, ensembl_data=ENSEMBL)
        self.assertEqual(card['status'], 'PASS')
        self.assertEqual(card['ncbi']['length'], 100)
        self.assertEqual(card['ncbi']['c_start'], 52)
        self.assertEqual(card['ncbi']['phase'], 0)
        self.assertEqual(card['ncbi']['mod3'], 1)
        self.assertIn('shifts the reading frame', card['ncbi']['frame'])

    def test_synthetic_mismatch(self):
        ens = copy.deepcopy(ENSEMBL)
        ens['Transcript'][0]['Exon'][1]['end'] += 1
        card = check('NM_TEST.1', 2, genbank_text=GENBANK, ensembl_data=ens)
        self.assertEqual(card['status'], 'MISMATCH')


if __name__ == '__main__':
    unittest.main()
