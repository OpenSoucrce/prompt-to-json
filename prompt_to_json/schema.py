from typing import Any, Dict, Optional

from pydantic import BaseModel


class PromptJSON(BaseModel):
    """Schema for structured prompt representation."""

    task: str
    input_data: Any
    output_format: Optional[Any] = None
    constraints: Optional[Any] = None
    context: Optional[Any] = None
    config: Optional[Any] = None

    @classmethod
    def to_schema(cls) -> Dict[str, Any]:
        """Return the JSON schema for the model."""
        return cls.model_json_schema()
