# agentic_workflow.py

from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
import os
from dotenv import load_dotenv

load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPEN_API_KEY is not None, "OPENAI_API_KEY not found in .env"
# load the product spec

product_spec = None
with open("Product-Spec-Email-Router.txt", 'r', encoding="utf-8") as f:
    product_spec = f.read()
    
assert product_spec is not None, "Product spec not found"
# Instantiate all the agents
MAX_INTERACTIONS = 30
# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
action_planning_agent = ActionPlanningAgent(OPEN_API_KEY, knowledge_action_planning)
# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    "Here is the product spec: \n"
    f"{product_spec}"
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(OPEN_API_KEY, persona_product_manager, knowledge_product_manager)
# Product Manager - Evaluation Agent
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_product_manager_eval = "You are an evaluation agent that checks the answers of product_manager_knowledge_agent."
evaluation_criteria = "The answer should provide user stories that follow the structure: 'As a [type of user], I want [an action or feature] so that [benefit/value]'. Each story should clearly identify the user persona, define a specific action or feature they desire, and explain the intended benefit or value."
product_manager_evaluation_agent = EvaluationAgent(OPEN_API_KEY, persona_product_manager_eval, evaluation_criteria,
                                                   product_manager_knowledge_agent, max_interactions=MAX_INTERACTIONS)
# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(OPEN_API_KEY, persona_program_manager, knowledge_program_manager)
# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
program_manager_eval_criteria = "The answer should be product features that follow the following structure: " \
    "Feature Name: A clear, concise title that identifies the capability\n" \
    "Description: A brief explanation of what the feature does and its purpose\n" \
    "Key Functionality: The specific capabilities or actions the feature provides\n" \
    "User Benefit: How this feature creates value for the user"
program_manager_evaluation_agent = EvaluationAgent(OPEN_API_KEY, persona_program_manager_eval, program_manager_eval_criteria, program_manager_knowledge_agent, max_interactions=MAX_INTERACTIONS)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(OPEN_API_KEY, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."

# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
development_engineer_evaluation_criteria = "The answer should be tasks following this exact structure: " \
    "Task ID: A unique identifier for tracking purposes\n" \
    "Task Title: Brief description of the specific development work\n" \
    "Related User Story: Reference to the parent user story\n" \
    "Description: Detailed explanation of the technical work required\n" \
    "Acceptance Criteria: Specific requirements that must be met for completion\n" \
    "Estimated Effort: Time or complexity estimation\n" \
    "Dependencies: Any tasks that must be completed first"

development_engineer_evaluation_agent = EvaluationAgent(OPEN_API_KEY, persona_dev_engineer_eval, development_engineer_evaluation_criteria, development_engineer_knowledge_agent, max_interactions=MAX_INTERACTIONS)

# Routing Agent

routing_agent = RoutingAgent(OPEN_API_KEY, [
    {"name": "Product Manager",
     "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories",
     "func": lambda x: product_manager_support_function(x)},
    {"name": "Program Manager",
     "description": "Responsible for defining product features only. Groups user stories into cohesive features. Does not define user stories or tasks.",
     "func": lambda x: program_manager_support_function(x)},
    {"name": "Development Engineer",
     "description": "Responsible for defining development tasks only. Does not define product personas or features.",
     "func": lambda x: development_engineer_support_function(x)}
])
# Job function persona support functions
def product_manager_support_function(query):
    response = product_manager_knowledge_agent.respond(query)
    evaluated_response = product_manager_evaluation_agent.evaluate(response)
    return evaluated_response['final_response']

def program_manager_support_function(query):
    response = program_manager_knowledge_agent.respond(query)
    evaluated_response = program_manager_evaluation_agent.evaluate(response)
    return evaluated_response['final_response']

def development_engineer_support_function(query):
    response = development_engineer_knowledge_agent.respond(query)
    evaluated_response = development_engineer_evaluation_agent.evaluate(response)
    return evaluated_response['final_response']
# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "What would the development tasks for this product be?"
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")

action_planning_response = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
with open("action_planning_response.txt", "w", encoding="utf-8") as f:
    f.write(str(action_planning_response))
if os.path.exists("routing_response.txt"):
    os.remove("routing_response.txt")
completed_steps = []
for step in action_planning_response:
    selected_agent_name, routing_response = routing_agent.route(step,
                                           detailed_input = f"{'\n'.join(completed_steps)} \n Step {step}: ",
                                           return_agent_name=True)
    completed_steps.append(routing_response)
    with open("routing_response.txt", "a", encoding="utf-8") as f:
        f.write(f"Step {step} completed by {selected_agent_name} with result:\n {routing_response}\n =====")
    print(f"Step {step} completed by {selected_agent_name} with result: {routing_response}")

print(f"\nWorkflow completed. Final result: {completed_steps[-1]}")
with open("final_result.txt", "w", encoding="utf-8") as f:
    f.write(f"\nWorkflow completed. Final result: {completed_steps[-1]}")