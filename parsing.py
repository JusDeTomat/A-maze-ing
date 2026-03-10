def str_to_dict(content: str) -> dict:
    result = {}
    lst_content = content.split("\n")
    for element in lst_content:
        element_splited = element.split("=")
        if element_splited[0] == "WIDTH" or element_splited[0] == "HEIGHT":
            result[element_splited[0]] = int(element_splited[1])
        elif (element_splited[0] == "ENTRY" or element_splited[0] == "EXIT"):
            value = element_splited[1].split(",")
            result[element_splited[0]] = (int(value[0]),int(value[1]))
        elif (element_splited[0] == "OUTPUT_FILE"):
            result[element_splited[0]] = element_splited[1]
        elif (element_splited[0] == "PERFECT"):
            result[element_splited[0]] = bool(element_splited[1])
    return result

	
def parssing(name_file: str) -> dict:
    try:
        with open(name_file, "r") as file:
            content = file.read()
            print(content)
            result = str_to_dict(content)
            print(result)
    except FileNotFoundError:
        print("[ERROR] File not found")
    except PermissionError:
        print("[ERROR] Need permition for open file")
    except Exception as e:
        print(f"[ERROR] {e}")


if (__name__ == "__main__"):
    parssing("test.txt")
