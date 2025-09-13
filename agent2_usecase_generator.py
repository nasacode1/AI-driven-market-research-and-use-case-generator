import requests
import json

OPENROUTER_API_KEY = "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"

def generate_use_cases(company_summary_json):
    prompt = f"""
You are an AI industry consultant. Given the company overview below, generate a list of AI/ML/GenAI use cases they can implement.

Company Overview:
{company_summary_json}

Instructions:
1. Research recent AI trends in the company's industry.
2. Suggest practical, business-aligned use cases for:
   - Customer experience
   - Operational efficiency
   - Automation
   - Internal tools (e.g., search, reporting, chatbots)
3. Use this exact JSON format:

{{
  "Use_Cases": [
    {{
      "Title": "Predictive Inventory Management",
      "Description": "Use ML models to forecast inventory needs and reduce overstocking/understocking.",
      "Category": "Operations",
      "Why_It_Matters": "Improves supply chain efficiency and reduces costs."
    }},
    ...
  ]
}}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        print("API request failed:", e)
        return None

if __name__ == "__main__":
    try:
        with open("company_summary.json", "r") as f:
            company_summary = f.read()

        use_cases_json = generate_use_cases(company_summary)

        if use_cases_json:
            with open("use_cases.json", "w") as f:
                f.write(use_cases_json)

            print("\n✅ Use cases successfully generated and saved to use_cases.json")
            print("\n===== Generated Use Cases Preview =====\n")
            print(use_cases_json[:1000]) 

        else:
            print("❌ Failed to generate use cases.")

    except FileNotFoundError:
        print("❌ 'company_summary.json' not found. Please run Agent 1 first.")
