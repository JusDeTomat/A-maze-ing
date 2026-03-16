#!/usr/bin/env python3
from typing import Dict, Any
from secrets import token_hex


class InvalidConfiguration(Exception):
    """Raised when the configuration file has invalid syntax or values."""


def str_to_dict(content: str) -> Dict[str, Any]:
    """Parse configuration content string into a dict of typed values.

    Raises InvalidConfiguration on syntax/value errors.
    """
    result: dict[str, int | str | tuple[int, int]] = {}
    lines = content.splitlines()
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise InvalidConfiguration(f"Invalid line (no '='): {raw}")

        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key in result:
            raise ValueError("Key Duplicated")

        required = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "SEED",
            "ANIMATED"
        ]

        if not val and key in required:
            if key == "SEED":
                raise ValueError("If you dont want seed, put None")
            raise ValueError(f"{key} cannot be empty")

        try:
            if key in ("WIDTH", "HEIGHT"):
                result[key] = int(val)
            elif key in ("ENTRY", "EXIT"):
                parts = val.split(",")
                if len(parts) != 2:
                    raise InvalidConfiguration(
                          f"Invalid coordinate for {key}: {val}")
                result[key] = (int(parts[0].strip()), int(parts[1].strip()))
            elif key == "OUTPUT_FILE":
                extension = val.split('.')
                if extension[-1] != "txt":
                    raise Exception("Output file must be in .txt format")
                result[key] = val
            elif key == "PERFECT":
                if val.lower() in ("true", "1", "yes"):
                    result[key] = True
                elif val.lower() in ("false", "0", "no"):
                    result[key] = False
                else:
                    raise InvalidConfiguration(
                          f"Invalid boolean for PERFECT: {val}")
            elif key == "SEED":
                result[key] = token_hex(8) if val.lower() == "none" else val
            elif key == "ANIMATED":
                if val.lower() in ("true", "1", "yes"):
                    result[key] = True
                elif val.lower() in ("false", "0", "no"):
                    result[key] = False
            else:
                raise InvalidConfiguration(f"Unknown configuration key: {key}")

        except ValueError as e:
            raise InvalidConfiguration(
                  f"Invalid value for {key}: {val}") from e

    for key in required:
        if key not in result.keys():
            raise ValueError(f"Missing valid key: {key}")
    return result


def parsing(name_file: str) -> Dict[str, Any]:
    """Read a configuration file and return parsed values as a dict.

    Propagates file I/O exceptions for the caller to handle.
    """
    try:
        with open(name_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception:
        raise

    return str_to_dict(content)
