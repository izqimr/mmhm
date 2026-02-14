from __future__ import annotations

import re
from typing import Any

from common.logger import get_logger

logger = get_logger(__name__)


class Assertion:
    """Common assertion helpers for API test cases."""

    @staticmethod
    def assert_status_code(response: Any, expected_status_code: int = 200) -> None:
        actual_status_code = getattr(response, "status_code", None)
        if actual_status_code != expected_status_code:
            raise AssertionError(
                f"status_code assert failed, expected={expected_status_code}, actual={actual_status_code}"
            )
        logger.info(
            "status_code assert passed, expected=%s, actual=%s",
            expected_status_code,
            actual_status_code,
        )

    @staticmethod
    def assert_equal(actual: Any, expected: Any, field: str | None = None) -> None:
        if actual != expected:
            field_part = f" field={field}," if field else ""
            raise AssertionError(
                f"equal assert failed,{field_part} expected={expected}, actual={actual}"
            )
        logger.info("equal assert passed, field=%s, expected=%s", field, expected)

    @staticmethod
    def assert_in(member: Any, container: Any, field: str | None = None) -> None:
        if member not in container:
            field_part = f" field={field}," if field else ""
            raise AssertionError(
                f"contains assert failed,{field_part} member={member}, container={container}"
            )
        logger.info("contains assert passed, field=%s, member=%s", field, member)

    @classmethod
    def assert_json_value(cls, response_or_json: Any, path: str, expected: Any) -> Any:
        actual = cls.get_json_value(response_or_json=response_or_json, path=path)
        cls.assert_equal(actual=actual, expected=expected, field=path)
        return actual

    @classmethod
    def get_json_value(cls, response_or_json: Any, path: str) -> Any:
        payload = cls._to_json(response_or_json)
        value = payload
        for part in cls._parse_path(path):
            if isinstance(part, int):
                if not isinstance(value, list):
                    raise AssertionError(
                        f"path resolve failed, expected list before index [{part}], path={path}"
                    )
                try:
                    value = value[part]
                except IndexError as exc:
                    raise AssertionError(
                        f"path resolve failed, index out of range [{part}], path={path}"
                    ) from exc
            else:
                if not isinstance(value, dict):
                    raise AssertionError(
                        f"path resolve failed, expected dict before key '{part}', path={path}"
                    )
                if part not in value:
                    raise AssertionError(f"path resolve failed, key '{part}' not found, path={path}")
                value = value[part]
        logger.info("json path resolve success, path=%s, value=%s", path, value)
        return value

    @staticmethod
    def _to_json(response_or_json: Any) -> Any:
        if isinstance(response_or_json, (dict, list)):
            return response_or_json
        if hasattr(response_or_json, "json"):
            return response_or_json.json()
        raise TypeError("response_or_json should be dict/list or requests.Response")

    @staticmethod
    def _parse_path(path: str) -> list[str | int]:
        if not path:
            raise ValueError("path can not be empty")

        parts: list[str | int] = []
        tokens = path.split(".")
        for token in tokens:
            if not token:
                raise ValueError(f"invalid path format: {path}")
            key_match = re.match(r"^[^\[\]]+", token)
            if key_match:
                parts.append(key_match.group())
            indexes = re.findall(r"\[(\d+)]", token)
            for idx in indexes:
                parts.append(int(idx))
        return parts
