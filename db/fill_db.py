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

from api import database  # pylint: disable=wrong-import-position

RED = Fore.RED
GREEN = Fore.GREEN
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
YELLOW = Fore.YELLOW
RESET_COLOR = Style.RESET_ALL


def print_section_end() -> None:
  """Prints a long line to separate sections in terminal"""
  print(MAGENTA + "=" * 70 + RESET_COLOR)


def get_data_from_json(path: str) -> Any:
  """Returns loaded json from provided path"""
  try:
    with open(path, "r", encoding="utf-8") as file:
      return json.load(file)
  except FileNotFoundError:
    sys.exit(f"{RED}⚠ {path} not found{RESET_COLOR}")


if __name__ == "__main__":
  ###
  # Load environment variables from .env file
  ###

  load_dotenv()

  ###
  # Ask user if he wants to delete all data from database
  ###

  print(f"{MAGENTA}ᓚᕬᗢ Wowtcg-tracker-api "
        f"db fill script ᗢᕬᓗ{RESET_COLOR}")
  print(f"{YELLOW}⚠ This script will delete all data in database "
        f"and import data from assets folder{RESET_COLOR}")
  to_continue = input(
      f"{YELLOW}⚠ Do you want to continue? [Y/n]:{RESET_COLOR} ")
  if to_continue.lower() == "n":
    sys.exit(0)
  db = Prisma()
  print_section_end()

  ###
  # Import data from assets folder
  ###

  print(f"{CYAN}🛈 Importing data from assets folder...{RESET_COLOR}")
  cards = get_data_from_json("assets/cards.json")
  card_prints = get_data_from_json("assets/prints.json")
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

  print(f"{CYAN}Imported {YELLOW}{len(card_prints)}{CYAN}"
        f" card prints of {YELLOW}{len(cards)}{CYAN}"
        f" cards{RESET_COLOR}")
  print(f"{CYAN}Imported {YELLOW}{expansions_count}{CYAN}"
        f" expansions from {YELLOW}{expansion_blocks_count}{CYAN}"
        f" blocks of {YELLOW}{block_sets_count}{CYAN}"
        f" sets{RESET_COLOR}")
  print_section_end()

  ###
  # Delete old data
  ###
  print(f"{CYAN}🛈 Deleting old sets from database{RESET_COLOR}")
  deleted_sets_count = asyncio.run(database.delete_all_block_sets(db=db))
  print(f"{CYAN}🛈 Deleted {YELLOW}{deleted_sets_count}{CYAN}"
        f" old set{'' if deleted_sets_count == 1 else 's'}{RESET_COLOR}")
  print(f"{CYAN}🛈 Deleting old cards from database{RESET_COLOR}")
  deleted_cards_count = asyncio.run(database.delete_all_cards(db=db))
  print(f"{CYAN}🛈 Deleted {YELLOW}{deleted_cards_count}{CYAN}"
        f" old card{'' if deleted_cards_count == 1 else 's'}{RESET_COLOR}")
  print_section_end()

  ###
  # Insert new data
  ###
  for block_set in expansions_dict:
    print(f"{CYAN}🛈 Inserting new set "
          f"{YELLOW}{block_set}{RESET_COLOR}")
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

  for card in progressbar(cards, suffix="Card"):
    asyncio.run(
        database.add_card(
            db=db,
            name=card,
            category=cards[card]["card_category"],
            mana_cost=cards[card]["card_mana_cost"],
            classes=cards[card]["card_classes"],
            types=cards[card]["card_types"],
            attack_type=cards[card]["card_attack_type"],
            legalities=cards[card]["card_legalities"],
        ))
  for card_print in progressbar(card_prints, suffix="Card print"):
    card_id = asyncio.run(db.card.find_unique(where={"name": card_print["card_name"]}))
    if not card_id:
      print(f"{RED}⚠ An error occurred while inserting card print")
      print(f"{RED}⚠ Card {YELLOW}{card_print['card_name']}{RED} not found in database{RESET_COLOR}")
    expansion_id = asyncio.run(db.expansion.find_unique(where={"name": card_print["card_print_expansion_name"]}))
    if not expansion_id:
      print(f"{RED}⚠ An error occurred while inserting card print")
      print(f"{RED}⚠ Expansion {YELLOW}{card_print['card_print_expansion_name']}{RED} not found in database{RESET_COLOR}")
    asyncio.run(
        database.add_card_print(
            db=db,
            card_id=card_id,
            expansion_id=expansion_id,
            rarity=card_print["card_print_rarity"],
            text_front=card_print["card_print_text_front"],
            text_back=card_print["card_print_text_back"]))

  print_section_end()
  print(f"{GREEN}🛈 Done!{RESET_COLOR}")
