import json
import os
import re
from typing import Dict, Optional, List
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
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY or pass api_key")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def convert(self, prompt: str) -> Dict:
        """
        Convert natural language prompt to structured JSON
        """
        system_instructions = """You are an expert at converting natural language prompts into structured JSON.
Analyze the prompt and extract:
- task: The main action/verb (summarize, extract, generate, analyze, etc.)
- input_data: What data/content to process
- output_format: Expected format and structure of output. dont give json format by default. it should text . dont mention any format until specifed
- constraints: Any limitations (length, count, style, etc.)
- context: Background information or purpose
- config: Settings like tone, approach, style

Return ONLY valid JSON, with no markdown formatting or explanation.
"""

        try:
            # Use the Responses API (not chat.completions)
            response = self.client.responses.create(
                model=self.model,
                instructions=system_instructions,   # system prompt goes here
                input=prompt,                       # user prompt as simple text
                max_output_tokens=500,              # responses API parameter
                temperature=0.1,
            )

            # responses API offers direct text output
            content = response.output_text or ""

            # Try to parse JSON directly
            result = json.loads(content)
            result["note"] = (
                "This JSON is only a task specification. "
                "Do not return the actual task output in JSON unless explicitly asked."
            )
            return result

        except json.JSONDecodeError:
            # Try to extract JSON if the model added extra text (shouldn't, but be safe)
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
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

    def convert_batch(self, prompts: List[str]) -> List[Dict]:
        """Convert multiple prompts to structured JSON"""
        return [self.convert(p) for p in prompts]
