"""This module contains data structures regarding issues."""

import json
from enum import Enum
from uuid import uuid4


class Severity(Enum):
    """An Enum denoting the severities an issue can have."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __str__(self):
        return self.name


class Issue:
    """An object describing a vulnerability, weakness, or informational
    message."""

    def __init__(
        self,
        title: str = None,
        description: str = None,
        severity: Severity = None,
        raw_data: str = None,
    ):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.severity = severity
        self.raw_data = raw_data

    def is_severe(self) -> bool:
        """Returns whether the issue is considered severe.

        :return: A boolean indicating whether the issue is severe
        """
        return not (self.severity == Severity.LOW or self.severity.NONE)

    def is_complete(self) -> bool:
        """Returns whether the issue is complete.

        :return: A boolean indicating that the issue is complete
        """
        return all(
            (
                self.id,
                self.title is not None,
                self.description is not None,
                self.severity is not None,
            )
        )

    def to_dict(self) -> dict:
        """Converts the issue instance into a Python dict.

        :return: A dict representing the issue
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": str(self.severity).lower(),
            "raw": json.dumps(self.raw_data),
        }
