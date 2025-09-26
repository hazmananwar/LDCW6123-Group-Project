from dataclasses import dataclass
from typing import Dict

#Global settings
TAX_RATE = 0.06          # 6% SST
STANDARD_SHIP = 8.00     # RM
EXPRESS_SHIP = 15.00     # RM

#Data models
@dataclass
class Item:
    id: str
    name: str
    price: float
    buy_n_get_1_free: int | None = None

@dataclass
class CartLine:
    item: Item
    qty: int

#Product catalog
CATALOG: Dict[str, Item] = {
    "A1": Item("A1", "Reusable Tote Bag", 12.90),
    "A2": Item("A2", "Organic Coffee 250g", 24.50),
    "B1": Item("B1", "Baby Wipes (80s)", 7.90, buy_n_get_1_free=3),  # Buy 3 Pay 2
    "B2": Item("B2", "Kids Colouring Book", 9.50),
    "C1": Item("C1", "Wireless Mouse", 39.00),
    "C2": Item("C2", "USB-C Cable", 15.00),
}
