# Test script for DirectPromptAgent class

from workflow_agents.base_agents import DirectPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('tests/.env')


openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key is not None, "OPENAI_API_KEY not found in .env"
prompt = "What is the Capital of France?"

direct_agent_response = DirectPromptAgent(openai_api_key).respond(prompt)

# Print the response from the agent
print(direct_agent_response)

print("======= [DirectPromptAgent] =======")
print("Knowledge sorce: Only the training dataset in the LLM ")
print("Persona: None")
print(f"prompt: {prompt}")
print(f"response: {direct_agent_response}")
print()
