#!/usr/bin/env python

import os

TEMPLATE = """\
#!/usr/bin/env python

from rich import print as rich_print

std_print = print
print = rich_print


def main():
    print("All tests passed.")


if __name__ == "__main__":
    main()
"""


def main():
    day = str(
        max(
            [int(path) for path in os.listdir(".") if path.isdigit()],
            default=0,
        )
        + 1
    ).zfill(2)
    os.mkdir(day)
    run_path = f"./{day}/run.py"
    with open(run_path, "w") as f:
        f.write(TEMPLATE)
    os.system(f"chmod +x {run_path}")
    os.system(f"touch ./{day}/input.txt")
    os.system(f"touch ./{day}/example.txt")
    print(f"Created template for day {int(day)}. Good luck!")


if __name__ == "__main__":
    main()
