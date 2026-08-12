import requests
from html.parser import HTMLParser
from urllib.parse import urlparse
import json

class DuckDuckGoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_tag = None
        self.in_result = False
        self.in_title = False
        self.in_snippet = False
        
        self.current_title = ""
        self.current_link = ""
        self.current_snippet = ""
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        if tag == 'a' and 'class' in attrs_dict and 'result__url' in attrs_dict['class']:
            self.in_result = True
            self.current_link = attrs_dict.get('href', '')
            if self.current_link.startswith('//duckduckgo.com/l/?uddg='):
                from urllib.parse import unquote
                self.current_link = unquote(self.current_link.split('uddg=')[1].split('&')[0])
                
        elif tag == 'a' and 'class' in attrs_dict and 'result__snippet' in attrs_dict['class']:
            self.in_snippet = True
            
        elif tag == 'h2' and 'class' in attrs_dict and 'result__title' in attrs_dict['class']:
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'a' and self.in_result and getattr(self, 'current_link', ''):
            pass # Link captured
        elif tag == 'a' and self.in_snippet:
            self.in_snippet = False
        elif tag == 'h2' and self.in_title:
            self.in_title = False
            
    def handle_data(self, data):
        data = data.strip()
        if not data: return
        
        if self.in_title:
            self.current_title += data
        elif self.in_snippet:
            self.current_snippet += data + " "
            
        # We assume snippet comes last in DDG HTML layout usually
        if self.in_snippet and len(self.current_title) > 0 and len(self.current_link) > 0:
            if not any(r['link'] == self.current_link for r in self.results):
                self.results.append({
                    "title": self.current_title.strip(),
                    "link": self.current_link.strip(),
                    "snippet": self.current_snippet.strip()
                })

def perform_web_search(query: str, max_results: int = 5) -> str:
    """
    Perform a free web search using DuckDuckGo HTML version.
    Zero-setup, no API key required.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        response = requests.get(url, headers=headers, timeout=10)
        
        parser = DuckDuckGoParser()
        parser.feed(response.text)
        
        results = parser.results[:max_results]
        
        if not results:
            return json.dumps({"error": "No results found or rate limited by search engine."})
            
        return json.dumps({"query": query, "results": results}, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


def read_url_text(url: str) -> str:
    """
    Fetch a URL and extract text content using built-in HTML parsing.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.hide_tags = {'script', 'style', 'head', 'nav', 'footer', 'header'}
                self.hide = False
                
            def handle_starttag(self, tag, attrs):
                if tag in self.hide_tags:
                    self.hide = True
                    
            def handle_endtag(self, tag):
                if tag in self.hide_tags:
                    self.hide = False
                    
            def handle_data(self, data):
                if not self.hide:
                    cleaned = data.strip()
                    if cleaned:
                        self.text.append(cleaned)
                        
        extractor = TextExtractor()
        extractor.feed(response.text)
        
        content = "\n".join(extractor.text)
        return content[:15000] # Return max 15k chars to prevent context overflow
        
    except Exception as e:
        return f"Error reading URL: {str(e)}"
