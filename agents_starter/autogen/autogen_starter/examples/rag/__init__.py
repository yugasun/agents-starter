import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.memory.chromadb import (
    ChromaDBVectorMemory,
    PersistentChromaDBVectorMemoryConfig,
)
from .indexer import SimpleDocumentIndexer
from ...llm.client import model_client


async def init_indexes():
    # Initialize vector memory
    rag_memory = ChromaDBVectorMemory(
        config=PersistentChromaDBVectorMemoryConfig(
            collection_name="autogen_docs",
            persistence_path=os.path.join(os.getcwd(), ".chromadb_autogen"),
            k=3,  # Return top 3 results
            score_threshold=0.4,  # Minimum similarity score
        )
    )

    await rag_memory.clear()  # Clear existing memory

    # Index AutoGen documentation
    async def index_autogen_docs() -> None:
        indexer = SimpleDocumentIndexer(memory=rag_memory)
        sources = [
            "https://raw.githubusercontent.com/microsoft/autogen/main/README.md",
            # "https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/agents.html",
            # "https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/teams.html",
            # "https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/termination.html",
        ]
        chunks: int = await indexer.index_documents(sources)
        print(f"Indexed {chunks} chunks from {len(sources)} AutoGen documents")

    await index_autogen_docs()

    return rag_memory


async def run():
    rag_memory = await init_indexes()
    # Create our RAG assistant agent
    rag_assistant = AssistantAgent(
        name="rag_assistant", model_client=model_client, memory=[rag_memory]
    )

    # Ask questions about AutoGen
    stream = rag_assistant.run_stream(task="What is AgentChat?")
    await Console(stream)

    # Remember to close the memory when done
    await rag_memory.close()
