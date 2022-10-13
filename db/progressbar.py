"""
Progress bar module

Bar was made becuase modules providing progress bars use stout
which makes prisma a bit clunky.
"""

import sys
from colorama import Fore, Style
from typing import Generator

def progressbar(iterable,
                prefix="",
                suffix="",
                print_size=80,
                file=sys.stdout) -> Generator:
  """Call in a loop to create terminal progress bar"""

  count = len(iterable)
  prefix = prefix.ljust(15)
  suffix += " " if count == 1 else "s"
  bar_size = print_size - len(prefix) - len(suffix) - 8

  def show(progress: int) -> None:
    relative_progress = int(bar_size * progress / count)
    bar = f"{Fore.CYAN}{prefix} |{Fore.YELLOW}"
    bar += f"{'█' * relative_progress}{'.' * (bar_size - relative_progress)}"
    bar += f"{Fore.CYAN}| {Fore.YELLOW}{progress}{Fore.CYAN}/{Fore.YELLOW}"
    bar += f"{count} {Fore.CYAN}{suffix}{Style.RESET_ALL}\r"
    file.write(bar)
    file.flush()

  show(0)
  for i, item in enumerate(iterable):
    yield item
    show(i + 1)
  file.write("\n")
  file.flush()
