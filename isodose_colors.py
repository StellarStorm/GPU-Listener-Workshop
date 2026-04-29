"""
Colors for setting up isodose lines that match
target dose levels

Copyright (C) Skylar Gay 2021-2026
"""

import logging
import typing as typ

from pydantic.dataclasses import dataclass as pyd_dataclass

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)


@pyd_dataclass
class IsodoseColors:
    template: dict[typ.Union[int, float], list]

    def __post_init__(self):
        self.template = dict(
            sorted(self.template.items(), key=lambda item: item[0])
        )
        self._state: dict = {'normalized': False, 'unit': None}

    def __call__(self):
        return self.template

    def normalize(self):
        """
        Normalize values for Matplotlib
        """
        if not self._state['normalized']:
            self.template = {
                k: [c / 255 for c in v] for k, v in self.template.items()
            }
            self._state['normalized'] = True
        else:
            logger.debug('Already normalized')

    def change_unit(self, to: str):
        if self._state['unit'] == to:
            logger.debug(f'Already in units of {to}, skipping.')
        elif to == 'cGy' and self._state['unit'] in (None, 'Gy'):
            self.template = {(k * 100): v for k, v in self.template.items()}
        elif to == 'Gy' and self._state['unit'] in (None, 'cGy'):
            self.template = {(k / 100): v for k, v in self.template.items()}
        else:
            raise ValueError('Can only convert to/from Gy and cGy')
        self._state['unit'] = to

    def reset(self):
        if self._state['normalized']:
            self.template = {
                k: [int(c * 255) for c in v] for k, v in self.template.items()
            }
            self._state['normalized'] = False
        if self._state['unit'] == 'cGy':
            self.template = {(k / 100): v for k, v in self.template.items()}
            self._state['unit'] = None
        elif self._state['unit'] == 'Gy':
            self.template = {(k * 100): v for k, v in self.template.items()}
            self._state['unit'] = None
