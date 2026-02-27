import unittest
from unittest.mock import MagicMock, patch
import os
import io
import sys
# Make sure we can import local_ai_cli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from local_ai_cli.ai_client import AIClient
from local_ai_cli import cli

class TestCLI(unittest.TestCase):
    def setUp(self):
        # Create a dummy file for testing file ops
        self.test_file = "test_input.txt"
        with open(self.test_file, "w") as f:
            f.write("Sample content")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('local_ai_cli.ai_client.anthropic.Anthropic')
    def test_client_init(self, mock_anthropic):
        # Test initialization with API key
        client = AIClient(api_key="test-key")
        mock_anthropic.assert_called_with(api_key="test-key")
        self.assertIsNotNone(client.client)

        # Test initialization with env var
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env-key"}):
            client = AIClient()
            mock_anthropic.assert_called_with(api_key="env-key")

    @patch('local_ai_cli.ai_client.anthropic.Anthropic')
    def test_summarize(self, mock_anthropic):
        # Mock the API response
        mock_client_instance = mock_anthropic.return_value
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Summary result")]
        mock_client_instance.messages.create.return_value = mock_message

        client = AIClient(api_key="test")
        result = client.summarize("Long text")

        self.assertEqual(result, "Summary result")

        # Verify the correct prompt was sent
        args, kwargs = mock_client_instance.messages.create.call_args
        self.assertIn("summarizes text concisely", kwargs['system'])
        self.assertIn("Long text", kwargs['messages'][0]['content'])

    @patch('local_ai_cli.ai_client.anthropic.Anthropic')
    def test_refactor(self, mock_anthropic):
        mock_client_instance = mock_anthropic.return_value
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Refactored code")]
        mock_client_instance.messages.create.return_value = mock_message

        client = AIClient(api_key="test")
        result = client.refactor("def foo(): pass")

        self.assertEqual(result, "Refactored code")

        args, kwargs = mock_client_instance.messages.create.call_args
        self.assertIn("Refactor the following code", kwargs['system'])
        self.assertIn("def foo(): pass", kwargs['messages'][0]['content'])

    @patch('local_ai_cli.ai_client.anthropic.Anthropic')
    def test_generate_tests(self, mock_anthropic):
        mock_client_instance = mock_anthropic.return_value
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Test code")]
        mock_client_instance.messages.create.return_value = mock_message

        client = AIClient(api_key="test")
        result = client.generate_tests("def add(a,b): return a+b")

        self.assertEqual(result, "Test code")

    @patch('local_ai_cli.ai_client.anthropic.Anthropic')
    def test_explain_error(self, mock_anthropic):
        mock_client_instance = mock_anthropic.return_value
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Error explanation")]
        mock_client_instance.messages.create.return_value = mock_message

        client = AIClient(api_key="test")
        result = client.explain_error("Traceback...")

        self.assertEqual(result, "Error explanation")

    @patch('local_ai_cli.ai_client.anthropic.Anthropic')
    def test_ask_question(self, mock_anthropic):
        mock_client_instance = mock_anthropic.return_value
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Answer")]
        mock_client_instance.messages.create.return_value = mock_message

        client = AIClient(api_key="test")
        context = {"file1.py": "print('hello')"}
        result = client.ask_question("What does this do?", context)

        self.assertEqual(result, "Answer")
        args, kwargs = mock_client_instance.messages.create.call_args
        self.assertIn("file1.py", kwargs['messages'][0]['content'])
        self.assertIn("print('hello')", kwargs['messages'][0]['content'])
        self.assertIn("What does this do?", kwargs['messages'][0]['content'])

    # Testing CLI Integration using mocked AIClient

    @patch('local_ai_cli.cli.AIClient')
    def test_cli_summarize(self, MockAIClient):
        mock_client = MockAIClient.return_value
        mock_client.summarize.return_value = "Mock Summary"

        # Redirect stdout to capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        test_args = ["main.py", "summarize", self.test_file]
        with patch.object(sys, 'argv', test_args):
            cli.main()

        sys.stdout = sys.__stdout__ # Reset stdout

        mock_client.summarize.assert_called_once()
        self.assertIn("Mock Summary", captured_output.getvalue())

    @patch('local_ai_cli.cli.AIClient')
    def test_cli_ask(self, MockAIClient):
        mock_client = MockAIClient.return_value
        mock_client.ask_question.return_value = "Mock Answer"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Test ask command with --files
        test_args = ["main.py", "ask", "Why?", "--files", self.test_file]
        with patch.object(sys, 'argv', test_args):
             cli.main()

        sys.stdout = sys.__stdout__

        # Verify ask_question called with correct arguments
        mock_client.ask_question.assert_called()
        args, kwargs = mock_client.ask_question.call_args
        self.assertEqual(args[0], "Why?")
        # The second arg should be a dict containing the file content
        self.assertIn(self.test_file, args[1])
        self.assertEqual(args[1][self.test_file], "Sample content")

if __name__ == '__main__':
    unittest.main()
