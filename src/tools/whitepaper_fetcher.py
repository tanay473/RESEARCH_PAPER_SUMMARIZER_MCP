import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from src.utils.helpers import safe_get_href

def fetch_white_papers(company: str, keywords: str, max_results: int = 3) -> List[Dict[str, str]]:
    company_urls = {
        "deepmind": "https://deepmind.google/research/publications/",
        "meta": "https://research.facebook.com/publications/",
        "nvidia": "https://www.amax.com/nvidia-technical-whitepapers/",
        "openai": "https://openai.com/research/",
        "ibm": "https://community.ibm.com/community/user/blogs/armand-ruiz-gabernet/2024/06/24/ibm-granite-large-language-models-whitepaper"
    }
    url = company_urls.get(company.lower())
    if not url:
        return [{"error": f"No URL found for company: {company}"}]

    response = requests.get(url)
    if response.status_code != 200:
        return [{"error": f"Failed to fetch data from {url}"}]

    soup = BeautifulSoup(response.text, 'html.parser')
    papers = []
    for link in soup.find_all('a', href=True)[:max_results]:
        title = link.text.strip()
        href = safe_get_href(link)
        if keywords.lower() in title.lower():
            papers.append({
                "title": title,
                "url": href if href.startswith("http") else url + href,
                "summary": "Summary not directly available; fetch PDF for details."
            })
    return papers or [{"note": f"No matching papers found for '{keywords}' on {company}"}]
