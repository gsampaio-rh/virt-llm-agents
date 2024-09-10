# Virt-Language Model Agents for OpenShift and Virtualization

## Overview

This repository contains a set of Python notebooks and tools designed to build AI-powered agents that interact with **OpenShift** and virtualization environments. These agents can perform tasks such as listing virtual machines (VMs), creating migration plans, interacting with OpenShift, and leveraging large language models (LLMs) to drive decision-making processes.

The notebooks demonstrate how to implement AI agents using models like **Llama 3** and workflow orchestration through **LangChain** and **LangGraph**. They integrate with tools such as **OpenShift**, virtualization platforms, and persistent state management using SQLite.

---

## Directory Structure

```bash
.
├── 01-agent.ipynb                # Initial setup of AI-powered agent├── 01-llm.ipynb                # Introduction to LLMs (Llama 3)
├── 02-agent.ipynb             # Initial setup of AI-powered agent
├── 03-react-agent.ipynb      # ReAct agent implementation with Llama 3
├── 04-multi-agent.ipynb      # Multi-Agent orchestration using LangChain├── 02-planning.ipynb             # AI agent planning tasks
├── 10-planning-memory.ipynb      # AI agent planning with memory integration
├── 11-virt-agent.ipynb           # Virtualization agent for interacting with VMs
├── 12-ocp-agent.ipynb            # OpenShift agent for handling OCP workflows
├── TODO.md                       # Project to-do list
├── agent                         # Agent source code
│   └── base_agent.py             # Base agent
│   └── react_agent.py            # ReAct agent logic
├── agents.yaml                   # Configuration file for agents
├── images
├── prompt                        # Prompts used to interact with LLMs
│   └── react_prompt.py           # Prompt definitions for ReAct agent
│   └── base_prompt.py            # Prompt definitions for Base agent
├── schemas                       # JSON schemas for validation
│   └── vms_schema.py             # Schema for validating planner outputs
│   └── vm_schema.py              # Schema for validating VM outputs
│   └── vms_schema.py             # Schema for validating VMs outputs
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

### 1. `01-llm.ipynb` - **Introduction to LLMs (Llama 3)**

This notebook introduces the concept of Large Language Models (LLMs) using Llama 3. It demonstrates how to use LLMs for natural language processing tasks, such as answering questions and generating text.

### 2. `02-agent.ipynb` - **Initial Agent Setup**

This notebook introduces the basic setup of the AI-powered agent. It demonstrates how to initialize the agent, load necessary configurations, and establish connections to external services such as OpenShift and the language model.

### 3. `03-react-agent.ipynb` - **ReAct Agent with Llama 3**

This notebook introduces the **ReAct agent** powered by the Llama 3 language model. The ReAct framework allows the agent to respond and act on the user’s input in a more dynamic and intelligent manner. The agent can now execute multiple tasks, make decisions, and provide feedback on workflows.

### 4. `04-multi-agent.ipynb` - **Multi-Agent Orchestration using LangChain**

This notebook demonstrates how to use LangChain for multi-agent orchestration. It shows how to create a workflow that involves multiple agents working together to achieve a common goal.

### 5. `10-planning-memory.ipynb` - **AI Agent Planning Tasks with Memory Integration**

This notebook explores how the AI agent can assist in planning workflows, such as migration plans for virtual machines. The agent processes user queries and executes tasks like creating migration plans for specific VMs with memory integration.

### 6. `11-virt-agent.ipynb` - **Virtualization Agent**

This notebook focuses on the agent’s interaction with virtualization platforms, such as VMware vSphere. The agent can list all virtual machines (VMs), retrieve details about each VM, and create migration plans.

### 7. `12-ocp-agent.ipynb` - **OpenShift Agent**

This notebook demonstrates how the AI agent can interact with **OpenShift** to manage various OpenShift resources such as pods, deployments, and nodes. It shows how to use the OpenShift agent for handling OCP workflows.

## Code and Configurations

The `agent`, `services`, `state`, and `utils` directories contain code and configurations related to the AI-powered agents, services, state management, and utility functions.

## Data and Images

The `data` directory contains sample data used in the notebooks, while the `images` directory contains images used for documentation and illustration purposes.

## Contributing

Contributions are welcome! If you have suggestions, improvements, or new ideas, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Special thanks to the developers and community behind LangChain and the LLM models.
All contributors and users who provided feedback and improvements.

## Contact

For any questions or comments, please reach out via <gsampaio@redhat.com>

Let me know if this looks good to you! I'll be happy to make any further adjustments.
