import requests
from bs4 import BeautifulSoup
import re
from knowledge_base import KnowledgeBase
from intent_recognizer import IntentRecognizer

class WebScraper:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.intent_recognizer = IntentRecognizer()
    
    def search_web(self, query):
        """
        Performs a web search and extracts useful content.
        """
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code != 200:
            return "Failed to retrieve search results."
        
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("h3")  # Extracts headlines from search results
        
        links = []
        for result in search_results[:5]:  # Limit to first 5 results
            parent = result.find_parent("a")
            if parent and parent.get("href"):
                links.append(parent.get("href"))
        
        return links if links else "No results found."
    
    def scrape_content(self, url):
        """
        Extracts meaningful content from a web page.
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return "Failed to retrieve the webpage."
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        
        text_content = " ".join([p.get_text() for p in paragraphs])
        return re.sub(r'\s+', ' ', text_content).strip()  # Clean up extra spaces
    
    def fetch_information(self, query):
        """
        Searches the web, scrapes relevant content, and stores key findings in the knowledge base.
        """
        print(f"Searching the web for: {query}")
        search_results = self.search_web(query)
        
        if isinstance(search_results, str):
            return search_results  # Return error message if search failed
        
        for url in search_results:
            content = self.scrape_content(url)
            if content:
                self.knowledge_base.add_fact("WebScraped", query, content[:500])  # Store only first 500 chars for summary
                return f"Information retrieved and stored: {content[:200]}..."
        
        return "No relevant information could be extracted."
    
if __name__ == "__main__":
    scraper = WebScraper()
    
    test_queries = [
        "Latest AI advancements",
        "How does machine learning work?",
        "Python programming basics"
    ]
    
    for query in test_queries:
        print(scraper.fetch_information(query))