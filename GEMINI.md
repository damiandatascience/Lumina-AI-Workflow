# GEMINI.md

## Project Overview

This project, named **Lumina**, is an AI agent designed to transform natural language instructions into polished data visualizations. It follows an "AI Workflow" pattern, which is a structured pipeline of components that execute in sequence to generate, critique, and refine data visualizations.

The core technologies used in this project are:

*   **Python 3.12+**
*   **FastAPI** for the REST API
*   **Gradio** for the web interface
*   **OpenAI (GPT-4)** for code generation and reflection
*   **Pandas** for data manipulation
*   **Matplotlib** for creating visualizations

The project is structured as a modular application with a clear separation of concerns. The main components are:

*   **`src/main.py`**: The main entry point for the AI workflow.
*   **`src/api.py`**: The FastAPI application that exposes the workflow as a REST API.
*   **`src/interface.py`**: The Gradio web interface that provides a user-friendly UI.
*   **`src/generator.py`**: The component responsible for generating the initial Python code for the visualization.
*   **`src/reflector.py`**: The component that critiques the generated visualization and provides feedback for improvement.
*   **`src/executor.py`**: The component that executes the Python code to generate the visualizations.
*   **`src/data_processing.py`**: The module for loading and preparing data from different sources (CSV or MongoDB).
*   **`src/config.py`**: The centralized configuration file for the project.
*   **`pyproject.toml`**: The file that contains the project's dependencies.

## Building and Running

The project uses `uv` for dependency management.

### Running the Application

There are two ways to run the application:

1.  **Web Interface (Recommended)**:
    *   Start the FastAPI server:
        ```bash
        uv run fastapi -m dev src/api.py
        ```
    *   In a separate terminal, start the Gradio interface:
        ```bash
        uv run python src/interface.py
        ```
    *   Open your browser and go to `http://localhost:7860`.

2.  **Command Line**:
    *   You can run the entire workflow directly from the command line:
        ```bash
        python src/main.py
        ```

### Running Tests

This project does not have a dedicated test suite.

## Development Conventions

### Linting and Formatting

The project uses `ruff` for linting and formatting.

*   To check for linting errors:
    ```bash
    uv run ruff check src/
    ```
*   To format the code:
    ```bash
    uv run ruff format src/
    ```

### Code Style

The project follows the PEP 8 style guide for Python code. The code is well-documented with docstrings and comments where necessary.

### Contribution Guidelines

Contributions are welcome. Please follow these steps:

1.  Fork the project.
2.  Create a new branch for your feature.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Open a pull request.
