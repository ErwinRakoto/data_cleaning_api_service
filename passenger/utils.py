MALE_TITLES = {"Mr.", "Master.", "Don.", "Rev.", "Sir.", "Col.", "Capt.", "Jonkheer."}
FEMALE_TITLES = {"Mrs.", "Miss.", "Ms.", "Mme.", "Lady.", "Dona.", "Countess.", "Dr."}


def parse_name(name: str) -> tuple[str, str, str]:
    """
    parse name format Titanic (Last name, Title. First names)
    into (last_name, title, first_name)
    Args:
        name: Raw name from dataset

    Returns: (last_name, title, first_name)

    """
    last_name, rest = name.split(", ", 1)
    title, given = rest.split(" ", 1)

    if "(" in given and ")" in given:
        start = given.index("(") + 1
        end = given.index(")")
        first_name = given[start:end].strip()
    else:
        first_name = given.strip()

    return last_name.strip(), title.strip(), first_name


def normalize_title(title: str, sex: str | None) -> str:
    """
    normalize title based on sex first, then title to "Mr." or "Mrs." or "Rare".
    Args:
        title: Raw title extracted from name
        sex: Passenger sex

    Returns: Normalized title

    """
    if sex is not None:
        if sex.lower() == "male":
            return "Mr."
        if sex.lower() == "female":
            return "Mrs."
    if title in MALE_TITLES:
        return "Mr."
    if title in FEMALE_TITLES:
        return "Mrs."
    return "Rare"
