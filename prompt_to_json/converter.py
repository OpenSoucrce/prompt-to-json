import json
import os
import re
from typing import Any, Dict, List, Optional, cast

from openai import OpenAI


class PromptToJSON:
    """Convert natural language prompts to structured JSON using OpenAI Responses API"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4.1"):
        """
        Initialize with OpenAI API key

        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
            model: OpenAI model to use (e.g., gpt-4.1, gpt-4o, gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY or pass api_key"
            )

        self.client: Any = OpenAI(api_key=self.api_key)
        self.model = model

    def convert(self, prompt: str) -> Dict[str, Any]:
        """Convert natural language prompt to structured JSON"""
        system_instructions = (
            "You convert natural language prompts into structured JSON.\n"
            "Analyze the prompt and extract:\n"
            "- task: main action or verb\n"
            "- input_data: data or content to process\n"
            "- output_format: expected output structure if specified\n"
            "- constraints: limitations such as length or count\n"
            "- context: background information or purpose\n"
            "- config: settings like tone or approach\n\n"
            "Respond with ONLY valid JSON."
        )

        try:
            # Use the Responses API (not chat.completions)
            response = self.client.responses.create(
                model=self.model,
                instructions=system_instructions,  # system prompt goes here
                input=prompt,  # user prompt as simple text
                max_output_tokens=500,  # responses API parameter
                temperature=0.1,
            )

            # responses API offers direct text output
            content = response.output_text or ""

            # Try to parse JSON directly
            return cast(Dict[str, Any], json.loads(content))

        except json.JSONDecodeError:
            # Try to extract JSON if the model added extra text (shouldn't, but be safe)
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                try:
                    return cast(Dict[str, Any], json.loads(match.group()))
                except json.JSONDecodeError:
                    pass

            # Fallback: return basic structure
            return {
                "task": "process",
                "input_data": {"prompt": prompt},
                "error": "Failed to parse response",
            }

        except Exception as e:
            # Handle API errors
            return {
                "task": "process",
                "input_data": {"prompt": prompt},
                "error": str(e),
            }

    def convert_batch(self, prompts: List[str]) -> List[Dict[str, Any]]:
        """Convert multiple prompts to structured JSON"""
        return [self.convert(p) for p in prompts]
