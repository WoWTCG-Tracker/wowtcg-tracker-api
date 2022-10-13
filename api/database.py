"""Useful database queries and functions"""

from typing import Optional

from prisma import Prisma
from prisma.models import BlockSet, ExpansionBlock, Expansion
from prisma.models import Card, CardPrint, User, Collection, Deck


###
# Delete all data from table functions
###
async def delete_all_block_sets(db: Prisma) -> int:
  """Delete all data from block_set table from database"""
  await db.connect()
  deleted_sets_count = await db.blockset.delete_many()
  await db.disconnect()
  return deleted_sets_count


async def delete_all_expansion_blocks(db: Prisma) -> int:
  """Delete all data from expansion_block table from database"""
  await db.connect()
  deleted_expansion_blocks_count = await db.expansionblock.delete_many()
  await db.disconnect()
  return deleted_expansion_blocks_count


async def delete_all_expansions(db: Prisma) -> int:
  """Delete all data from expansion table from database"""
  await db.connect()
  deleted_expansions_count = await db.expansion.delete_many()
  await db.disconnect()
  return deleted_expansions_count


async def delete_all_cards(db: Prisma) -> int:
  """Delete all data from card table from database"""
  await db.connect()
  deleted_cards_count = await db.card.delete_many()
  await db.disconnect()
  return deleted_cards_count


async def delete_all_card_prints(db: Prisma) -> int:
  """Delete all data from card_print table from database"""
  await db.connect()
  deleted_card_prints_count = await db.cardprint.delete_many()
  await db.disconnect()
  return deleted_card_prints_count


async def delete_all_users(db: Prisma) -> int:
  """Delete all data from user table from database"""
  await db.connect()
  deleted_users_count = await db.user.delete_many()
  await db.disconnect()
  return deleted_users_count


async def delete_all_collections(db: Prisma) -> int:
  """Delete all data from collection table from database"""
  await db.connect()
  deleted_collections_count = await db.collection.delete_many()
  await db.disconnect()
  return deleted_collections_count


async def delete_all_decks(db: Prisma) -> int:
  """Delete all data from deck table from database"""
  await db.connect()
  deleted_decks_count = await db.deck.delete_many()
  await db.disconnect()
  return deleted_decks_count


###
# Add data to table functions
###
async def add_block_set(db: Prisma, name: str) -> BlockSet:
  """Add a block set to the database"""
  await db.connect()
  block_set = await db.blockset.create(data={"name": name},)
  await db.disconnect()
  return block_set


async def add_expansion_block(db: Prisma, name: str,
                              block_set_id: int) -> ExpansionBlock:
  """Add an expansion block to the database"""
  await db.connect()
  expansion_block = await db.expansionblock.create(data={
      "name": name,
      "block_set_id": block_set_id,
  })
  await db.disconnect()
  return expansion_block


async def add_expansion(db: Prisma, name: str,
                        expansion_block_id: int) -> Expansion:
  """Add an expansion to the database"""
  await db.connect()
  expansion = await db.expansion.create(data={
      "name": name,
      "expansion_block_id": expansion_block_id,
  })
  await db.disconnect()
  return expansion


async def add_card(db: Prisma,
                   name: str,
                   category: Optional[str] = None,
                   mana_cost: Optional[int] = None,
                   classes: Optional[list] = None,
                   types: Optional[list] = None,
                   attack_types: Optional[list] = None,
                   legalities: Optional[list] = None) -> Card:
  """Add a card to the database"""
  await db.connect()
  card = await db.Card.create(
      data={
          "name": name,
          "category": category,
          "mana_cost": mana_cost,
          "classes": classes,
          "types": types,
          "attack_types": attack_types,
          "legalities": legalities,
      })
  await db.disconnect()
  return card


async def add_card_print(db: Prisma,
                         card_id: int,
                         expansion_id: int,
                         id_in_expansion: int,
                         image_front_url: str,
                         rarity: str,
                         image_back_url: Optional[str] = None,
                         rules: Optional[str] = None) -> CardPrint:
  """Add a card print to the database"""
  await db.connect()
  card_print = await db.cardprint.create(
      data={
          "card_id": card_id,
          "expansion_id": expansion_id,
          "id_in_expansion": id_in_expansion,
          "image_front_url": image_front_url,
          "image_back_url": image_back_url,
          "rules": rules,
          "rarity": rarity,
      })
  await db.disconnect()
  return card_print


async def add_user(db: Prisma,
                   username: str,
                   email: str,
                   user_role: str = "Basic") -> User:
  """Add a user to the database"""
  await db.connect()
  user = await db.user.create(data={
      "username": username,
      "email": email,
      "user_role": user_role,
  })
  await db.disconnect()
  return user


async def add_collcetion(db: Prisma,
                         user_id: int,
                         name: str,
                         description: Optional[str] = None) -> Collection:
  """Add a collection to the database"""
  await db.connect()
  collection = await db.collection.create(data={
      "user_id": user_id,
      "name": name,
      "description": description,
  })
  await db.disconnect()
  return collection


async def add_deck(db: Prisma,
                   user_id: int,
                   hero_card_print_id: int,
                   name: str,
                   description: Optional[str] = None) -> Deck:
  """Add a deck to the database"""
  await db.connect()
  deck = await db.deck.create(
      data={
          "user_id": user_id,
          "name": name,
          "description": description,
          "hero_card_print_id": hero_card_print_id
      })
  await db.disconnect()
  return deck
