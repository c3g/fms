import re
import unicodedata
from typing import Tuple, Union


__all__ = [
    "CoordinateAxis",
    "CoordinateSpec",

    "CoordinateError",

    "alphas",
    "ints",

    "validate_and_normalize_coordinates",
    "check_coordinate_overlap",
]


CoordinateAxis = Tuple[str, ...]
CoordinateSpec = Union[Tuple[()], Tuple[CoordinateAxis], Tuple[CoordinateAxis, CoordinateAxis]]


class CoordinateError(Exception):
    pass


def alphas(end: int) -> CoordinateAxis:
    if end < 0:
        raise ValueError

    if end > 26:
        raise ValueError

    return tuple(chr(a) for a in range(65, 65 + end))


def ints(end: int) -> CoordinateAxis:
    if end < 0:
        raise ValueError

    return tuple(str(i) for i in range(1, end + 1))


def validate_and_normalize_coordinates(coords: str, spec: CoordinateSpec) -> str:
    """
    Given a set of coordinates and a coordinate spec, validates if those coordinates are valid by the spec.
    """

    # TODO: Handle padded 0s?

    c = unicodedata.normalize("NFC", coords.strip())

    coordinate_regex_str = "^" + "".join(f"({'|'.join(s)})" for s in spec) + "$"
    coordinate_regex = re.compile(coordinate_regex_str)

    if not coordinate_regex.match(c):
        raise CoordinateError(f"Invalid coordinates {c} specified for coordinate system {coordinate_regex_str}")

    return c


def check_coordinate_overlap(queryset, obj, parent, obj_type: str = "container"):
    # Check for coordinate overlap with existing child containers/samples of the parent
    existing = queryset.exclude(pk=obj.pk).get(coordinates=obj.coordinates)
    raise CoordinateError(f"Parent container {parent} already contains {obj_type} {existing} at "
                          f"coordinates {obj.coordinates}")