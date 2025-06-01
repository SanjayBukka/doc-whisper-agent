
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
from utils.logger import get_logger

class MoEngageScraper:
    """Scraper specifically designed for MoEngage documentation sites"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_url(self, url):
        """Scrape a MoEngage documentation URL and extract structured content"""
        
        try:
            self.logger.info(f"Scraping URL: {url}")
            
            # Make request with retry logic
            response = self._make_request_with_retry(url)
            if not response:
                return {'error': 'Failed to fetch URL after retries'}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract structured data
            scraped_data = {
                'url': url,
                'title': self._extract_title(soup),
                'content': self._extract_main_content(soup),
                'headings': self._extract_headings(soup),
                'paragraphs': self._extract_paragraphs(soup),
                'images': self._extract_images(soup),
                'links': self._extract_links(soup),
                'code_blocks': self._extract_code_blocks(soup),
                'lists': self._extract_lists(soup),
                'metadata': self._extract_metadata(soup),
                'scraped_at': time.time()
            }
            
            # Validate scraped content
            if not scraped_data['content'] or len(scraped_data['content']) < 100:
                return {'error': 'Insufficient content extracted'}
            
            self.logger.info(f"Successfully scraped {len(scraped_data['content'])} characters")
            return scraped_data
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return {'error': str(e)}
    
    def _make_request_with_retry(self, url, max_retries=3):
        """Make HTTP request with retry logic"""
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
                
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"All attempts failed for {url}")
                    return None
    
    def _extract_title(self, soup):
        """Extract document title"""
        
        # Try multiple selectors for title
        selectors = [
            'h1.article-title',
            'h1.page-title', 
            '.article-header h1',
            'h1',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "No title found"
    
    def _extract_main_content(self, soup):
        """Extract main article content"""
        
        # Try multiple selectors for main content
        content_selectors = [
            '.article-body',
            '.article-content',
            '.post-content',
            '.content-body',
            '.main-content',
            'main',
            '.content',
            'article'
        ]
        
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                # Remove script, style, and navigation elements
                for element in content_div.find_all(['script', 'style', 'nav', 'header', 'footer']):
                    element.decompose()
                
                # Get text content
                text = content_div.get_text(separator=' ', strip=True)
                # Clean up whitespace
                text = re.sub(r'\s+', ' ', text)
                return text
        
        # Fallback: extract all paragraph text
        paragraphs = soup.find_all('p')
        if paragraphs:
            text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            return re.sub(r'\s+', ' ', text)
        
        return ""
    
    def _extract_headings(self, soup):
        """Extract document headings with hierarchy"""
        
        headings = []
        for level in range(1, 7):  # h1 to h6
            for heading in soup.find_all(f'h{level}'):
                headings.append({
                    'level': level,
                    'text': heading.get_text(strip=True),
                    'id': heading.get('id', ''),
                    'class': heading.get('class', [])
                })
        
        return headings
    
    def _extract_paragraphs(self, soup):
        """Extract all paragraphs"""
        
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 10:  # Filter out very short paragraphs
                paragraphs.append({
                    'text': text,
                    'word_count': len(text.split()),
                    'char_count': len(text)
                })
        
        return paragraphs
    
    def _extract_images(self, soup):
        """Extract image information"""
        
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src:
                images.append({
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', '')
                })
        
        return images
    
    def _extract_links(self, soup):
        """Extract all links"""
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            if text:  # Only include links with text
                links.append({
                    'href': href,
                    'text': text,
                    'title': link.get('title', ''),
                    'is_external': not href.startswith('/') and 'moengage.com' not in href
                })
        
        return links
    
    def _extract_code_blocks(self, soup):
        """Extract code blocks and inline code"""
        
        code_blocks = []
        
        # Extract <pre><code> blocks
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                code_blocks.append({
                    'type': 'block',
                    'text': code.get_text(),
                    'language': self._detect_code_language(code)
                })
            else:
                code_blocks.append({
                    'type': 'block',
                    'text': pre.get_text(),
                    'language': 'unknown'
                })
        
        # Extract standalone <code> elements
        for code in soup.find_all('code'):
            if not code.find_parent('pre'):  # Avoid duplicates
                code_blocks.append({
                    'type': 'inline',
                    'text': code.get_text(strip=True),
                    'language': self._detect_code_language(code)
                })
        
        return code_blocks
    
    def _extract_lists(self, soup):
        """Extract ordered and unordered lists"""
        
        lists = []
        
        for list_element in soup.find_all(['ul', 'ol']):
            items = []
            for li in list_element.find_all('li', recursive=False):
                items.append(li.get_text(strip=True))
            
            if items:
                lists.append({
                    'type': 'ordered' if list_element.name == 'ol' else 'unordered',
                    'items': items,
                    'item_count': len(items)
                })
        
        return lists
    
    def _extract_metadata(self, soup):
        """Extract page metadata"""
        
        metadata = {}
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # Extract other useful information
        metadata.update({
            'total_words': len(self._extract_main_content(soup).split()),
            'total_headings': len(self._extract_headings(soup)),
            'total_paragraphs': len(self._extract_paragraphs(soup)),
            'total_images': len(self._extract_images(soup)),
            'total_links': len(self._extract_links(soup)),
            'total_code_blocks': len(self._extract_code_blocks(soup))
        })
        
        return metadata
    
    def _detect_code_language(self, code_element):
        """Try to detect programming language from code element"""
        
        # Check class attributes for language hints
        classes = code_element.get('class', [])
        for cls in classes:
            if cls.startswith('language-'):
                return cls.replace('language-', '')
            elif cls in ['javascript', 'python', 'java', 'css', 'html', 'json', 'xml']:
                return cls
        
        # Simple content-based detection
        content = code_element.get_text().strip()
        if content.startswith('{') and content.endswith('}'):
            return 'json'
        elif 'function' in content or 'var ' in content:
            return 'javascript'
        elif 'def ' in content or 'import ' in content:
            return 'python'
        
        return 'unknown'
