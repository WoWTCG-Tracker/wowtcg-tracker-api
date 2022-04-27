"""
Database fill script for wowtcg-tracker-api

Script is used to fill database with all cards and extensions details
"""
import asyncio
import json
import os
import sys

from typing import Any
from colorama import Fore, Style
from dotenv import load_dotenv

from prisma import Prisma
from progressbar import progressbar

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from api import database


def print_section_end() -> None:
  """Prints a long line to separate sections in terminal"""
  print(Fore.MAGENTA + "=" * 70 + Style.RESET_ALL)


def get_data_from_json(path: str) -> Any:
  """Returns loaded json from provided path"""
  try:
    with open(path, "r", encoding="utf-8") as file:
      return json.load(file)
  except FileNotFoundError:
    sys.exit(f"{Fore.RED}⚠ {path} not found{Style.RESET_ALL}")


if __name__ == "__main__":
  ###
  # Load environment variables from .env file
  ###

  load_dotenv()

  ###
  # Ask user if he wants to delete all data from database
  ###

  print(
      f"{Fore.MAGENTA}ᓚᕬᗢ Wowtcg-tracker-api db fill script ᗢᕬᓗ{Style.RESET_ALL}"
  )
  print(
      f"{Fore.YELLOW}⚠ This script will delete all data in database and import data from assets folder{Style.RESET_ALL}"
  )
  to_continue = input(
      f"{Fore.YELLOW}⚠ Do you want to continue? [Y/n]:{Style.RESET_ALL} ")
  if to_continue.lower() == "n":
    sys.exit(0)
  db = Prisma()
  print_section_end()

  ###
  # Import data from assets folder
  ###

  print(f"{Fore.CYAN}🛈 Importing data from assets folder...{Style.RESET_ALL}")
  # cards = get_data_from_json("assets/cards.json")
  # card_prints = get_data_from_json("assets/prints.json")
  expansions_dict = get_data_from_json("assets/expansions.json")
  block_sets_count = len(expansions_dict)
  expansion_blocks_count = len([
      expansion_block for block_set in expansions_dict.values()
      for expansion_block in block_set.values()
  ])
  expansions_count = len([
      expansion for block_set in expansions_dict.values()
      for expansion_block in block_set.values() for expansion in expansion_block
  ])

  #print(
  #    f"{Fore.CYAN}Imported {Fore.YELLOW}{len(card_prints)}{Fore.CYAN} card prints of {Fore.YELLOW}{len(cards)}{Fore.CYAN} cards{Style.RESET_ALL}"
  #)
  print(
      f"{Fore.CYAN}Imported {Fore.YELLOW}{expansions_count}{Fore.CYAN} expansions from {Fore.YELLOW}{expansion_blocks_count}{Fore.CYAN} blocks of {Fore.YELLOW}{block_sets_count}{Fore.CYAN} sets{Style.RESET_ALL}"
  )
  print_section_end()

  ###
  # Delete old data
  ###
  print(f"{Fore.CYAN}🛈 Deleting old sets from database{Style.RESET_ALL}")
  deleted_sets_count = asyncio.run(database.delete_all_block_sets(db=db))
  print(
      f"{Fore.CYAN}🛈 Deleted {Fore.YELLOW}{deleted_sets_count}{Fore.CYAN} old set{'' if deleted_sets_count == 1 else 's'}{Style.RESET_ALL}"
  )
  print(f"{Fore.CYAN}🛈 Deleting old cards from database{Style.RESET_ALL}")
  deleted_cards_count = asyncio.run(database.delete_all_cards(db=db))
  print(
      f"{Fore.CYAN}🛈 Deleted {Fore.YELLOW}{deleted_cards_count}{Fore.CYAN} old card{'' if deleted_cards_count == 1 else 's'}{Style.RESET_ALL}"
  )
  print_section_end()

  ###
  # Insert new data
  ###
  for block_set in expansions_dict:
    print(
        f"{Fore.CYAN}🛈 Inserting new set {Fore.YELLOW}{block_set}{Style.RESET_ALL}"
    )
    tmp_block_set = asyncio.run(database.add_block_set(db=db, name=block_set))
    for expansion_block in progressbar(expansions_dict[block_set], block_set,
                                       "block"):
      tmp_expansion_block = asyncio.run(
          database.add_expansion_block(db=db,
                                       name=expansion_block,
                                       block_set_id=tmp_block_set.id))
      for expansion in expansions_dict[block_set][expansion_block]:
        asyncio.run(
            database.add_expansion(db=db,
                                   name=expansion,
                                   expansion_block_id=tmp_expansion_block.id))

  print(f"{Fore.GREEN}🛈 Done!{Style.RESET_ALL}")
