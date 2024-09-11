# Virt-Language Model Agents for OpenShift and Virtualization

## Overview

This repository contains a set of Python notebooks and tools designed to build AI-powered agents that interact with **OpenShift** and virtualization environments. These agents can perform tasks such as listing virtual machines (VMs), creating migration plans, interacting with OpenShift, and leveraging large language models (LLMs) to drive decision-making processes.

The notebooks demonstrate how to implement AI agents using models like **Llama 3** and workflow orchestration through **LangChain** and **LangGraph**. They integrate with tools such as **OpenShift**, virtualization platforms, and persistent state management using SQLite.

---

## Directory Structure

```bash
.
├── 01-llm.ipynb                # Introduction to LLMs (Llama 3)
├── 02-react-prompting.ipynb    # Introduction to ReAct Prompting with Llama 3
├── 03-agent.ipynb              # Initial setup of AI-powered agent
├── 04-multi-agent.ipynb        # Multi-Agent orchestration using LangChain
├── 11-planning.ipynb           # AI agent task planning
├── 12-virt-agent.ipynb         # Virtualization agent interacting with VMs
├── 13-ocp-agent.ipynb          # OpenShift agent for handling OCP workflows
├── agent                       # Agent source code
│   └── base_agent.py           # Base agent logic
│   └── react_agent.py          # ReAct agent logic
├── agents.yaml                 # Configuration file for agents
├── images                      # Directory for storing images
├── prompt                      # Prompts used to interact with LLMs
│   └── react_prompt.py         # Prompt definitions for ReAct logic
│   └── base_prompt.py          # Prompt definitions for Base agent
├── schemas                     # JSON schemas for validation
│   └── vms_schema.py           # Schema for validating planner outputs
│   └── vm_schema.py            # Schema for validating VM outputs
├── services                    # Service layer for OpenShift and models
│   ├── model_service.py        # Service for interacting with the language model
│   └── openshift_service.py    # Service for interacting with OpenShift
├── state                       # State management for agent workflows
│   └── agent_graph.py          # State graph for task orchestration
└── utils                       # Helper functions and utilities
    └── general
        └── helpers.py          # General utility functions
```

## First Module

This module contains several Jupyter notebooks, each focusing on the fundamentals of LLMs, ReAct prompting, and AI-powered agents. The notebooks guide you through setting up and understanding key concepts, such as using LLMs, implementing reasoning-based workflows, and integrating various tools into agent-driven tasks.

### 1. `01-llm.ipynb` - **Introduction to LLMs (Llama 3)**

This notebook introduces the concept of Large Language Models (LLMs) using Llama 3. It explains how LLMs can be used for tasks like question answering and text generation.

### 2. `02-react-prompting.ipynb` - **Introduction to ReAct Prompting**

This notebook introduces the ReAct (Reasoning + Acting) prompting framework with Llama 3. It demonstrates how ReAct enables models to reason through problems, take actions, and adjust based on observations, creating a more dynamic problem-solving loop.

### 3. `03-agent.ipynb` - **Initial Agent Setup**

This notebook covers the basic setup of an AI-powered agent. It demonstrates how to initialize the agent, load configurations, and connect to external services like OpenShift and the language model.

### 4. `04-react-agent.ipynb` - **ReAct Agent with Llama 3**

This notebook introduces the **ReAct agent** powered by the Llama 3 language model. The ReAct framework allows the agent to respond and act on the user’s input in a more dynamic and intelligent manner. The agent can now execute multiple tasks, make decisions, and provide feedback on workflows.

### 5. `06-multi-agent.ipynb` - **Multi-Agent Orchestration using LangChain**

This notebook demonstrates how to orchestrate multiple agents using LangChain, allowing agents to collaborate on tasks to achieve complex goals.

## Second Module

This module delves into more advanced topics, focusing on AI agents’ capabilities in task planning, virtualization environments, and integration with OpenShift. The notebooks demonstrate how agents can interact with external platforms and orchestrate complex workflows.

### 1. `11-planning.ipynb` - **AI Agent Task Planning**

This notebook explores how AI agents can plan tasks using structured processes and tools. It focuses on task breakdown and execution.

### 2. `12-virt-agent.ipynb` - **Virtualization Agent**

This notebook focuses on the agent’s interaction with virtualization platforms, such as VMware vSphere. The agent can list all virtual machines (VMs), retrieve details about each VM, and create migration plans.

### 3. `13-ocp-agent.ipynb` - **OpenShift Agent**

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
