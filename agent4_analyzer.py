import json
from collections import Counter

def load_use_cases(file_path="use_cases.json"):
    """Load use cases from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("Use_Cases", [])

def analyze_use_cases(use_cases):
    """Analyze use cases to get counts by category and aggregate importance."""
    category_counts = Counter()
    importance_texts = []

    for case in use_cases:
        category = case.get("Category", "Unknown")
        category_counts[category] += 1
        
        why_it_matters = case.get("Why_It_Matters")
        if why_it_matters:
            importance_texts.append(f"- {case.get('Title')}: {why_it_matters}")

    return category_counts, importance_texts

def generate_report(category_counts, importance_texts):
    """Generate a textual report from the analysis."""
    report_lines = []
    report_lines.append("=== Use Case Analysis Report ===\n")
    report_lines.append("Use Cases Count by Category:\n")
    for category, count in category_counts.items():
        report_lines.append(f"  - {category}: {count}")
    report_lines.append("\nWhy These Use Cases Matter:\n")
    report_lines.extend(importance_texts)

    return "\n".join(report_lines)

def save_report(report, filename="use_case_report.txt"):
    """Save the generated report to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

def agent_4_analyze_and_report():
    use_cases = load_use_cases()
    if not use_cases:
        print("No use cases found to analyze.")
        return

    category_counts, importance_texts = analyze_use_cases(use_cases)
    report = generate_report(category_counts, importance_texts)

    print(report) 
    save_report(report)
    print(f"\nReport saved to 'use_case_report.txt'")

if __name__ == "__main__":
    agent_4_analyze_and_report()
