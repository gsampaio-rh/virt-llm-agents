# AI-Powered Agents for OpenShift and Virtualization

## Overview

Welcome to this collection of Python notebooks and tools designed to build AI-powered agents that interact with **OpenShift** and virtualization environments. These agents can:

- List virtual machines (VMs)
- Create migration plans
- Interact with OpenShift
- Leverage Large Language Models (LLMs) for decision-making

The notebooks demonstrate how to implement AI agents using models like **Llama 3.1** and orchestrate workflows using **LangChain** and **LangGraph**. They integrate with tools such as OpenShift, virtualization platforms, and use SQLite for state management.

---

## Prerequisites

To get the most out of these notebooks, please ensure you have the following installed and set up:

- **Ollama**: A local LLM server for running language models. Download it from [ollama.com/download](https://ollama.com/download).
- **LLM Models**: We use models like `llama3.1:latest` and `llama3.1:8b-instruct-fp16`. You can download these models directly from Meta or using Ollama.

### Instructions

- **Downloading Ollama**: [Download Ollama](https://ollama.com/download) and follow the installation instructions.
- **Models We Use**:
  - `llama3.1:latest`
  - `llama3.1:8b-instruct-fp16`
- **Downloading Models**:
  - **Direct Download from Meta**: Visit [llama.com/llama-downloads](https://www.llama.com/llama-downloads) to download models directly.
  - **Using Ollama**: You can download models using Ollama with the command:

  ```bash
  ollama pull llama3.1:latest
  ollama pull llama3.1:8b-instruct-fp16
  ```

---

## Modules

### Module 1: Introduction to LLMs and ReAct Prompting

#### 1. `11-llm.ipynb` - Introduction to LLMs (Llama 3.1)

Learn about Large Language Models using Llama 3.1. Understand how LLMs can be used for tasks like question answering and text generation.

#### 2. `12-tools.ipynb` - Introduction to Tool Calling

Discover how LLMs can be extended using tools to solve tasks requiring real-time information or specialized capabilities.

#### 3. `13-react-prompting.ipynb` - Introduction to ReAct Prompting

Explore the ReAct (Reasoning + Acting) prompting framework. See how ReAct enables models to reason through problems, take actions, and adjust based on observations, creating a dynamic problem-solving loop.

### Module 2: Agent-Based Interactions

#### 1. `21-agent.ipynb` - Initial Agent Setup

Set up an AI-powered agent. Learn how to initialize the agent, load configurations, and connect to external services like OpenShift and the language model.

#### 2. `22-react-agent.ipynb` - ReAct Agent with Llama 3.1

Introduce the ReAct agent powered by Llama 3.1. See how the agent can execute multiple tasks, make decisions, and provide workflow feedback.

#### 3. `23-multi-agent.ipynb` - Multi-Agent Orchestration using LangChain

Learn how to orchestrate multiple agents using LangChain, allowing them to collaborate to achieve complex goals.

### Module 3: Advanced Agent Applications

#### 1. `31-planning.ipynb` - AI Agent Task Planning

Explore how AI agents can plan tasks using structured processes and tools, focusing on task breakdown and execution.

#### 2. `32-virt-agent.ipynb` - Virtualization Agent

See how agents interact with virtualization platforms like VMware vSphere. Agents can list VMs, retrieve VM details, and create migration plans.

#### 3. `33-ocp-agent.ipynb` - OpenShift Agent

Discover how AI agents interact with OpenShift to manage resources such as pods, deployments, and nodes. Learn to use the OpenShift agent for handling workflows.

### Module 4: Migration Workflows

#### 1. `41-migration.ipynb` - Migration Multi-Agent Workflow

Dive into creating a powerful migration workflow agent that seamlessly integrates virtualization environments with OpenShift.

---

## Code and Configurations

The following directories contain code and configurations for the AI agents, services, state management, and utilities:

- `agent`
- `prompt`
- `schemas`
- `services`
- `state`
- `utils`

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

Special thanks to the developers and community behind LangChain, LangGraph, and LLM models.

---

## Contact

For questions or comments, please reach out via email: [gsampaio@redhat.com](mailto:gsampaio@redhat.com)

---

Let me know if this looks good to you! I'm happy to make further adjustments.
