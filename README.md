# Interactive CrewAI Panel

This project leverages the CrewAI framework and Panel library to create an interactive web application facilitating dynamic interaction between human users and AI agents. It's designed to analyze and strategize business processes with AI insights and human expertise.

## What This App Does

This application is a demo of how custom AI agents work together and include a human-in-the-loop to derive strategic insights through a single prompt. It integrates three specialized AI agents:
- **Market Research Analyst**: Analyzes market demands and customer outreach strategies.
- **Technology Expert**: Assesses technological trends and adoption strategies to enhance business operations.
- **Business Development Consultant**: Advises on business model scalability and potential revenue streams.

These agents work collaboratively within a responsive web interface to provide real-time analysis and feedback, allowing users to input data and receive actionable business intelligence.

## Features

- Dynamic human-agent interaction.
- Real-time analytical feedback.
- Responsive web interface using Panel.

## Prerequisites

- **Python Installation**: Make sure you have Python 3.10.11 or higher installed. [Download Python](https://www.python.org/downloads/)
- **Virtual Environment**: Usage of a Python virtual environment is recommended for managing dependencies. [Learn about virtual environments](https://docs.python.org/3/tutorial/venv.html)
- **Ollama Installation**: [Ollama must be installed](https://ollama.com/) as part of the LangChain libraries. Ensure all dependencies for Ollama are correctly installed. `crewai_panel.py` uses mistral which can be installed running this command: `ollama run mistral`
- **SERP API Key**: An API key for the SERP service. Ensure you have the API key configured as an environment variable. Sign up and get a key at [SERP](https://serper.dev/). (Optional)
- **API Keys**: Ensure you have the necessary API keys configured as environment variables, as detailed in the `.env` file instructions.
- **Git**: Optional but recommended for cloning the repository. [Install Git](https://git-scm.com/downloads)

## Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Create a .env file at the root directory with your SERPER_API_KEY:
```
SERPER_API_KEY=your_api_key_here
```
See `.env.sample`

Run the application:
```bash
panel serve crewai_panel.py
```
Access the application via http://localhost:5006/crewai_panel in your browser.


## License

Distributed under the MIT License. See LICENSE for more information.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) and [Panel](https://github.com/holoviz/panel) frameworks for backend and frontend support.
- [Ollama](https://github.com/ollama/ollama) from [LangChain](https://github.com/langchain-ai/langchain) for providing the advanced language model capabilities that enhance agent interactions and decision-making processes.
- [Yeyu Huang's - How to Create an Interactive UI for CrewAI Applications Blog Post](https://medium.com/gitconnected/how-to-create-an-interactive-ui-for-crewai-applications-e4d3fae0dbf8)