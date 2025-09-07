from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

from prompt_to_json import PromptJSON, PromptToJSON


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.output_text = text


@pytest.fixture
def converter() -> PromptToJSON:
    return PromptToJSON(api_key="test")


def run_mocked(converter: PromptToJSON, text: str, prompt: str) -> Dict[str, Any]:
    converter.client.responses.create = MagicMock(return_value=FakeResponse(text))
    return converter.convert(prompt)


def test_schema_validation(converter: PromptToJSON) -> None:
    result = run_mocked(
        converter, '{"task":"summarize","input_data":{"text":"hi"}}', "Summarize"
    )
    PromptJSON.model_validate(result)


@pytest.mark.parametrize(
    "prompt, mocked",
    [
        ("Do it", '{"task":"clarify","input_data":{"text":"Do it"}}'),
        (
            "¿Puedes resumir esto?",
            '{"task":"summarize","input_data":{"language":"es"}}',
        ),
        ("Long" + "x" * 1000, '{"task":"process","input_data":{"length":1000}}'),
        (
            "Broken",
            'Note: {"task":"summarize","input_data":{}} trailing',
        ),
    ],
)
def test_edge_prompts(converter: PromptToJSON, prompt: str, mocked: str) -> None:
    result = run_mocked(converter, mocked, prompt)
    PromptJSON.model_validate(result)
    assert result["task"]
