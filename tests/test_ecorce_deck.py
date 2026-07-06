from pathlib import Path
import unittest

from tools.ecorce_deck import parse_device, parse_stimulus, validate_pair


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'models' / 'ecorce' / 'lateral-gan-hemt'


class EcorceDeckTests(unittest.TestCase):
    def test_device_metadata(self) -> None:
        device = parse_device(MODEL / 'device.dev')
        self.assertEqual(device['format_version'], '2.22')
        self.assertEqual(device['dimension'], 'dim_2')
        self.assertEqual(
            {contact['name'] for contact in device['contacts']},
            {'Source', 'Gate', 'Drain', 'Substrate'},
        )
        self.assertEqual(
            {material['material'] for material in device['materials']},
            {'AlGaN', 'GaN', 'Si'},
        )
        self.assertTrue(device['enabled_physics']['poisson'])
        self.assertFalse(device['enabled_physics']['ionisation_impact'])

    def test_transfer_stimulus(self) -> None:
        stimulus = parse_stimulus(MODEL / 'transfer_gate_0_to_5V.sti')
        self.assertEqual(stimulus['format_version'], '2.22')
        self.assertEqual(stimulus['temperature'], '300 K')
        gate = next(item for item in stimulus['biases'] if item['contact'] == 'Gate')
        self.assertEqual(gate['start'], '0 V')
        self.assertEqual(gate['end'], '5 V')
        self.assertEqual(gate['increment'], '0.1 V')

    def test_device_stimulus_references_match(self) -> None:
        errors = validate_pair(
            MODEL / 'device.dev',
            MODEL / 'transfer_gate_0_to_5V.sti',
        )
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
