from tools.mock_systems import ERPSystem, SupplierPortal, ShippingAPI

class InventoryAnalystAgent:
    def __init__(self, erp: ERPSystem):
        self.erp = erp

    def analyze_stock(self):
        inventory = self.erp.get_stock_levels()
        low_stock_items = []
        for item_id, details in inventory.items():
            if details['stock'] < details['threshold']:
                low_stock_items.append({
                    "item_id": item_id,
                    "current_stock": details['stock'],
                    "threshold": details['threshold']
                })
        return low_stock_items

class ProcurementAgent:
    def __init__(self, portal: SupplierPortal):
        self.portal = portal

    def get_best_quote(self, item_id):
        quotes = self.portal.get_quotes(item_id)
        if not quotes:
            return None
        # Simple logic: choose lowest price
        best_supplier = min(quotes, key=lambda x: quotes[x]['price'])
        return {"supplier": best_supplier, "details": quotes[best_supplier]}

    def order_item(self, supplier_id, item_id, quantity):
        po_number = self.portal.place_order(supplier_id, item_id, quantity)
        return po_number

class LogisticsTrackerAgent:
    def __init__(self, shipping: ShippingAPI):
        self.shipping = shipping

    def get_eta(self, po_number):
        return self.shipping.track_shipment(po_number)
