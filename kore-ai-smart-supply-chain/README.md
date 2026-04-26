# Smart Supply Chain Orchestrator

## Project Overview
This project demonstrates a real-world use case of the Kore.ai agentic architecture, implementing a **Smart Supply Chain Orchestrator**. The system is designed to autonomously monitor inventory, manage procurement, and track logistics, leveraging a multi-agent system orchestrated by a central supervisor.

## Architecture
The system employs a **Supervisor Pattern** for agent orchestration, where a central `Supply Chain Orchestrator` agent delegates tasks to specialized agents:

- **Inventory Analyst Agent**: Monitors stock levels and identifies items requiring reorder.
- **Procurement Agent**: Manages supplier interactions, obtains quotes, and places orders.
- **Logistics Tracker Agent**: Tracks shipments and provides estimated times of arrival (ETAs).

These agents interact with mock external systems (ERP, Supplier Portal, Shipping API) to simulate real-world supply chain operations. Human-in-the-loop intervention is simulated for critical decisions like reorder approvals.

## Components

### `agents/`
Contains the Python implementations of the specialized agents and the supervisor agent.
- `specialized_agents.py`: Defines `InventoryAnalystAgent`, `ProcurementAgent`, and `LogisticsTrackerAgent`.
- `supervisor.py`: Defines the `SupplyChainOrchestrator` which orchestrates the specialized agents.

### `tools/`
Contains mock implementations of external systems that the agents interact with.
- `mock_systems.py`: Provides `ERPSystem`, `SupplierPortal`, and `ShippingAPI` classes.

### `config/`
Contains configuration files, including a sample Kore.ai platform configuration.
- `kore_ai_config.json`: A JSON file outlining the agent definitions, orchestration pattern, and tool configurations as they would be set up in the Kore.ai XO Platform.

### `main.py`
The entry point for the simulation, demonstrating the flow of interaction between the orchestrator and specialized agents.

## How to Run the Simulation
1. Navigate to the project directory:
   ```bash
   cd smart_supply_chain
   ```
2. Run the main simulation script:
   ```bash
   python3 main.py
   ```

## Expected Output
The simulation will output messages indicating the orchestrator's actions, such as detecting low stock, requesting quotes, placing orders, and tracking shipments.

## Kore.ai Integration (Conceptual)
While this project provides a Python-based simulation, the `config/kore_ai_config.json` file illustrates how this multi-agent system would be configured within the Kore.ai XO Platform. Each Python agent would correspond to a Kore.ai agent, and the mock system functions would be exposed as tools (e.g., REST APIs) within the platform.

## Future Enhancements
- Integration with actual ERP, CRM, and logistics systems.
- Advanced AI models for demand forecasting and predictive analytics.
- Dynamic human-in-the-loop approvals via Kore.ai's platform features.
- Implementation of Adaptive Agent Network or Custom patterns for different use cases.
