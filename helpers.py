from colorama import Fore


def color_print(color: str, message: str) -> None:
    fore_color: str = ""
    choosen_color = color.lower()
    match choosen_color:
        case "red":
            fore_color = Fore.RED
        case "yellow":
            fore_color = Fore.YELLOW
        case "blue":
            fore_color = Fore.BLUE
        case "green":
            fore_color = Fore.GREEN
        case _:
            color_print("red", "Invalid color print, printing white...")
            fore_color = Fore.WHITE

    colored_message: str = f"{fore_color}{message}{Fore.RESET}"
    print(colored_message)
