import streamlit as st
import os
import glob
from local_ai_cli.ai_client import AIClient
from local_ai_cli.file_ops import read_file_content

# Page Configuration
st.set_page_config(
    page_title="Local AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Sidebar - Configuration
with st.sidebar:
    st.title("🤖 Local AI Assistant")

    # API Key Handling
    # Use session state to persist API key if entered manually, otherwise env var
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    api_key_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Anthropic API Key. It defaults to the ANTHROPIC_API_KEY environment variable.",
        key="api_key_input"
    )

    # Update session state if input changes
    if api_key_input:
        st.session_state.api_key = api_key_input

    # Model Selection
    model = st.selectbox(
        "Model",
        ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        index=0
    )

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This tool wraps the Anthropic API to help you summarize files, refactor code, generate tests, explain errors, and chat with your codebase.")

# Initialize Client
client = None
if st.session_state.api_key:
    try:
        # Pass the key explicitly to the client
        client = AIClient(api_key=st.session_state.api_key)
        # Hack to allow model switching since AIClient hardcodes it in init
        client.model = model
    except Exception as e:
        st.error(f"Failed to initialize AI Client: {e}")
        st.stop()

# Helper Functions
def get_file_content(filepath):
    """
    Reads file content and returns (content, error_message).
    """
    if not filepath:
        return None, "Please enter a file path."

    content, error = read_file_content(filepath)
    if error:
        return None, error
    return content, None


# Main Interface
st.title("Local AI Coding Assistant")

if not client:
    st.warning("Please provide an Anthropic API Key in the sidebar to proceed.")
    st.stop()

# Tabs for different functionalities
# Using distinct tabs to organize the workflow
tab_chat, tab_summarize, tab_refactor, tab_tests, tab_explain = st.tabs([
    "💬 Chat with Codebase",
    "📝 Summarize File",
    "🛠️ Refactor Code",
    "🧪 Generate Tests",
    "🔍 Explain Error"
])

# --- Tab: Chat with Codebase ---
with tab_chat:
    st.header("Chat with your Codebase")
    st.markdown("Ask questions about your project. You can specify file patterns (e.g., `src/*.py`) to include relevant files as context.")

    # Context Files Input
    context_patterns = st.text_input(
        "Context Files (Glob Patterns)",
        placeholder="e.g. local_ai_cli/*.py tests/*.py",
        help="Space-separated glob patterns to identify files to read for context.",
        key="chat_context_patterns"
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Prepare context files
        context_files = {}
        if context_patterns:
            patterns = context_patterns.split()
            for pattern in patterns:
                # glob.glob returns a list of file paths matching the pattern
                found_files = glob.glob(pattern, recursive=True)
                for filepath in found_files:
                    c, e = read_file_content(filepath)
                    if not e:
                        context_files[filepath] = c

        # Generate response
        with st.spinner("Thinking..."):
            try:
                response = client.ask_question(prompt, context_files)
            except Exception as e:
                response = f"Error: {str(e)}"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


# --- Tab: Summarize ---
with tab_summarize:
    st.header("Summarize File")
    file_path_sum = st.text_input("File Path", key="sum_path", placeholder="path/to/file.txt")

    if st.button("Summarize", key="btn_summarize"):
        with st.spinner("Reading file..."):
            content, error = get_file_content(file_path_sum)

        if error:
            st.error(error)
        else:
            st.subheader("File Content Preview")
            with st.expander("Show Content"):
                st.code(content)

            with st.spinner("Generating summary..."):
                try:
                    summary = client.summarize(content)
                    st.subheader("Summary")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

# --- Tab: Refactor ---
with tab_refactor:
    st.header("Refactor Code")
    file_path_ref = st.text_input("File Path", key="ref_path", placeholder="path/to/code.py")

    if st.button("Refactor Code", key="btn_refactor"):
        with st.spinner("Reading file..."):
            content, error = get_file_content(file_path_ref)

        if error:
            st.error(error)
        else:
            # Layout: Original Code (Left) -> Refactored Code (Right)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Code")
                st.code(content, language='python')

            with st.spinner("Refactoring..."):
                try:
                    refactored_code = client.refactor(content)
                    with col2:
                        st.subheader("Refactored Code")
                        st.code(refactored_code, language='python')
                except Exception as e:
                    st.error(f"Error refactoring code: {e}")

# --- Tab: Generate Tests ---
with tab_tests:
    st.header("Generate Tests")
    file_path_test = st.text_input("File Path", key="test_path", placeholder="path/to/code.py")

    if st.button("Generate Tests", key="btn_tests"):
        with st.spinner("Reading file..."):
            content, error = get_file_content(file_path_test)

        if error:
            st.error(error)
        else:
            st.subheader("Source Code")
            with st.expander("Show Source"):
                st.code(content, language='python')

            with st.spinner("Generating tests..."):
                try:
                    tests = client.generate_tests(content)
                    st.subheader("Generated Tests")
                    st.code(tests, language='python')
                except Exception as e:
                    st.error(f"Error generating tests: {e}")

# --- Tab: Explain Error ---
with tab_explain:
    st.header("Explain Error")
    file_path_err = st.text_input("Log File Path", key="err_path", placeholder="path/to/error.log")

    if st.button("Explain Error", key="btn_explain"):
        with st.spinner("Reading file..."):
            content, error = get_file_content(file_path_err)

        if error:
            st.error(error)
        else:
            st.subheader("Error Log")
            with st.expander("Show Log"):
                st.code(content)

            with st.spinner("Analyzing error..."):
                try:
                    explanation = client.explain_error(content)
                    st.subheader("Explanation & Fix")
                    st.markdown(explanation)
                except Exception as e:
                    st.error(f"Error explaining log: {e}")
