
from dataclasses import dataclass


@dataclass
class Animal:
    animal_id: int
    org_id: int
    status: str
    params: dict

    def __post_init__(self):
        for k, v in self.params.items():
            setattr(self, k, v)
        del self.params


