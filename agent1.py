import requests

OPENROUTER_API_KEY = "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"
SERPER_API_KEY = "15e1acb454a0e06a63970582f5ac4dd9c3c99a91"

def web_search(query, api_key):
    url = f"https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
    }
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    results = []
    for item in data.get('organic', []):
        results.append(item.get('snippet', ''))
    return " ".join(results[:5])

def generate_company_summary(text):
    prompt = f"""
You are an expert market analyst. Given the following text about a company, extract:
1. Industry (sector)
2. Key Offerings (products or services)
3. Strategic Focus Areas (like supply chain, customer experience, etc.)

Text:
\"\"\"{text}\"\"\"

Provide your answer in this JSON format:

{{
    "Industry": "...",
    "Key_Offerings": ["...", "..."],
    "Strategic_Focus_Areas": ["...", "..."]
}}
"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']

def agent_1_company_research(company_name):
    print(f"Searching web for company info about: {company_name} ...")
    query = f"{company_name} company overview, industry, products, strategy"
    search_text = web_search(query, SERPER_API_KEY)
    
    print("Raw search info collected:")
    print(search_text[:1000])
    
    print("\nGenerating structured company summary...")
    summary = generate_company_summary(search_text)
    
    return summary

if __name__ == "__main__":
    company = input("Enter company name: ")
    summary = agent_1_company_research(company)
    print("\n===== Company Summary =====")
    print(summary)
