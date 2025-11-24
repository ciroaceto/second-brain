import sys
from src.agents.orchestrator_agent import process_query
from src.agents.ingestion_agent import ingest_file
from src.memory.mem0_adapter import get_all_memories
from src.evaluation.evals import run_evals
from src.evaluation.metrics import collector

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.cli.interface <command> [args]")
        print("Commands:")
        print("  ingest <file>  - Ingest PDF or text file")
        print("  query <question> - Ask a question")
        print("  chat - Interactive chat mode")
        print("  memory - View stored memories")
        print("  eval - Run evaluations")
        print("  metrics - View metrics")
        return
    
    command = sys.argv[1]
    
    if command == "ingest" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        result = ingest_file(file_path)
        print(f"Ingested: {result}")
    
    elif command == "query" and len(sys.argv) >= 3:
        question = " ".join(sys.argv[2:])
        response = process_query(question)
        print(f"\n{response}\n")
    
    elif command == "chat":
        print("Chat mode (type 'exit' to quit)")
        user_id = "default"
        while True:
            query = input("\nYou: ")
            if query.lower() == "exit":
                break
            response = process_query(query, user_id)
            print(f"\nAssistant: {response}\n")
    
    elif command == "memory":
        memories = get_all_memories("default")
        print(f"\nMemories ({len(memories)}):")
        for m in memories[:10]:
            print(f"  - {m.get('memory', '')[:100]}...")
    
    elif command == "eval":
        print("Running evaluations...")
        results = run_evals()
        print(f"\nEvaluation Results ({len(results)} test cases):")
        for i, result in enumerate(results, 1):
            print(f"\n  Case {i} - {result['name']}:")
            print(f"    Inputs: {result['case']}")
            print(f"    Expected: {result['expected']}")
            print(f"    Evaluators: {', '.join(result['evaluators'])}")
    
    elif command == "metrics":
        stats = collector.get_stats("process_query.latency")
        print(f"\nMetrics: {stats}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

