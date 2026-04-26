from tools.mock_systems import ERPSystem, SupplierPortal, ShippingAPI
from agents.specialized_agents import InventoryAnalystAgent, ProcurementAgent, LogisticsTrackerAgent
from agents.supervisor import SupplyChainOrchestrator

def main():
    # Initialize Mock Systems
    erp = ERPSystem()
    portal = SupplierPortal()
    shipping = ShippingAPI()

    # Initialize Specialized Agents
    inventory_agent = InventoryAnalystAgent(erp)
    procurement_agent = ProcurementAgent(portal)
    logistics_agent = LogisticsTrackerAgent(shipping)

    # Initialize Supervisor
    orchestrator = SupplyChainOrchestrator(inventory_agent, procurement_agent, logistics_agent)

    # Run the simulation
    orchestrator.run_automated_check()

if __name__ == "__main__":
    main()
