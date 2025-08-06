
# TODO: 1 - Import the KnowledgeAugmentedPromptAgent and RoutingAgent
import os
from dotenv import load_dotenv

from starter.phase_1.workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
from starter.phase_1.workflow_agents.base_agents import RoutingAgent

# Load environment variables from .env file
load_dotenv('tests/.env')
# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key is not None, "OPENAI_API_KEY not found in .env"

persona = "You are a college professor"

knowledge = "You know everything about Texas"
# TODO: 2 - Define the Texas Knowledge Augmented Prompt Agent
texas_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

knowledge = "You know everything about Europe"
# TODO: 3 - Define the Europe Knowledge Augmented Prompt Agent
europe_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

persona = "You are a college math professor"
knowledge = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
# TODO: 4 - Define the Math Knowledge Augmented Prompt Agent
math_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

routing_agent = RoutingAgent(openai_api_key, {})
agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: texas_agent.respond(x)
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: europe_agent.respond(x)
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: math_agent.respond(x)
    }
]

routing_agent.agents = agents

# TODO: 8 - Print the RoutingAgent responses to the following prompts:
#           - "Tell me about the history of Rome, Texas"
#           - "Tell me about the history of Rome, Italy"
#           - "One story takes 2 days, and there are 20 stories"
prompt1 = "Tell me about the history of Rome, Texas"
prompt2 = "Tell me about the history of Rome, Italy"
prompt3 = "One story takes 2 days, and there are 20 stories"
response1 = routing_agent.route(prompt1)
response2 = routing_agent.route(prompt2)
response3 = routing_agent.route(prompt3)

print("======= [RoutingAgent] =======")
print("Knowledge sorce: Training dataset in LLM, and the provided agent descriptions")
print(f"prompt: {prompt1}")
print(f"response: {response1}")
print(f"expected roted agent: Texas agent")
print(f"prompt: {prompt2}")
print(f"response: {response2}")
print(f"expected routed agent: Europe agent")
print(f"prompt: {prompt3}")
print(f"response: {response3}")
print(f"expected roted agent: Math agent")
print()