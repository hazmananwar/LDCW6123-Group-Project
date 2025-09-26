from typing import List
from models import CartLine, TAX_RATE, STANDARD_SHIP, EXPRESS_SHIP

# --- Promo codes: code -> (description, calculator) ---
PROMO_CODES = {
    "IBU10": ("10% off orders ≥ RM50",
              lambda subtotal, ship, cart: 0.10 * subtotal if subtotal >= 50 else 0.0),
    "FREESHIP": ("Free Standard Shipping",
                 lambda subtotal, ship, cart: ship if ship > 0 and ship == STANDARD_SHIP else 0.0),
}

def calc_b3p2_discount(line: CartLine) -> float:
    """Buy 3 Pay 2: every 3rd unit free."""
    if line.item.buy_n_get_1_free == 3 and line.qty >= 3:
        free_units = line.qty // 3
        return free_units * line.item.price
    return 0.0

def summarize(cart: List[CartLine], shipping_choice: str, promo_code: str | None, is_member: bool) -> None:
    """Compute and PRINT a full bill breakdown for the given cart and options."""
    subtotal = 0.0
    line_savings = 0.0

    print("\n=== Cart Summary ===")
    if not cart:
        print("Your cart is empty.")
        return

    print(f"{'Item':<24}{'Qty':>5}{'Unit':>10}{'Line (RM)':>12}{'Savings':>10}")
    for ln in cart:
        line_total = ln.qty * ln.item.price
        discount = calc_b3p2_discount(ln)
        line_savings += discount
        subtotal += (line_total - discount)
        print(f"{ln.item.name:<24}{ln.qty:>5}{ln.item.price:>10.2f}{line_total - discount:>12.2f}{discount:>10.2f}")

    # Shipping
    if shipping_choice == "2":
        ship = EXPRESS_SHIP
    else:
        ship = 0.0 if subtotal >= 100 else STANDARD_SHIP  # standard (free ≥ RM100)

    # Promo
    promo_disc = 0.0
    promo_desc = "-"
    if promo_code:
        code = promo_code.upper()
        if code in PROMO_CODES:
            promo_desc = PROMO_CODES[code][0]
            promo_disc = PROMO_CODES[code][1](subtotal, ship, cart)
        else:
            promo_desc = "Invalid code"

    # Loyalty
    member_disc = 0.05 * max(subtotal - promo_disc, 0) if is_member else 0.0

    # Tax on discounted merchandise (not on shipping)
    taxable_amount = max(subtotal - promo_disc - member_disc, 0)
    tax = TAX_RATE * taxable_amount

    # If promo is "FREESHIP", we already set promo_disc to the shipping amount.
    effective_ship = max(ship - (promo_disc if promo_desc.startswith("Free") else 0), 0)

    total = taxable_amount + tax + effective_ship

    print("\n--- Charges ---")
    print(f"Merchandise Subtotal : RM{subtotal:,.2f}")
    print(f"Line-item Savings    : RM{line_savings:,.2f} (e.g., Buy 3 Pay 2)")
    print(f"Shipping             : RM{ship:,.2f} ({'Express' if shipping_choice=='2' else 'Standard'})")
    print(f"Promo Code           : {promo_code.upper() if promo_code else '-'} ({promo_desc})  ->  -RM{promo_disc:,.2f}")
    print(f"Loyalty Member 5%    : {'Yes' if is_member else 'No'} ->  -RM{member_disc:,.2f}")
    print(f"Tax @ {int(TAX_RATE*100)}%        : RM{tax:,.2f}")
    print("------------------------")
    print(f"Grand Total          : RM{total:,.2f}")

    total_savings = line_savings + promo_disc + member_disc + (STANDARD_SHIP if (shipping_choice!='2' and subtotal>=100) else 0)
    print(f"Total Savings        : RM{total_savings:,.2f}\n")
