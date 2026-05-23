from dotenv import load_dotenv
load_dotenv()
import os
import requests
from rich import print
from langchain_core.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup



client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_search(query:str)->str:
    """search the web for recent and reliable information on a topic, Returns Titles,URL,snnipet"""
    response=client.search(
        query=query,
        search_depth="basic",
        max_results=3
    )

    if not response['results']:
        return(f"no any content about {query}")
    search_list=[]
    for item in response["results"]:
        search_list.append(
            f"""
title={item['title']}
url={item['url']}
content={item['content'][:300]}
            """
        )

    return "\n".join(search_list)

tool
def scarp_url(url: str) -> str:
    """Scrape and return clean text content from the given URL for deeper reading."""
    
    try:
        res = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        scrap = BeautifulSoup(res.text, "html.parser")

        for tag in scrap(["script", "style", "nav", "footer"]):
            tag.decompose()

        return scrap.get_text(separator=" ", strip=True)[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"





