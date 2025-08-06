# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

# Load environment variables from .env file
load_dotenv('tests/.env')
# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key is not None, "OPENAI_API_KEY not found in .env"

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
knowledge_agent_response = knowledge_agent.respond(prompt)

print(knowledge_agent_response)

print("======= [KnowledgeAugmentedPromptAgent] =======")
print("Knowledge sorce: Training dataset in LLM, and the provided knowledge ")
print(f"Persona: {persona}")
print(f"prompt: {prompt}")
print(f"response: {knowledge_agent_response}")
print(f"expected difference: the output starts with 'Dear students,'. Also it will say London is the capital of France")
print()