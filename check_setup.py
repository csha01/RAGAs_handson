# check_setup.py — run this to confirm everything is ready

print("Checking RAGAs setup...\n")

try:
    import ragas
    print(f"✓ ragas {ragas.__version__}")
except ImportError as e:
    print(f"✗ ragas — {e}")

try:
    from ragas.metrics.collections import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    )
    print("✓ all 4 metrics imported")
except ImportError as e:
    print(f"✗ metrics — {e}")

try:
    from datasets import Dataset
    print("✓ datasets")
except ImportError as e:
    print(f"✗ datasets — {e}")

try:
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    print("✓ langchain_openai")
except ImportError as e:
    print(f"✗ langchain_openai — {e}")

print("\nSetup complete — you are ready to run RAGAs!")