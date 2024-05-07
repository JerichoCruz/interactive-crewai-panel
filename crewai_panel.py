from crewai import Crew, Process, Agent, Task
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.callbacks import BaseCallbackHandler
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
from langchain.agents import load_tools
from langchain.tools import tool
from typing import TYPE_CHECKING, Any, Dict, Optional
import panel as pn 
pn.extension(design="material") # Setting the design framework for the Panel UI
import threading
import time
import os
from dotenv import load_dotenv
from crewai.agents import CrewAgentExecutor

# Load environment variables
load_dotenv()

# Set API key from environment variable in the .env file
# To get your API key for free, visit: https://serper.dev/
os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')

search = GoogleSerperAPIWrapper()

search_tool = Tool(
    name="Scrape Google Searches",
    func=search.run,
    description="Ask the agent to search the internet using Google.",
)

# Custom function to handle human inputs in the agent-executor workflow
def custom_ask_human_input(self, final_answer: dict) -> str:
      
      global user_input

      # Compose a prompt message to request human input
      prompt = self._i18n.slice("getting_input").format(final_answer=final_answer)
      chat_interface.send(prompt, user="assistant", respond=False)

      # Wait for user input to be available
      while user_input == None:
          time.sleep(1)  

      human_comments = user_input  # Store the user input
      user_input = None  # Reset user input for future inputs

      return human_comments  # Return the captured human input

# Replacing the default input asking method with the custom method
CrewAgentExecutor._ask_human_input = custom_ask_human_input

# Global variables for storing user input and tracking task initiation
user_input = None
initiate_chat_task_created = False

# Function to initiate chat by starting a new thread
def initiate_chat(message):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True # Set flag that a chat task has been created

    StartCrew(message) # Start the crew task based on the message

# Callback function for handling chat inputs
def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    
    global initiate_chat_task_created
    global user_input

    # Start a new chat thread if no task has been initiated
    if not initiate_chat_task_created:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()

    else:
        user_input = contents   # Otherwise, store user input for processing

# Dictionary of agent avatars for UI representation
avatars = {
    "Marketer": "https://i.imgur.com/mkfOVyG.png",
    "Technologist": "https://i.imgur.com/XEusRS3.png",
    "Business Consultant": "https://i.imgur.com/9hslbDP.png"
}

# Custom handler for managing agent callback events
class MyCustomHandler(BaseCallbackHandler):
    
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""

        chat_interface.send(inputs['input'], user="Assistant", respond=False)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
    
        chat_interface.send(outputs['output'], user=self.agent_name, avatar=avatars[self.agent_name], respond=False)

# Use OpenAI's model(s)
# llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Use of different language models from langchain libraries 
llm = Ollama(model="mistral") # https://ollama.com/library/mistral

# Definitions of agents with specific roles, backstories, and goals
# Define agents
marketer = Agent(
    role="Market Research Analyst",
    goal="Find out how big is the demand for my products and suggest how to reach the widest possible customer base",
    backstory="""You are an expert at understanding the market demand, target audience, and competition. 
    	        This is crucial for validating whether an idea fulfills a market need and has the potential to attract a wide audience. 
    	        You are good at coming up with ideas on how to appeal to the widest possible audience.
		""",
    # verbose=True,
    allow_delegation=False,
    tools=[search_tool], # Allows agent to use google search.
    llm=llm,
    callbacks=[MyCustomHandler("Marketer")],
)

technologist = Agent(
    role="Technology Expert",
    goal="Make assessment on how technologically feasible the company is and what type of technologies the company needs to adopt in order to succeed",
    backstory="""You are a visionary in the realm of technology, with a deep understanding of both current and emerging technological trends. 
        Your expertise lies not just in knowing the technology but in foreseeing how it can be leveraged to solve real-world problems and drive business innovation.
		You have a knack for identifying which technological solutions best fit different business models and needs, ensuring that companies stay ahead of the curve. 
        Your insights are crucial in aligning technology with business strategies, ensuring that the technological adoption not only enhances operational efficiency but also provides a competitive edge in the market.""",
    # verbose=True,
    allow_delegation=False,
    llm=llm,
    callbacks=[MyCustomHandler("Technologist")],
)

business_consultant = Agent(
    role="Business Development Consultant",
    goal="Evaluate and advise on the business model, scalability, and potential revenue streams to ensure long-term sustainability and profitability",
    backstory="""You are a seasoned professional with expertise in shaping business strategies. Your insight is essential for turning innovative ideas 
		into viable business models. You have a keen understanding of various industries and are adept at identifying and developing potential revenue streams. 
		Your experience in scalability ensures that a business can grow without compromising its values or operational efficiency. Your advice is not just
		about immediate gains but about building a resilient and adaptable business that can thrive in a changing market.""",
    # verbose=True,
    allow_delegation=False,
    llm=llm,
    callbacks=[MyCustomHandler("Business Consultant")],
)

# Function to start the crew process based on a prompt
def StartCrew(prompt):

    task1 = Task(
        description=f"""Analyze what the market demand for GenAI agents, LLMs, Embeddings and GenAI Solutions in the {prompt} industry. 
                    Find out what the ideal customer might look like, and how to reach the widest possible audience.""",
        agent=marketer,
        expected_output="A concise report with at least 10 builtin points and it has to address the most important areas when it comes to marketing this type of business.",
    )

    task2 = Task(
        description="""Analyze how to create systems that leverage LLMs for many use cases, including retrieval augmented generation, data parsing, data generation, decision making and analysis.
                    with description of which technologies the business needs to use in order to implement GenAI for customers.""",
        agent=technologist,
        expected_output="""A detailed report with at least 10 builtin points with description of which technologies the business needs to use in order to implement GenAI for customers 
                        for this type of business when it comes to marketing this type of business.
                        
                        Make sure to check with a human if your comment is good before finalizing your answer.""",
        human_input=True, # Respond with "Approved, please proceed." or "Try again."
    )

    task3 = Task(
        description="""Analyze and summarize marketing and technological report.""",
        agent=business_consultant,
        expected_output="""A detailed business plan with description of how to make a sustainable and profitable business using the marketing and technological reports.
            The Business Plan Output MUST have the following format:
            Marketing Report: Provide the full marketing report in full. Provide your own thoughts on how it connects to the overall business plan.
            Technological Report: Provide the full technological report. Provide your own thoughts on how it connects to the overall business plan.
            Business Model: Description of how to make a sustainable and profitable consulting business with at least 10 concise points.
            Scalability Strategies: Description of scalability strategies with at least 5 concise builtin points.
            Potential Revenue Streams: 5 bullet points of potential revenue streams.
            Goals: Time schedule for 5 goals to be achieved and when.

            Make sure to check with a human if your comment is good before finalizing your answer.
            """,
        # human_input=True,
    )

    # Establishing the crew with a hierarchical process
    project_crew = Crew(
        agents=[marketer, technologist, business_consultant],
        tasks=[task1, task2, task3],
        verbose=2,
        manager_llm=llm,
        # process=Process.hierarchical, # Specifies the hierarchical management approach.
        process=Process.sequential, # Specifies the sequential approach and will follow the task order.
    )

    result = project_crew.kickoff() # Start the process and get the result

    chat_interface.send("## Final Result\n"+result, user="Assistant", respond=False)

# Setting up the chat interface and making it interactive using panel
chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Enter your industry or topic to start the analysis and receive strategic insights.", user="System", respond=False)
chat_interface.servable()