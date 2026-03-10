def str_to_dict(content):
    i_width = content.find("WIDTH")
    i_height = content.find("HEIGHT")
    i_entry = content.find("ENTRY")
    iexit = content.find("EXIT")
    i_output = content.find("OUTPUT_FILE")
    i_perfect = content.find("PERFECT")

def parssing(name_file: str) -> dict:
    try:
        with open(name_file, "r") as file:
            content = file.read()
            print(content)
            str_to_dict(content)
    except FileNotFoundError:
        print("[ERROR] File not found")
    except PermissionError:
        print("[ERROR] Need permition for open file")
    except Exception as e:
        print(f"[ERROR] {e}")


if (__name__ == "__main__"):
    parssing("test.txt")
