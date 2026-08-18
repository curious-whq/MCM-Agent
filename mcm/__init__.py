from .ir import Event, Before, Literal, Guard, Case, AliasMap
from .project import project_case
from .merge import normalize_case, merge_equivalent_cases

__all__ = [
    'Event', 'Before', 'Literal', 'Guard', 'Case', 'AliasMap',
    'project_case', 'normalize_case', 'merge_equivalent_cases',
]
