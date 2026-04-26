from agents.specialized_agents import InventoryAnalystAgent, ProcurementAgent, LogisticsTrackerAgent

class SupplyChainOrchestrator:
    def __init__(self, inventory_agent: InventoryAnalystAgent, procurement_agent: ProcurementAgent, logistics_agent: LogisticsTrackerAgent):
        self.inventory_agent = inventory_agent
        self.procurement_agent = procurement_agent
        self.logistics_agent = logistics_agent

    def run_automated_check(self):
        print("[Orchestrator] Starting automated inventory check...")
        low_stock_items = self.inventory_agent.analyze_stock()
        
        if not low_stock_items:
            print("[Orchestrator] All stock levels are healthy.")
            return

        for item in low_stock_items:
            item_id = item['item_id']
            print(f"[Orchestrator] Alert: Low stock for {item_id} ({item['current_stock']}/{item['threshold']})")
            
            print(f"[Orchestrator] Consulting Procurement Agent for {item_id}...")
            quote = self.procurement_agent.get_best_quote(item_id)
            
            if quote:
                print(f"[Orchestrator] Best quote found: {quote['supplier']} at ${quote['details']['price']} (Lead time: {quote['details']['lead_time']} days)")
                
                # In a real Kore.ai bot, this would be a "Human-in-the-loop" node
                print(f"[Orchestrator] Requesting approval to order 100 units of {item_id}...")
                approved = True # Simulated approval
                
                if approved:
                    po_number = self.procurement_agent.order_item(quote['supplier'], item_id, 100)
                    print(f"[Orchestrator] Order placed successfully. PO Number: {po_number}")
                    
                    print(f"[Orchestrator] Tracking shipment for {po_number}...")
                    tracking = self.logistics_agent.get_eta(po_number)
                    print(f"[Orchestrator] Shipment Status: {tracking['status']}, ETA: {tracking['eta']}")
            else:
                print(f"[Orchestrator] No suppliers found for {item_id}.")
