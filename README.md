# Local AI Assistant

A powerful local AI tool that wraps the Anthropic API to assist developers with coding tasks. It features both a Command Line Interface (CLI) and a beautiful Web User Interface (UI) built with Streamlit.

## Features

- **Chat with Codebase**: Ask questions about your project, providing relevant file context.
- **Summarize Files**: Get concise summaries of text or code files.
- **Refactor Code**: Improve code readability, performance, and maintainability.
- **Generate Tests**: Automatically generate unit tests for your code.
- **Explain Errors**: Get explanations and fixes for error logs.

## Prerequisites

- **Python 3.8+**
- **Anthropic API Key**: You need an API key from [Anthropic](https://console.anthropic.com/).

## Installation

### macOS (and Linux)

1.  **Install Python** (if not already installed):
    ```bash
    brew install python
    ```

2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/local-ai-assistant.git
    cd local-ai-assistant
    ```

3.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set your API Key**:
    You can set it as an environment variable (recommended) or enter it in the UI.
    ```bash
    export ANTHROPIC_API_KEY="your-api-key-here"
    ```

## Usage

### Web UI (Recommended)

The Web UI provides a user-friendly interface for all features.

1.  **Run the App**:
    ```bash
    streamlit run app.py
    ```
2.  The app will open in your default web browser (usually at `http://localhost:8501`).
3.  Enter your API Key in the sidebar (if not set via environment variable).
4.  Select a model (e.g., Claude 3 Opus).
5.  Use the tabs to navigate between features.

### CLI

The CLI is perfect for quick tasks or scripting.

```bash
# General usage
python main.py <command> [options]

# Examples:
python main.py summarize path/to/file.txt
python main.py refactor path/to/code.py
python main.py gen-tests path/to/code.py
python main.py explain path/to/error.log
python main.py ask "What does this class do?" --files "src/*.py"
```

## Uploading to GitHub

If you want to host your own version or contribute:

1.  **Initialize Git**:
    ```bash
    git init
    ```

2.  **Add Files**:
    ```bash
    git add .
    ```

3.  **Commit Changes**:
    ```bash
    git commit -m "Initial commit"
    ```

4.  **Push to GitHub**:
    Create a new repository on GitHub, then follow the instructions to push:
    ```bash
    git remote add origin https://github.com/your-username/local-ai-assistant.git
    git branch -M main
    git push -u origin main
    ```

## Testing

To run the unit tests (which mock the API calls):

```bash
python -m unittest tests/test_cli_mock.py
```
