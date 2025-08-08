import os
from dotenv import load_dotenv

from starter.phase_1.workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, EvaluationAgent

# Load environment variables from .env file
load_dotenv('tests/.env')
# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key is not None, "OPENAI_API_KEY not found in .env"

prompt = "What is the capital of France?"

# Parameters for the Knowledge Agent
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

# Parameters for the Evaluation Agent
persona = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
evaluation_agent = EvaluationAgent(openai_api_key, persona, evaluation_criteria, knowledge_agent, max_interactions=10)

response = evaluation_agent.evaluate(prompt)

print("======= [EvaluationAgent] =======")
print("Knowledge sorce: Training dataset in LLM, and the provided knowledge, and the evaluation criteria")
print(f"Persona: {persona}")
print(f"prompt: {prompt}")
print(f"Evaluation criteria: {evaluation_criteria}")
print(f"response: {response}")
print(f"expected difference: the output is a single city name, not a sentence. Which does contradict the worker persona")
print()