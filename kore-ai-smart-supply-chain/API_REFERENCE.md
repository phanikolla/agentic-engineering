# Smart Supply Chain Orchestrator: API Reference (Mock Systems)

This document outlines the conceptual APIs used by the specialized agents to interact with external systems. These are currently mocked for demonstration purposes.

## 1. ERP System API

### `GET /v1/inventory`
Retrieves the current stock levels and thresholds for all items.

- **Endpoint (Mock)**: `ERPSystem.get_stock_levels()`
- **Description**: Returns a dictionary of item IDs with their current stock, reorder threshold, and price.
- **Example Response**:
```json
{
    "Item_A": {"stock": 50, "threshold": 100, "price": 10.0},
    "Item_B": {"stock": 200, "threshold": 150, "price": 25.0},
    "Item_C": {"stock": 30, "threshold": 50, "price": 100.0}
}
```

### `GET /v1/inventory/{item_id}`
Retrieves details for a specific item.

- **Endpoint (Mock)**: `ERPSystem.get_item_details(item_id)`
- **Description**: Returns details for the specified `item_id`.
- **Parameters**:
    - `item_id` (string, path): The unique identifier of the item.
- **Example Response**:
```json
{
    "stock": 50,
    "threshold": 100,
    "price": 10.0
}
```

## 2. Supplier Portal API

### `GET /v1/quotes/{item_id}`
Retrieves quotes from various suppliers for a given item.

- **Endpoint (Mock)**: `SupplierPortal.get_quotes(item_id)`
- **Description**: Returns a dictionary of suppliers with their respective prices and lead times for the `item_id`.
- **Parameters**:
    - `item_id` (string, path): The unique identifier of the item.
- **Example Response**:
```json
{
    "Supplier_X": {"price": 9.5, "lead_time": 3},
    "Supplier_Y": {"price": 10.0, "lead_time": 2}
}
```

### `POST /v1/orders`
Places a purchase order with a specified supplier for an item.

- **Endpoint (Mock)**: `SupplierPortal.place_order(supplier_id, item_id, quantity)`
- **Description**: Simulates placing an order and returns a Purchase Order (PO) number.
- **Parameters**:
    - `supplier_id` (string, body): The unique identifier of the supplier.
    - `item_id` (string, body): The unique identifier of the item to order.
    - `quantity` (integer, body): The quantity of the item to order.
- **Example Response**:
```
"PO-1234"
```

## 3. Shipping Carrier API

### `GET /v1/track/{po_number}`
Tracks the status of a shipment using its purchase order number.

- **Endpoint (Mock)**: `ShippingAPI.track_shipment(po_number)`
- **Description**: Returns the current status and estimated time of arrival (ETA) for the shipment.
- **Parameters**:
    - `po_number` (string, path): The Purchase Order number to track.
- **Example Response**:
```json
{
    "status": "In Transit",
    "eta": "2026-05-01"
}
```
