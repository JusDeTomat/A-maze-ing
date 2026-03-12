#!/usr/bin/env python3
from typing import Dict, Any
 

class InvalidConfiguration(Exception):
    """Raised when the configuration file has invalid syntax or values."""

def str_to_dict(content: str) -> Dict[str, Any]:
    result = {}
    lines = content.splitlines()
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise InvalidConfiguration(f"Invalid line (no '='): {raw}")

        key, val = line.split("=", 1)
        key = key.strip().upper()
        val = val.strip()

        try:
            if key in ("WIDTH", "HEIGHT"):
                result[key] = int(val)
            elif key in ("ENTRY", "EXIT"):
                parts = val.split(",")
                if len(parts) != 2:
                    raise InvalidConfiguration(f"Invalid coordinate for {key}: {val}")
                result[key] = (int(parts[0].strip()), int(parts[1].strip()))
            elif key == "OUTPUT_FILE":
                result[key] = val
            elif key == "PERFECT":
                if val.lower() in ("true", "1", "yes"):
                    result[key] = True
                elif val.lower() in ("false", "0", "no"):
                    result[key] = False
                else:
                    raise InvalidConfiguration(f"Invalid boolean for PERFECT: {val}")
            elif key == "SEED":
                result[key] = None if val.lower() == "none" else val
            else:
                raise InvalidConfiguration(f"Unknown configuration key: {key}")
        except ValueError as e:
            raise InvalidConfiguration(f"Invalid value for {key}: {val}") from e
    return result


	
def parsing(name_file: str) -> Dict[str, Any]:
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


def main():
    config = parsing("config.txt")
    print(config)


if __name__ == "__main__":
    main()