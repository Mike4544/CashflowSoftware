import backend.integrations.excel as excel

INTEGRATIONS: dict = {
    "excel": excel.__get_data_from_excel,
    # Expand this as needed
}

def __repair_str(string: str) -> str:
    """
    Repair a string
    """
    str = ''
    for char in string:
        if char.isalpha():
            str += char.lower()

    return str

def integration(name: str, file: str) -> list:
    """
    Get data from an excel file
    """
    try:
        print(f"Using integration {name}")
        print("All integrations: ", INTEGRATIONS)
        func = INTEGRATIONS[__repair_str(name)]
        print("Function: ", func)
        return func(file)
    except KeyError:
        raise Exception("Integration not found")