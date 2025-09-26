from typing import List
from models import CATALOG, CartLine
from pricing import summarize

def show_catalog() -> None:
    print("\n=== Product Catalog ===")
    print(f"{'ID':<4} {'Item':<24} {'Price (RM)':>10} {'Offer':>10}")
    for it in CATALOG.values():
        offer = "Buy 3 Pay 2" if it.buy_n_get_1_free == 3 else "-"
        print(f"{it.id:<4} {it.name:<24} {it.price:>10.2f} {offer:>10}")
    print()

def safe_int(prompt: str, min_val: int = 0, max_val: int | None = None) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if v < min_val or (max_val is not None and v > max_val):
                raise ValueError()
            return v
        except ValueError:
            rng = f"{min_val}–{max_val}" if max_val is not None else f"≥{min_val}"
            print(f"  ! Please enter a valid integer ({rng}).")

def main():
    cart: List[CartLine] = []
    print("Welcome to Ibupreneur Demo Shop 🧺 (Shopping Cart Summary)\n")
    while True:
        print("Menu:")
        print("  1) View catalog")
        print("  2) Add item")
        print("  3) Remove item")
        print("  4) View current summary")
        print("  5) Checkout & final summary")
        print("  0) Exit")
        choice = input("Choose: ").strip()

        match choice:
            case "1":
                show_catalog()

            case "2":
                show_catalog()
                item_id = input("Enter Item ID to add: ").strip().upper()
                if item_id not in CATALOG:
                    print("  ! Item not found.\n"); continue
                qty = safe_int("Enter quantity: ", 1, 100)
                cart.append(CartLine(CATALOG[item_id], qty))
                print("  ✓ Added to cart.\n")

            case "3":
                if not cart:
                    print("  ! Cart is empty.\n"); continue
                for i, ln in enumerate(cart, 1):
                    print(f"  {i}) {ln.item.name} x{ln.qty}")
                idx = safe_int("Select line to remove: ", 1, len(cart))
                removed = cart.pop(idx - 1)
                print(f"  ✓ Removed {removed.item.name}.\n")

            case "4":
                summarize(cart, shipping_choice="1", promo_code=None, is_member=False)

            case "5":
                if not cart:
                    print("  ! Add something first.\n"); continue
                print("\nShipping:\n  1) Standard  (RM8, free ≥ RM100)\n  2) Express   (RM15)")
                ship_choice = input("Choose shipping [1/2]: ").strip()
                promo = input("Enter promo code (or leave blank): ").strip() or None
                mem = input("Loyalty member? [y/n]: ").strip().lower().startswith("y")
                summarize(cart, ship_choice, promo, mem)
                print("Thank you! 🧡"); break

            case "0":
                print("Bye!"); break

            case _:
                print("  ! Invalid menu.\n")

if __name__ == "__main__":
    main()
