"""ABCs for agentic Tools.

New tools are added by implementing this interface and registering the tool with the agent.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Tool(ABC):
    name: str
    description: str
    parameters: dict

    @abstractmethod
    def run(self, **kwargs) -> str:
        """Execute the tool and return a text result for the model."""

    def spec(self) -> dict:
        """OpenAI function-calling schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
