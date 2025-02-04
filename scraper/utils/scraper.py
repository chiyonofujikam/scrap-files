import os
from urllib.parse import urljoin, urlparse

import lxml
import requests
from bs4 import BeautifulSoup
from pyunpack import Archive


class WebsiteScraper:
    def __init__(self, base_url, output_dir='downloads', max_depth=3):
        """
        Initialize the web scraper

        :param base_url: The starting URL to scrape
        :param output_dir: Directory to save downloaded files
        :param max_depth: Maximum recursion depth
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.max_depth = max_depth
        self.visited_urls = set()

        os.makedirs(output_dir, exist_ok=True)

    def is_valid_url(self, url):
        """
        Check if the URL is valid and within the same domain

        :param url: URL to validate
        :return: Boolean indicating if URL is valid
        """
        try:
            parsed_base = urlparse(self.base_url)
            parsed_url = urlparse(url)
            
            return (
                parsed_url.scheme in ['http', 'https'] and 
                parsed_base.netloc == parsed_url.netloc
            )
        except Exception:
            return False

    def download_file(self, url):
        """
        Download file from given URL

        :param url: URL of the file to download
        :return: Path to downloaded file or None
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            filename = os.path.join(
                self.output_dir, 
                url.split('/')[-1].split('?t=')[0].replace(' ', '_'
                        ).replace('\n', ''
                        ).replace('?', ''
                        ).replace('%20', ' '
                        ).replace('/', '_'
                        ).replace(':', '_'
                        ).replace('#', '')
            )

            base, ext = os.path.splitext(filename)
            if ext not in {".pdf", ".docx", ".zip", ".xlsx", ".doc", ".7z", ".xls"}:
                return None

            filename = f"{base}{ext}"
            if os.path.exists(filename):
                return None

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if ext.replace('.', '') in {'zip', '7z'}:
                print(f"Decompression of {filename}")
                Archive(filename).extractall(self.output_dir)

            print(f"Downloaded: {url}")
            return filename

        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return None

    def scrape_page(self, url, current_depth=0):
        """
        Recursively scrape a page for files and links

        :param url: URL to scrape
        :param current_depth: Current recursion depth
        """
        if (url in self.visited_urls or 
            current_depth > self.max_depth):
            return

        self.visited_urls.add(url)

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml-xml") # 'html.parser')

            for article in soup.find_all('article'):
                if article.get('class') is not None:
                    continue

                for link in article.find_all('a', href=True):
                    full_link = urljoin(url, link['href'])

                    if self.is_valid_url(full_link):
                        self.download_file(full_link)

                    if current_depth < self.max_depth:
                        self.scrape_page(full_link, current_depth + 1)

                break

        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    def start_scraping(self):
        """
        Start the scraping process from base URL
        """
        print(f"Starting scrape of {self.base_url}")
        self.scrape_page(self.base_url)
        print("Scraping completed.")

if __name__ == "__main__":
    BASE_URL = r"https://www.era.europa.eu/domains/infrastructure/european-rail-traffic-management-system-ertms_en"
    
    scraper = WebsiteScraper(
        base_url=BASE_URL, 
        output_dir='downloads', 
        max_depth=10
    )
    
    scraper.start_scraping()
