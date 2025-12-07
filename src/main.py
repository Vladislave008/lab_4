from src.simulation import Simulator
from src.constants import COLORS
from typing import Optional

def main() -> None:
    print(f"{COLORS.LIGHT_BLUE}Preparing to run a random simulation...{COLORS.RESET}")
    try:
        inp_n = str(input(f"{COLORS.LIGHT_BLUE}Type in the number of steps for a simulation (Press Enter for default):{COLORS.RESET} "))
        inp_seed = str(input(f"{COLORS.LIGHT_BLUE}Type in the seed value for a simulation (Press Enter for default):{COLORS.RESET} "))
        if inp_n == '':
            n = 20
        else:
            n = int(inp_n)
        if inp_seed == '':
            seed: Optional[int] = None
        else:
            seed = int(inp_seed)
    except Exception:
        print(f"{COLORS.RED}Bad input{COLORS.RESET}")
        return
    s = Simulator()
    s.run_simulation(n, seed)
    print(s.library.generate_report())
if __name__ == "__main__":
    main()
