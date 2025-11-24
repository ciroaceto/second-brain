from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Contains, LLMJudge
from src.agents.orchestrator_agent import process_query
from src.rag.vector_store import search
from src.config import ANTHROPIC_API_KEY, MODEL

def eval_retrieval_accuracy(query: str, expected_content: str):
    """Evaluate retrieval accuracy using pydantic_evals."""
    results = search(query, n_results=5)
    retrieved_texts = [r["text"] for r in results]
    combined_text = " ".join(retrieved_texts)
    
    # Check if expected content is in retrieved results
    case = Case(
        inputs={"query": query},
        expected_output=expected_content,
        evaluators=(Contains(value=expected_content),),
    )
    
    return case, combined_text

def eval_response_quality_llm(query: str, expected_criteria: str):
    """Evaluate response quality using LLM judge."""
    response = process_query(query)
    
    # Use LLM to judge response quality
    case = Case(
        inputs={"query": query},
        expected_output=response,
        evaluators=(
            LLMJudge(
                model=f"anthropic:{MODEL}",
                criteria=expected_criteria,
                api_key=ANTHROPIC_API_KEY,
            ),
        ),
    )
    
    return case, response

def create_eval_dataset():
    """Create evaluation dataset with test cases."""
    cases = [
        Case(
            name="retrieval_test",
            inputs={"query": "test query"},
            expected_output="expected content",
            evaluators=(Contains(value="expected"),),
        ),
        Case(
            name="ai_query_test",
            inputs={"query": "What is AI?"},
            expected_output="artificial intelligence",
            evaluators=(Contains(value="intelligence"),),
        ),
    ]
    
    return Dataset(cases=cases, name="second_brain_evals")

def run_evals():
    """Run evaluation suite."""
    # Create simple evaluation dataset
    dataset = create_eval_dataset()
    
    results = []
    for case in dataset.cases:
        # Simulate evaluation
        results.append({
            "name": case.name,
            "case": case.inputs,
            "expected": case.expected_output,
            "evaluators": [type(e).__name__ for e in case.evaluators]
        })
    
    return results

