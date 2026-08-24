import os
from langchain_openai import ChatOpenAI
from src.prompts import finwise_prompt, JSON_SCHEMA

def get_llm():
    """Initializes and returns the ChatOpenAI model."""
    return ChatOpenAI(
        temperature=0.2, # Low temperature for analytical consistency
        model_name="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True # Crucial for the st.write_stream requirement
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