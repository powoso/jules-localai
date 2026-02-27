# Local AI CLI Tool

A command-line tool that wraps the Anthropic API to perform various coding tasks, such as summarizing files, refactoring code, generating tests, explaining error logs, and answering questions about your codebase.

## Prerequisites

- Python 3.7+
- An Anthropic API Key

## Installation

1.  Clone the repository or navigate to the project directory.
2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Set your Anthropic API Key as an environment variable:

    ```bash
    export ANTHROPIC_API_KEY="your-api-key-here"
    ```

## Usage

You can run the tool using `python main.py` followed by a command.

### Commands

#### 1. Summarize a File
Summarizes the content of a text file.

```bash
python main.py summarize <path-to-file>
```

#### 2. Refactor Code
Refactors the code in the specified file for readability, performance, and maintainability.

```bash
python main.py refactor <path-to-file>
```

#### 3. Generate Tests
Generates unit tests for the code in the specified file.

```bash
python main.py gen-tests <path-to-file>
```

#### 4. Explain Error
Explains an error log found in the specified file and suggests fixes.

```bash
python main.py explain <path-to-log-file>
```

#### 5. Ask Questions
Answers questions about your codebase, using provided files as context.

```bash
python main.py ask "What does the user class do?" --files "src/*.py" "tests/*.py"
```

The `--files` argument accepts file paths or glob patterns to include relevant context for the LLM.

## Testing

To run the unit tests (which mock the API calls):

```bash
python -m unittest tests/test_cli_mock.py
```
