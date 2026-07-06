"""Small, dependency-free utilities for inspecting legacy Ecorce decks.

This module does not execute semiconductor simulations. It extracts enough
metadata from .dev and .sti text files to audit a repository before opening
the model in the Ecorce GUI.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re
from typing import Iterable


VALUE_PATTERN = re.compile(r'(?P<key>[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*)\s*=\s*(?P<value>[^;]+);')


@dataclass(frozen=True)
class Contact:
    name: str
    contact_type: str
    address: str | None


@dataclass(frozen=True)
class Material:
    name: str
    material: str
    parameter_file: str
    band_gap: str | None
    permittivity: str | None


@dataclass(frozen=True)
class Bias:
    contact: str
    bias_type: str
    constant: str | None = None
    start: str | None = None
    end: str | None = None
    increment: str | None = None


def _read(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8', errors='replace')


def _first(text: str, key: str) -> str | None:
    match = re.search(rf'\b{re.escape(key)}\s*=\s*"?([^;"\n]+)"?\s*;', text)
    return match.group(1).strip() if match else None


def _blocks(text: str, block_name: str) -> list[str]:
    """Return balanced-brace blocks named *block_name*."""
    found: list[str] = []
    pattern = re.compile(rf'\b{re.escape(block_name)}\s*\{{')
    for match in pattern.finditer(text):
        index = match.end()
        depth = 1
        while index < len(text) and depth:
            if text[index] == '{':
                depth += 1
            elif text[index] == '}':
                depth -= 1
            index += 1
        if depth == 0:
            found.append(text[match.start():index])
    return found


def _quoted(block: str, key: str) -> str | None:
    match = re.search(rf'\b{re.escape(key)}\s*=\s*"([^"]*)"\s*;', block)
    return match.group(1).strip() if match else None


def parse_device(path: str | Path) -> dict:
    path = Path(path)
    text = _read(path)

    contacts: list[Contact] = []
    for block in _blocks(text, 'Reference'):
        name = _quoted(block, 'nom')
        if not name:
            continue
        contacts.append(Contact(
            name=name,
            contact_type=_first(block, 'type') or 'unknown',
            address=_first(block, 'adresse'),
        ))

    materials: list[Material] = []
    for block in _blocks(text, 'Sous_domaine'):
        name = _quoted(block, 'nom')
        if not name:
            continue
        materials.append(Material(
            name=name,
            material=_quoted(block, 'nom_materiau') or 'unknown',
            parameter_file=_quoted(block, 'nom_fichier') or 'unknown',
            band_gap=_first(block, 'gap'),
            permittivity=_first(block, 'epsilon'),
        ))

    enabled_physics = {}
    for key in (
        'poisson', 'transport_n', 'transport_p', 'piegeage_n', 'piegeage_p',
        'band_to_band_tunneling', 'ionisation_impact',
        'recombinaison_schockley_read_hall', 'recombinaison_auger',
        'mobilite_fonction_champ_electrique_parallele',
    ):
        value = _first(text, key)
        if value is not None:
            enabled_physics[key] = value.lower() == 'true'

    xs = [float(v) for v in re.findall(r'\bx\s*=\s*([-+0-9.eE]+)\s*(?:μm|um)', text)]
    ys = [float(v) for v in re.findall(r'\by\s*=\s*([-+0-9.eE]+)\s*(?:μm|um)', text)]

    return {
        'path': str(path),
        'format_version': _first(text, 'version'),
        'created': _first(text, 'date_creation'),
        'modified': _first(text, 'date_modification'),
        'dimension': _first(text, 'dimension'),
        'discretisation': _first(text, 'methode_discretisation'),
        'enabled_physics': enabled_physics,
        'contacts': [asdict(item) for item in contacts],
        'materials': [asdict(item) for item in materials],
        'geometry': {
            'nodes': len(_blocks(text, 'Node')),
            'lines': len(_blocks(text, 'Line')),
            'surfaces': len(_blocks(text, 'Surface')),
            'x_range_um': [min(xs), max(xs)] if xs else None,
            'y_range_um': [min(ys), max(ys)] if ys else None,
        },
    }


def parse_stimulus(path: str | Path) -> dict:
    path = Path(path)
    text = _read(path)
    biases: list[Bias] = []
    for block in _blocks(text, 'Bias'):
        contact = _first(block, 'nom_reference')
        if not contact:
            continue
        biases.append(Bias(
            contact=contact,
            bias_type=_first(block, 'type') or 'unknown',
            constant=_first(block, 'constant_value'),
            start=_first(block, 'start_value'),
            end=_first(block, 'end_value'),
            increment=_first(block, 'increment'),
        ))

    temperature = None
    temperature_blocks = _blocks(text, 'Temperature')
    if temperature_blocks:
        temperature = _first(temperature_blocks[0], 'constant_value')

    return {
        'path': str(path),
        'format_version': _first(text, 'version'),
        'created': _first(text, 'date_creation'),
        'modified': _first(text, 'date_modification'),
        'analysis': _first(text, 'analysis') or _first(text, 'analyse'),
        'temperature': temperature,
        'biases': [asdict(item) for item in biases],
        'mesh': {
            'max_nodes': _first(text, 'nombre_maximum_noeud'),
            'minimum_edge': _first(text, 'longueur_minimum_arete'),
            'spatial_precision': _first(text, 'precision_espace'),
        },
        'solver': {
            'newton_max_iterations': _first(text, 'nombre_iteration_maximum_newton'),
            'gmres_max_iterations': _first(text, 'nombre_iteration_maximum_gmres'),
            'linear_tolerance': _first(text, 'precision_resolution_systeme_lineaire'),
            'equation_tolerance': _first(text, 'precision_resolution_equation'),
        },
    }


def validate_pair(device_path: str | Path, stimulus_path: str | Path) -> list[str]:
    device = parse_device(device_path)
    stimulus = parse_stimulus(stimulus_path)
    errors: list[str] = []

    if device['format_version'] != stimulus['format_version']:
        errors.append(
            f"Version mismatch: device={device['format_version']} stimulus={stimulus['format_version']}"
        )

    contacts = {item['name'] for item in device['contacts']}
    for bias in stimulus['biases']:
        if bias['contact'] not in contacts:
            errors.append(f"Stimulus references unknown contact: {bias['contact']}")

    if not device['contacts']:
        errors.append('No contacts found in device deck.')
    if not device['materials']:
        errors.append('No materials found in device deck.')
    if not stimulus['biases']:
        errors.append('No bias definitions found in stimulus deck.')

    return errors


def inspect_directory(directory: str | Path) -> dict:
    directory = Path(directory)
    devices = sorted(directory.glob('*.dev'))
    stimuli = sorted(directory.glob('*.sti'))
    result = {
        'directory': str(directory),
        'devices': [parse_device(path) for path in devices],
        'stimuli': [parse_stimulus(path) for path in stimuli],
        'validation': [],
    }
    if len(devices) == 1:
        for stimulus in stimuli:
            result['validation'].append({
                'device': devices[0].name,
                'stimulus': stimulus.name,
                'errors': validate_pair(devices[0], stimulus),
            })
    return result


def print_human_summary(payload: dict) -> None:
    print(f"Directory: {payload['directory']}")
    for device in payload['devices']:
        print(f"\nDevice: {Path(device['path']).name}")
        print(f"  Ecorce format: {device['format_version']}")
        print(f"  Dimension: {device['dimension']}")
        print(f"  Contacts: {', '.join(c['name'] for c in device['contacts'])}")
        print(f"  Materials: {', '.join(m['material'] for m in device['materials'])}")
        geometry = device['geometry']
        print(
            f"  Geometry entities: {geometry['nodes']} nodes, "
            f"{geometry['lines']} lines, {geometry['surfaces']} surfaces"
        )
    for stimulus in payload['stimuli']:
        print(f"\nStimulus: {Path(stimulus['path']).name}")
        print(f"  Analysis: {stimulus['analysis']}")
        print(f"  Temperature: {stimulus['temperature']}")
        for bias in stimulus['biases']:
            if bias['constant']:
                description = bias['constant']
            else:
                description = f"{bias['start']} -> {bias['end']} (step {bias['increment']})"
            print(f"  {bias['contact']}: {bias['bias_type']} {description}")
    for item in payload['validation']:
        if item['errors']:
            print(f"\nValidation FAILED for {item['stimulus']}")
            for error in item['errors']:
                print(f"  - {error}")
        else:
            print(f"\nValidation OK: {item['device']} + {item['stimulus']}")


def main(argv: Iterable[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description='Inspect Ecorce .dev/.sti text decks.')
    parser.add_argument('directory', type=Path, help='Directory containing .dev and .sti files')
    parser.add_argument('--json', action='store_true', help='Print JSON instead of a human summary')
    parser.add_argument('--output', type=Path, help='Optional JSON output path')
    args = parser.parse_args(list(argv) if argv is not None else None)

    payload = inspect_directory(args.directory)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_human_summary(payload)

    has_errors = any(item['errors'] for item in payload['validation'])
    return 1 if has_errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
