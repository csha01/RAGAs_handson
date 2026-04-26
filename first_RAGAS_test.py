# first_ragas_test.py — RAGAs with Ollama (free, local, no API key)

# REPLACE WITH THIS
from datasets import Dataset
from ragas import evaluate
from ragas import RunConfig
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)
# REPLACE WITH THIS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

llm = LangchainLLMWrapper(ChatOllama(
    model="llama3",
    temperature=0,
))

embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(
    model="llama3",
))
# ---------------------------------------------------------------
# EVAL DATASET — 3 test cases
# Row 2 is hallucinated — watch Faithfulness catch it
# ---------------------------------------------------------------

data = {
    "question": [
        "What is the leave policy for employees?",
        "How many days can I work from home?",
        "When are performance reviews held?",
    ],
    "answer": [
        # Row 1: GOOD — grounded in context
        "Employees are entitled to 18 days of paid annual leave per year.",

        # Row 2: HALLUCINATED — ignores retrieved context
        "Employees can work from home 5 days a week with no restrictions.",

        # Row 3: GOOD — matches context
        "Performance reviews are conducted twice a year in June and December.",
    ],
    "contexts": [
        ["All full-time employees are entitled to 18 days of paid annual leave per year. "
         "Leave must be approved by your manager at least 7 days in advance."],

        ["Employees may work from home up to 2 days per week with manager approval. "
         "All remote work must be conducted during core hours of 10am to 4pm."],

        ["Performance Reviews are conducted twice a year — in June and December. "
         "Employees self-assess using the company portal before the manager review."],
    ],
    "ground_truth": [
        "Full-time employees get 18 days of paid annual leave per year.",
        "Employees can work from home up to 2 days per week with manager approval.",
        "Performance reviews are held twice a year in June and December.",
    ],
}

# ---------------------------------------------------------------
# BUILD DATASET AND EVALUATE
# ---------------------------------------------------------------

dataset = Dataset.from_dict(data)

print("Running RAGAs with Ollama (local LLM)...")
print("This may take 1-3 minutes depending on your machine...\n")

result = evaluate(
    dataset=dataset,
    metrics=[
        Faithfulness(llm=llm),
        AnswerRelevancy(llm=llm, embeddings=embeddings),
        ContextPrecision(llm=llm),
        ContextRecall(llm=llm),
    ],
    run_config=RunConfig(
        timeout=180,        # wait up to 3 minutes per call
        max_retries=3,      # retry failed calls
        max_workers=1,      # run one at a time — safer for local Ollama
    ),
)

# ---------------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------------

# REPLACE WITH THIS
def avg(val):
    if isinstance(val, list):
        valid = [v for v in val if v is not None]
        return sum(valid) / len(valid) if valid else 0.0
    return float(val)

print(f"  Faithfulness       : {avg(result['faithfulness']):.3f}")
print(f"  Answer Relevancy   : {avg(result['answer_relevancy']):.3f}")
print(f"  Context Precision  : {avg(result['context_precision']):.3f}")
print(f"  Context Recall     : {avg(result['context_recall']):.3f}")

print("\n===== WHAT TO OBSERVE =====")
print("  Row 2 answer is hallucinated (says 5 days, context says 2 days).")
print("  Faithfulness should be the lowest scoring metric.")
print("  Context Precision/Recall stay high — retrieval was correct.")
print("  The LLM failed, not the retriever.")