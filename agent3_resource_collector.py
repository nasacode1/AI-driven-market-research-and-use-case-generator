import requests
import json
import urllib.parse
import re

SEARCH_ENGINE = "https://duckduckgo.com/html/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_datasets(query):
    results = []
    search_sites = ["kaggle.com", "huggingface.co", "github.com"]

    for site in search_sites:
        search_query = f"{query} site:{site}"
        params = {"q": search_query}
        try:
            res = requests.get(SEARCH_ENGINE, params=params, headers=HEADERS)
            if res.status_code == 200:
                links = extract_links(res.text)
                results.extend(links[:3])
        except Exception as e:
            print(f"[ERROR] Search failed for '{search_query}': {e}")
    return results

def extract_links(html):
    matches = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', html)
    links = []
    for url, title in matches:
        clean_title = re.sub('<.*?>', '', title).strip()
        clean_url = urllib.parse.unquote(url).strip()
        links.append((clean_title, clean_url))
    return links

def load_use_cases():
    with open("use_cases.json", "r", encoding="utf-8") as f:
        return json.load(f)["Use_Cases"]

def save_to_markdown(enriched_data):
    with open("resources.md", "w", encoding="utf-8") as f:
        f.write("AI/ML Resource Links for Use Cases\n\n")
        for case in enriched_data:
            f.write(f"## 🔹 {case['Title']}\n")
            f.write(f"**Category:** {case.get('Category', 'N/A')}\n\n")
            f.write(f"**Description:** {case['Description']}\n\n")
            f.write(f"**Why It Matters:** {case.get('Why_It_Matters', '')}\n\n")
            f.write("**Resources:**\n")
            if case['Resources']:
                for title, url in case['Resources']:
                    f.write(f"- [{title}]({url})\n")
            else:
                f.write("- No resources found.\n")
            f.write("\n---\n\n")

def agent_3_collect_resources():
    use_cases = load_use_cases()
    enriched = []

    print(f"\n11 Searching for resources for {len(use_cases)} use cases...\n")

    for case in use_cases:
        search_query = f"{case['Title']} {case['Description']} {case.get('Why_It_Matters', '')}"
        print(f"Searching for: {case['Title']}")
        resources = search_datasets(search_query)
        case['Resources'] = resources
        enriched.append(case)

    save_to_markdown(enriched)
    print("\n Done! Results saved to: `resources.md`\n")

if __name__ == "__main__":
    agent_3_collect_resources()
