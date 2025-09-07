# prompt-to-json

[![PyPI version](https://img.shields.io/pypi/v/prompt-to-json)](https://pypi.org/project/prompt-to-json/)
[![Build Status](https://github.com/prompt-to-json/prompt-to-json/actions/workflows/ci.yml/badge.svg)](https://github.com/prompt-to-json/prompt-to-json/actions/workflows/ci.yml)
[![Coverage Status](https://img.shields.io/codecov/c/github/prompt-to-json/prompt-to-json)](https://codecov.io/gh/prompt-to-json/prompt-to-json)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/prompt-to-json.svg)](https://pypi.org/project/prompt-to-json/)

Convert natural language prompts to structured JSON using OpenAI's GPT models.

## Installation

```bash
pip install prompt-to-json
```

## Quick Start

```python
from prompt_to_json import PromptToJSON

# Initialize with API key
converter = PromptToJSON(api_key="sk-...")  # or set OPENAI_API_KEY env var

# Convert natural language to structured JSON
prompt = "Summarize this article in 3 bullet points professionally"
result = converter.convert(prompt)

print(result)
# Output:
# {
#   "task": "summarize",
#   "input_data": {"type": "article", "source": "provided"},
#   "output_format": {"format": "bullet_points", "count": 3},
#   "constraints": {"max_points": 3},
#   "config": {"tone": "professional"}
# }
```

## Features

- 🎯 **Simple API** - Just one method: `convert()`
- 🧠 **Intelligent Parsing** - Uses GPT to understand intent and structure
- 📦 **Structured Output** - Returns clean JSON ready for downstream processing
- 🔄 **Batch Processing** - Convert multiple prompts at once
- ⚡ **Production Ready** - Error handling and fallbacks included

## Usage

### Basic Usage

```python
from prompt_to_json import PromptToJSON

converter = PromptToJSON()

# Simple prompt
result = converter.convert("Extract key points from this text")
```

### Batch Processing

```python
prompts = [
    "Summarize this article",
    "Translate to Spanish",
    "Extract data points"
]

results = converter.convert_batch(prompts)
```

### Using Different Models

```python
# Use GPT-4.1 for better accuracy (default)
converter = PromptToJSON()

# Use GPT-3.5 Turbo for speed and cost efficiency
converter = PromptToJSON(model="gpt-3.5-turbo")
```

## Output Structure

The converter extracts and structures:
- **task** - Main action/verb (summarize, extract, generate, etc.)
- **input_data** - Data or content to process
- **output_format** - Expected format and structure
- **constraints** - Limitations (length, count, style, etc.)
- **context** - Background information or purpose
- **config** - Settings like tone, approach, style

## Examples

```python
# Content Generation
prompt = "Write a marketing email for our new AI product"
# Returns: {"task": "generate", "input_data": {"type": "marketing_email"}, ...}

# Data Extraction
prompt = "Extract all dates and amounts from these invoices"
# Returns: {"task": "extract", "input_data": {"type": "invoices"}, ...}

# Analysis
prompt = "Analyze customer feedback and identify top complaints"
# Returns: {"task": "analyze", "input_data": {"type": "customer_feedback"}, ...}
```

## Advanced Usage

### Error Handling, Rate Limits, and Retries

```python
from prompt_to_json import PromptToJSON
from openai import OpenAI, OpenAIError
from time import sleep

converter = PromptToJSON()

for attempt in range(3):
    try:
        result = converter.convert("Summarize this article")
        break
    except OpenAIError as e:
        # basic exponential backoff on failure or rate limit
        sleep(2 ** attempt)
else:
    raise RuntimeError("Request failed after retries")

print(result)
```

### Timeout Configuration

```python
converter = PromptToJSON()
# underlying OpenAI client supports a timeout parameter
converter.client = OpenAI(api_key=converter.api_key, timeout=30)
```

### JSON Schema and Validation

```python
from prompt_to_json import PromptJSON

result = converter.convert("Extract key facts")
PromptJSON.model_validate(result)  # raises if the shape is wrong
schema = PromptJSON.to_schema()
```

### Custom Models and Prompts

```python
# Use a different model and a deterministic temperature
converter = PromptToJSON(model="gpt-4o-mini")

# Modify system instructions or add few-shot examples
custom = PromptToJSON(model="gpt-4o-mini")
custom_prompt = "You are a precise JSON formatter."
response = custom.client.responses.create(
    model=custom.model,
    instructions=custom_prompt,
    input="Translate to French",
    temperature=0,
)
```

## Requirements

- Python 3.6+
- OpenAI API key

## Environment Setup

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

## License

MIT

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Support

For issues or questions, please open an issue on GitHub.