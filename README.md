# codex_testing

This repository showcases **AgentLogOntology**, a flexible object/action data
model for logging autonomous agent executions. The ontology distinguishes
between persistent objects (agents, observations, actions, etc.) and the
actions that mutate them. A parser demonstrates converting OpenAI
``agent-traces`` JSON into ontology objects, and a simple Tkinter GUI lets you
inspect and edit log state.

## Usage

1. Ensure Python with Tkinter is available.
2. Run ``python demo.py`` to load ``sample_agent_trace.json`` and open the GUI.
