"""Core marketing agent powered by Claude."""

from anthropic import Anthropic

from .brand import brand_context_block, load_brand_config
from .prompts import build_system_prompt
from .tools.definitions import TOOL_SCHEMAS, dispatch_tool


class MarketingAgent:
    """An agentic loop that acts as a Senior Marketing Manager."""

    def __init__(self, config_path=None, model="claude-sonnet-4-20250514"):
        self.client = Anthropic()
        self.model = model
        self.config = load_brand_config(config_path)
        brand_context = brand_context_block(self.config)
        self.system_prompt = build_system_prompt(brand_context)
        self.messages: list[dict] = []

    def chat(self, user_message: str) -> str:
        """Send a user message and run the agent loop until a final text response."""
        self.messages.append({"role": "user", "content": user_message})

        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=TOOL_SCHEMAS,
                messages=self.messages,
            )

            # Collect the full assistant turn
            self.messages.append({"role": "assistant", "content": response.content})

            # If the model stopped without requesting tools, return text
            if response.stop_reason == "end_turn":
                return self._extract_text(response.content)

            # Process any tool calls
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = dispatch_tool(block.name, block.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result,
                            }
                        )
                self.messages.append({"role": "user", "content": tool_results})
            else:
                # Unexpected stop reason — return whatever text we have
                return self._extract_text(response.content)

    def reset(self):
        """Clear conversation history to start a fresh session."""
        self.messages = []

    @staticmethod
    def _extract_text(content_blocks) -> str:
        """Pull text out of the response content blocks."""
        parts = []
        for block in content_blocks:
            if hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts)
