#!/usr/bin/env python3
import sys
from parsing import parsing, InvalidConfiguration


def main(argv=None):
    """Wrapper entrypoint that validates config and launches visual with robust error handling.

    Usage: python3 a_maze_ing.py path/to/config.txt
    """
    argv = argv if argv is not None else sys.argv
    if len(argv) < 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return 1

    config_path = argv[1]

    try:
        cfg = parsing(config_path)
    except FileNotFoundError:
        print(f"[ERROR] Configuration file not found: {config_path}")
        return 2
    except PermissionError:
        print(f"[ERROR] Permission denied reading configuration: {config_path}")
        return 3
    except InvalidConfiguration as e:
        print(f"[ERROR] Invalid configuration: {e}")
        return 4

    try:
        import visual
    except Exception as e:
        print(f"[ERROR] Cannot import visual module: {e}")
        return 5

    try:
        try:
            return visual.main(config_path)
        except TypeError:
            return visual.main()
    except Exception as e:
        print(f"[ERROR] Failed to start visual: {e}")
        return 6


if __name__ == "__main__":
    main()git 
