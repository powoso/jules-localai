import os
import anthropic

class AIClient:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY")

        self.client = None
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)

        # Use a cheaper/faster model for testing if needed, or default to opus
        self.model = os.environ.get("ANTHROPIC_MODEL", "claude-3-opus-20240229")

    def _generate_response(self, system_prompt, user_prompt):
        if not self.client:
             return "Error: ANTHROPIC_API_KEY not found. Please set the ANTHROPIC_API_KEY environment variable."

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            # Access the content correctly based on the response structure
            if message.content and len(message.content) > 0:
                return message.content[0].text
            return "Error: Empty response from API."
        except Exception as e:
            return f"Error communicating with Anthropic API: {e}"

    def summarize(self, text):
        return self._generate_response(
            "You are a helpful assistant that summarizes text concisely.",
            f"Please summarize the following text:\n\n{text}"
        )

    def refactor(self, code):
        return self._generate_response(
            "You are an expert software engineer. Refactor the following code to improve readability, performance, and maintainability. Return only the refactored code block.",
            f"Refactor this code:\n\n{code}"
        )

    def generate_tests(self, code):
        return self._generate_response(
            "You are an expert software engineer. Write comprehensive unit tests for the following code using a standard testing framework (like unittest for Python). Return only the code block containing the tests.",
            f"Generate unit tests for this code:\n\n{code}"
        )

    def explain_error(self, error_log):
        return self._generate_response(
            "You are a helpful assistant that explains error logs and suggests fixes.",
            f"Explain this error log and suggest a fix:\n\n{error_log}"
        )

    def ask_question(self, question, context_files):
        context_str = ""
        for filepath, content in context_files.items():
            context_str += f"--- File: {filepath} ---\n{content}\n\n"

        return self._generate_response(
            "You are a helpful assistant that answers questions about a codebase. You will be provided with the content of relevant files.",
             f"Context:\n{context_str}\nQuestion: {question}"
        )
