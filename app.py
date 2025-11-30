# food_app.py
import uuid
import time

# Simple in-memory stores
restaurants = {
    "R1": {"name": "Pizza Place", "menu": {"M1": ("Margherita", 6.5), "M2": ("Pepperoni", 8.0)}},
    "R2": {"name": "Burger Hub", "menu": {"M3": ("Classic Burger", 5.0), "M4": ("Fries", 2.0)}}
}
orders = {}  # orderID -> order dict
drivers = [{"id": "D1", "name": "Ali"}, {"id": "D2", "name": "Sara"}]

def list_restaurants():
    print("\nRestaurants:")
    for rid, r in restaurants.items():
        print(f"{rid}: {r['name']}")
    print()

def show_menu(rid):
    menu = restaurants[rid]["menu"]
    print(f"\nMenu for {restaurants[rid]['name']}:")
    for mid, (name, price) in menu.items():
        print(f"{mid} - {name}: ${price:.2f}")
    print()

def simulate_payment(amount):
    print(f"\nProcessing payment of ${amount:.2f}...")
    time.sleep(1)
    # Simple random-like success (deterministic here for demo)
    return True, "TXN-" + str(uuid.uuid4())[:8]

def assign_driver():
    # simple round-robin
    return drivers[len(orders) % len(drivers)]

def place_order():
    list_restaurants()
    rid = input("Choose restaurant ID: ").strip()
    if rid not in restaurants:
        print("Invalid restaurant.")
        return
    show_menu(rid)
    cart = []
    total = 0.0
    while True:
        mid = input("Enter menu item ID to add (or 'done'): ").strip()
        if mid == "done":
            break
        if mid not in restaurants[rid]["menu"]:
            print("Invalid menu item.")
            continue
        qty = int(input("Quantity: "))
        name, price = restaurants[rid]["menu"][mid]
        cart.append({"id": mid, "name": name, "price": price, "qty": qty})
        total += price * qty
        print(f"Added {qty} x {name} - subtotal ${total:.2f}")
    if not cart:
        print("Cart empty. Cancelling.")
        return
    print(f"\nOrder total: ${total:.2f}")
    method = input("Payment method (card/cod): ").strip().lower()
    if method == "card":
        success, txn = simulate_payment(total)
        if not success:
            print("Payment failed.")
            return
    else:
        txn = "COD"
    order_id = "O-" + str(uuid.uuid4())[:8]
    driver = assign_driver()
    orders[order_id] = {
        "id": order_id,
        "restaurant": rid,
        "items": cart,
        "total": total,
        "status": "Assigned" if method == "card" and txn else "Pending",
        "txn": txn,
        "driver": driver,
        "created": time.time()
    }
    print(f"\nOrder placed. ID: {order_id}")
    print(f"Assigned driver: {driver['name']}, status: {orders[order_id]['status']}")

def show_orders():
    if not orders:
        print("\nNo orders placed yet.")
        return
    for oid, o in orders.items():
        created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(o["created"]))
        print(f"\nOrder {oid} - {o['status']} - ${o['total']:.2f} - Created: {created}")
        print(f"Driver: {o['driver']['name']}, TXN: {o['txn']}")
        for it in o["items"]:
            print(f"  - {it['qty']}x {it['name']} @ ${it['price']:.2f}")

def main_menu():
    while True:
        print("\n--- Online Food Demo ---")
        print("1) Place Order")
        print("2) Show Orders")
        print("3) Exit")
        cmd = input("Choose: ").strip()
        if cmd == "1":
            place_order()
        elif cmd == "2":
            show_orders()
        elif cmd == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()
