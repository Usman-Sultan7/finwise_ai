import os
from langchain_openai import ChatOpenAI
from src.prompts import finwise_prompt, JSON_SCHEMA

# 1. Add api_key as a required parameter
def get_llm(api_key: str): 
    """Initializes and returns the ChatOpenAI model."""
    return ChatOpenAI(
        temperature=0.2, 
        model_name="gpt-4o-mini",
        # 2. Pass the dynamic key instead of os.getenv
        api_key=api_key, 
        streaming=True 
    )

def get_financial_chain():
    """Builds a reusable chain connecting the prompt and the model."""
    llm = get_llm()
    # Using LangChain Expression Language (LCEL) to build the chain
    chain = finwise_prompt | llm
    return chain

def stream_recommendations(llm, inputs: dict):
    """
    Streams the raw LLM output chunk by chunk.
    This fulfills the assignment requirement to use llm.stream().
    """
    messages = finwise_prompt.format_messages(
        json_schema=JSON_SCHEMA,
        **inputs
    )
    
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content