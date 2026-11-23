"""Depth patterns from auditor classifications only; never inferred from prose."""
from .common import require


def shot_pattern(shot):
    directions = [p.get('depth_direction') for p in shot['phases']]
    if not directions or any(d is None for d in directions):
        return None
    moving = []
    for direction in directions:
        require(direction in {'IN', 'OUT', 'NO IN/OUT'}, 'Invalid depth direction')
        if direction != 'NO IN/OUT' and (not moving or moving[-1] != direction):
            moving.append(direction)
    return ' → '.join(moving) if moving else 'NO IN/OUT'


def provenance(shot, index):
    return [{'source_pointer': f'/shots/{index}/phases/{j}/depth_direction',
             'phase': p['phase'], 'depth_direction': p.get('depth_direction'),
             'interval_s': [p['start_s'], p['end_s']], 'evidence_ids': list(p['evidence'])}
            for j, p in enumerate(shot['phases'])]


def video_pattern(shots):
    values = [shot_pattern(s) for s in shots]
    return ' – '.join('—' if v is None else f'({v})' if ' → ' in v else v for v in values)


def validate_direction(phase):
    """Explicit Dolly translation can contradict a classification; zoom/orbit cannot."""
    declared = phase['depth_direction']
    explicit = {c['movement'] for c in phase['components_parsed']} & {'Dolly-In', 'Dolly-Out'}
    require(len(explicit) < 2, 'Split opposing Dolly directions into separate phases')
    if declared is not None and explicit:
        expected = 'IN' if 'Dolly-In' in explicit else 'OUT'
        require(declared == expected, 'depth_direction conflicts with explicit Dolly component')
