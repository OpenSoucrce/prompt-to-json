from prompt_to_json import PromptToJSON
import json


def main():
    # Initialize converter (uses OPENAI_API_KEY env variable)
    converter = PromptToJSON()

    # Example prompts
    prompts = [
        "Summarize this article in 3 bullet points with professional tone",
        "Extract all emails and phone numbers from this text and return as JSON",
        "Compare these two products and show pros and cons in a table",
        "Generate a creative product description for a smartphone targeting Gen Z",
        "Analyze sales data from Q3 and identify top 3 trends",
        "Translate this document to French maintaining formal tone",
        "Create a step-by-step tutorial for beginners on how to use Python",
        "Classify customer reviews into positive, negative, and neutral"
    ]

    print("Converting Natural Language Prompts to Structured JSON\n")
    print("=" * 60)

    for prompt in prompts:
        print(f"\n📝 Prompt: {prompt}")
        print("-" * 40)

        result = converter.convert(prompt)
        print("📊 Structured JSON:")
        print(json.dumps(result, indent=2))
        print("=" * 60)


if __name__ == "__main__":
    main()