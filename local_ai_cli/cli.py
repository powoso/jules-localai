import argparse
import sys
import glob
from .ai_client import AIClient
from .file_ops import read_file_content

def main():
    parser = argparse.ArgumentParser(description="Local AI CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Summarize
    summarize_parser = subparsers.add_parser("summarize", help="Summarize a file")
    summarize_parser.add_argument("file", help="Path to the file to summarize")

    # Refactor
    refactor_parser = subparsers.add_parser("refactor", help="Refactor code in a file")
    refactor_parser.add_argument("file", help="Path to the file to refactor")

    # Generate Tests
    gen_tests_parser = subparsers.add_parser("gen-tests", help="Generate tests for a file")
    gen_tests_parser.add_argument("file", help="Path to the file to generate tests for")

    # Explain Error
    explain_parser = subparsers.add_parser("explain", help="Explain an error log")
    explain_parser.add_argument("file", help="Path to the file containing the error log")

    # Ask Question
    ask_parser = subparsers.add_parser("ask", help="Ask a question about the codebase")
    ask_parser.add_argument("question", help="The question to ask")
    ask_parser.add_argument("--files", nargs="+", help="List of file patterns to include as context (e.g., src/*.py)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = AIClient()

    if args.command == "summarize":
        content, error = read_file_content(args.file)
        if error:
            print(error)
        else:
            print(client.summarize(content))

    elif args.command == "refactor":
        content, error = read_file_content(args.file)
        if error:
            print(error)
        else:
            print(client.refactor(content))

    elif args.command == "gen-tests":
        content, error = read_file_content(args.file)
        if error:
            print(error)
        else:
            print(client.generate_tests(content))

    elif args.command == "explain":
        content, error = read_file_content(args.file)
        if error:
            print(error)
        else:
            print(client.explain_error(content))

    elif args.command == "ask":
        context_files = {}
        if args.files:
            for pattern in args.files:
                # glob returns a list of files matching the pattern
                files = glob.glob(pattern, recursive=True)
                for filepath in files:
                    content, error = read_file_content(filepath)
                    if not error:
                        context_files[filepath] = content
                    else:
                        print(f"Warning: {error}")

        if not context_files:
            print("Warning: No context files found or provided.")

        print(client.ask_question(args.question, context_files))

if __name__ == "__main__":
    main()
