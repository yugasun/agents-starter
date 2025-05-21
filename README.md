# Agents Starter

A comprehensive starter kit and guide for working with various AI agent frameworks, designed to help developers quickly set up and experiment with different agent architectures.

## Overview

Agents Starter provides a unified interface for working with multiple popular agent frameworks including:

- **AutoGen**: For building conversational agents with LLMs
- **CrewAI**: For creating AI agent teams that can collaborate
- **Google ADK**: For developing agents using Google's Agent Development Kit
- **LangGraph**: For creating complex agent workflows and graphs

This toolkit simplifies the process of getting started with these frameworks by providing consistent CLI interfaces, configuration management, and examples.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agents-starter.git
cd agents-starter

# Install dependencies
make install
```

## Project Structure

```bash
agents_starter/
├── agentsdk/            # Core SDK for all agent frameworks
├── autogen/             # AutoGen framework integration
├── crewai/              # CrewAI framework integration
├── googleadk/           # Google ADK framework integration
├── langgraph/           # LangGraph framework integration
└── settings/            # Configuration settings
```

## Configuration

The project uses a centralized configuration system located in the `settings` directory:

- settings.example.toml: Example configuration file
- settings.toml: Your personalized settings (create this by copying the example)

Configure your API keys, model preferences, and other settings in the settings.toml file:

```toml
[openai]
api_key = ""
base_url = "https://api.openai.com/v1"
model = "gpt-4o"
provider = "openai"
promtp = "You are a helpful assistant. Please answer the following question: "


[serper]
api_key = "xxx"

[langsmith]
tracing = "true"
endpoint = "https://api.smith.langchain.com"
api_key = "xxx"
project = "default"

[tavily]
api_key = "tvly-xxxx"
```

## Usage

### CLI Commands

Each framework comes with its own CLI commands for easy usage:

```bash
# AutoGen
cd agents_starter/autogen
uv sync
agst run quickstart

# CrewAI
cd agents_starter/crewai
uv sync
agst run quickstart

# Google ADK
cd agents_starter/googleadk
uv sync
agst run quickstart

# LangGraph
cd agents_starter/langgraph
uv sync
agst run quickstart
```

### Examples

Each framework directory contains example implementations in their respective examples folders to help you get started.

## Framework Guides

### AutoGen

AutoGen provides a framework for building conversational agents powered by LLMs. Key features include:

- Multi-agent conversations
- Human-in-the-loop capabilities
- Tool usage by agents

### CrewAI

CrewAI allows you to create collaborative agent teams that work together to accomplish tasks:

- Agent role definition
- Task assignment
- Team collaboration

### Google ADK (Agent Development Kit)

Google's ADK offers tools for building agents that can:

- Execute complex workflows
- Integrate with Google services
- Handle multi-step reasoning

### LangGraph

LangGraph enables the creation of stateful, multi-agent systems as computation graphs:

- Define agent workflows as graphs
- Create complex decision trees
- Visualize agent interactions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the license included in the repository.
