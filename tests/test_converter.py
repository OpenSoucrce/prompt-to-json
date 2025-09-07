import json
from prompt_to_json import PromptToJSON


def test_basic_conversion():
    """Test basic prompt conversion"""
    converter = PromptToJSON()

    result = converter.convert("Summarize this email in 3 bullet points")

    assert "task" in result
    assert result["task"] == "summarize"
    print("✓ Basic conversion test passed")
    print(json.dumps(result, indent=2))


def test_complex_conversion():
    """Test complex prompt conversion"""
    converter = PromptToJSON()

    prompt = """Extract all product names and prices from this e-commerce page,
    organize them in a table format sorted by price,
    and highlight items over $100"""

    result = converter.convert(prompt)

    assert "task" in result
    assert "output_format" in result or "config" in result
    print("✓ Complex conversion test passed")
    print(json.dumps(result, indent=2))


def test_batch_conversion():
    """Test batch prompt conversion"""
    converter = PromptToJSON()

    prompts = [
        "Generate a marketing email for our new product",
        "Analyze customer feedback and identify main complaints",
        "Translate this document to Spanish"
    ]

    results = converter.convert_batch(prompts)

    assert len(results) == 3
    assert all("task" in r for r in results)
    print("✓ Batch conversion test passed")
    for i, result in enumerate(results):
        print(f"\nPrompt {i+1}:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    print("Running tests...\n")
    test_basic_conversion()
    print("\n" + "="*50 + "\n")
    test_complex_conversion()
    print("\n" + "="*50 + "\n")
    test_batch_conversion()
    print("\n✅ All tests passed!")