# Virt-Language Model Agents for OpenShift and Virtualization

## Overview

This repository contains a set of Python notebooks and tools designed to build AI-powered agents that interact with **OpenShift** and virtualization environments. These agents can perform tasks such as listing virtual machines (VMs), creating migration plans, interacting with OpenShift, and leveraging large language models (LLMs) to drive decision-making processes.

The notebooks demonstrate how to implement AI agents using models like **Llama 3** and workflow orchestration through **LangChain** and **LangGraph**. They integrate with tools such as **OpenShift**, virtualization platforms, and persistent state management using SQLite.

---

## Directory Structure

```bash
.
├── 01-agent.ipynb                # Initial setup of AI-powered agent
├── 02-planning.ipynb             # AI agent planning tasks
├── 03-planning-memory.ipynb      # AI agent planning with memory integration
├── 04-react-agent-llama3.ipynb   # ReAct agent implementation with Llama 3
├── 05-react-agent-llama31.ipynb  # Extended version of the ReAct agent with Llama 3
├── 06-virt-agent.ipynb           # Virtualization agent for interacting with VMs
├── 07-ocp-agent.ipynb            # OpenShift agent for handling OCP workflows
├── TODO.md                       # Project to-do list
├── agent                         # Agent source code
│   └── react_agent.py            # ReAct agent logic
├── agents.yaml                   # Configuration file for agents
├── data                          # Directory for storing JSON outputs
│   └── json_vms_output.json      # Example output: VM listing
├── images
├── prompt                        # Prompts used to interact with LLMs
│   └── react_prompt.py           # Prompt definitions for ReAct agent
├── schemas                       # JSON schemas for validation
│   └── vms_schema.py             # Schema for validating VM outputs
├── services                      # Service layer to interact with OpenShift and models
│   ├── model_service.py          # Service to interact with the language model
│   └── openshift_service.py      # Service for interacting with OpenShift
├── state                         # State management for the agent workflows
│   └── agent_graph.py            # State graph for task orchestration
└── utils                         # Helper functions and utilities
    └── general
        └── helpers.py            # General utility functions
```

## Notebook Descriptions

This project contains several Jupyter notebooks, each focusing on different aspects of AI-powered agents and their interaction with virtualization platforms and OpenShift environments.

### 1. `01-agent.ipynb` - **Initial Agent Setup**

This notebook introduces the basic setup of the AI-powered agent. It demonstrates how to initialize the agent, load necessary configurations, and establish connections to external services such as OpenShift and the language model.

### 2. `02-planning.ipynb` - **Planning with the Agent**

This notebook explores how the AI agent can assist in planning workflows, such as migration plans for virtual machines. The agent processes user queries and executes tasks like creating migration plans for specific VMs.

**Key Features:**

- Using the agent to create migration plans.
- Example query: *"Create a migration plan for the VM named 'database'."*
- Interaction with virtualization environments to retrieve VM details.

### 3. `03-planning-memory.ipynb` - **Planning with Memory Integration**

In this notebook, the agent is enhanced with memory capabilities. The agent can now remember prior interactions, making it more context-aware during extended sessions. This is useful when working with complex workflows that require multi-step interactions.

**Key Features:**

- Adding memory to the agent using `langchain`.
- Storing and retrieving previous states for enhanced decision-making.
- Example scenarios where the agent retains context across tasks.

### 4. `04-react-agent-llama3.ipynb` - **ReAct Agent with Llama 3**

This notebook introduces the **ReAct agent** powered by the Llama 3 language model. The ReAct framework allows the agent to respond and act on the user’s input in a more dynamic and intelligent manner. The agent can now execute multiple tasks, make decisions, and provide feedback on workflows.

**Key Features:**

- ReAct agent implementation using Llama 3.
- Executing tasks based on natural language input.
- Example queries for task execution and feedback generation.

### 5. `05-react-agent-llama31.ipynb` - **Extended ReAct Agent with Llama 3.1**

An extension of the ReAct agent, this notebook demonstrates a more advanced use case of the agent with Llama 3.1. It adds more functionality, handles more complex workflows, and integrates additional custom tools.

**Key Features:**

- Advanced task execution using Llama 3.1.
- Handling complex, multi-step workflows in the agent.
- Enhanced error handling and response generation.

### 6. `06-virt-agent.ipynb` - **Virtualization Agent**

This notebook focuses on the agent’s interaction with virtualization platforms, such as VMware vSphere. The agent can list all virtual machines (VMs), retrieve details about each VM, and create migration plans.

**Key Features:**

- Connecting to virtualization platforms (e.g., VMware vSphere).
- Listing and managing VMs via the agent.
- Creating migration plans for VMs using a virtualization provider.

### 7. `07-ocp-agent.ipynb` - **OpenShift Agent**

This notebook demonstrates how the AI agent can interact with **OpenShift** to manage various OpenShift resources such as pods, deployments, and nodes. It integrates directly with the OpenShift API and handles tasks such as creating or modifying resources within an OpenShift environment.

**Key Features:**

- Interaction with OpenShift resources (e.g., pods, deployments).
- Managing OpenShift workflows via the agent.
- Example queries: Listing pods, creating deployments, or managing resources.

## Contributing

Contributions are welcome! If you have suggestions, improvements, or new ideas, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Special thanks to the developers and community behind LangChain and the LLM models.
All contributors and users who provided feedback and improvements.

## Contact

For any questions or comments, please reach out via <gsampaio@redhat.com>