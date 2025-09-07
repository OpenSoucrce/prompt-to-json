from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prompt-to-json",
    version="0.1.0",
    author="Aadarsh Gaikwad",
    author_email="aadarshgaikwad04@example.com",
    description="Convert natural language prompts to structured JSON using OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenSoucrce/prompt-to-json",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "openai>=1.0.0",
    ],
)
