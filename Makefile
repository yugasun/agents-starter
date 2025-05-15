
appdir := ${PWD}/myapp

install:
	@echo "Installing dependencies..."
	@uv sync --dev

# 用法示例: make run-agentsdk e=quickstart
run-agentsdk:
	@uv run -m agents_starter.cli --framework agentsdk --example ${e}

# 用法示例: make run-autogen e=quickstart
run-autogen:
	@uv run -m agents_starter.cli --framework autogen --example ${e}

# 用法示例: make run-crewai e=quickstart
run-crewai:
	@uv run -m agents_starter.cli --framework crewai --example ${e}

run-autogenstudio:
	autogenstudio ui --host 0.0.0.0 --port 8080 --appdir ${appdir}
