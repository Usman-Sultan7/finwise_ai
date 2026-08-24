from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache, SQLiteCache

def configure_llm_cache(cache_type: str = "memory"):
    """
    Configures the global caching mechanism for LangChain.
    """
    if cache_type == "sqlite":
        # Stores cache in a local database file
        set_llm_cache(SQLiteCache(database_path=".langchain.db"))
    else:
        # Stores cache strictly in RAM
        set_llm_cache(InMemoryCache())