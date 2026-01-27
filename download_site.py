#!/usr/bin/env python3
import os
import re
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
from bs4 import BeautifulSoup

base_url = "https://html.awaikenthemes.com/nextmind/ai-image/"
output_dir = "/Users/abidev/dev/gritsa/template"
downloaded = set()
pages_to_crawl = set()

def get_local_path(url, base_url):
    """Convert a URL to a local file path"""
    parsed = urlparse(url)
    path = parsed.path
    
    # Remove the /nextmind/ai-image/ prefix
    if path.startswith('/nextmind/ai-image/'):
        path = path[len('/nextmind/ai-image/'):]
    elif path.startswith('/nextmind/'):
        path = 'nextmind/' + path[len('/nextmind/'):]
    
    # If it's just a directory, add index.html
    if path.endswith('/') or path == '':
        path += 'index.html'
    
    return path

def download_file(url, local_path):
    """Download a file and save it to local path"""
    if url in downloaded:
        return
    
    try:
        print(f"Downloading: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create directory if needed
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        downloaded.add(url)
        print(f"  -> Saved to: {local_path}")
        return response.content
    except Exception as e:
        print(f"  -> Error: {e}")
        return None

def process_html(html_content, page_url, local_html_path):
    """Process HTML to find and download all assets"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all resource links
    for tag in soup.find_all(['link', 'script', 'img', 'source', 'video', 'audio']):
        attr = None
        if tag.name == 'link':
            attr = 'href'
        elif tag.name == 'script':
            attr = 'src'
        elif tag.name in ['img', 'source', 'video', 'audio']:
            attr = 'src'
        
        if attr and tag.get(attr):
            resource_url = tag[attr]
            
            # Skip external resources (except fonts.googleapis.com)
            if resource_url.startswith('http'):
                if 'awaikenthemes.com' not in resource_url and 'fonts.g' not in resource_url:
                    continue
                full_url = resource_url
            else:
                full_url = urljoin(page_url, resource_url)
            
            # Download if it's from the same site
            if 'awaikenthemes.com/nextmind' in full_url:
                local_resource_path = os.path.join(output_dir, get_local_path(full_url, base_url))
                download_file(full_url, local_resource_path)
                
                # Update the tag to use local path
                relative_path = os.path.relpath(local_resource_path, os.path.dirname(local_html_path))
                tag[attr] = relative_path
    
    # Find all page links for crawling
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href.startswith('http'):
            full_url = urljoin(page_url, href)
        else:
            full_url = href
        
        # Only crawl pages from the same site
        if 'awaikenthemes.com/nextmind/ai-image' in full_url and full_url.endswith('.html'):
            if full_url not in downloaded:
                pages_to_crawl.add(full_url)
                print(f"  -> Found page to crawl: {full_url}")
    
    # Save modified HTML
    with open(local_html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  -> Updated HTML saved")

def crawl_site():
    """Main function to crawl the site"""
    # Start with the index page
    index_url = base_url + "index.html"
    pages_to_crawl.add(index_url)
    
    while pages_to_crawl:
        page_url = pages_to_crawl.pop()
        
        if page_url in downloaded:
            continue
        
        print(f"\n{'='*60}")
        print(f"Crawling page: {page_url}")
        print(f"{'='*60}")
        
        local_path = os.path.join(output_dir, get_local_path(page_url, base_url))
        content = download_file(page_url, local_path)
        
        if content and page_url.endswith('.html'):
            process_html(content, page_url, local_path)

if __name__ == "__main__":
    print(f"Starting crawl of {base_url}")
    print(f"Output directory: {output_dir}")
    crawl_site()
    print(f"\n{'='*60}")
    print(f"Crawl complete! Downloaded {len(downloaded)} files.")
    print(f"{'='*60}")
