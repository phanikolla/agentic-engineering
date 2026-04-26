import random

class ERPSystem:
    def __init__(self):
        self.inventory = {
            "Item_A": {"stock": 50, "threshold": 100, "price": 10.0},
            "Item_B": {"stock": 200, "threshold": 150, "price": 25.0},
            "Item_C": {"stock": 30, "threshold": 50, "price": 100.0}
        }

    def get_stock_levels(self):
        return self.inventory

    def get_item_details(self, item_id):
        return self.inventory.get(item_id, None)

class SupplierPortal:
    def __init__(self):
        self.suppliers = {
            "Supplier_X": {"Item_A": {"price": 9.5, "lead_time": 3}, "Item_C": {"price": 98.0, "lead_time": 5}},
            "Supplier_Y": {"Item_A": {"price": 10.0, "lead_time": 2}, "Item_C": {"price": 105.0, "lead_time": 4}}
        }

    def get_quotes(self, item_id):
        quotes = {}
        for supplier, items in self.suppliers.items():
            if item_id in items:
                quotes[supplier] = items[item_id]
        return quotes

    def place_order(self, supplier_id, item_id, quantity):
        return f"PO-{random.randint(1000, 9999)}"

class ShippingAPI:
    def __init__(self):
        self.shipments = {}

    def track_shipment(self, po_number):
        if po_number not in self.shipments:
            self.shipments[po_number] = {"status": "In Transit", "eta": "2026-05-01"}
        return self.shipments[po_number]
