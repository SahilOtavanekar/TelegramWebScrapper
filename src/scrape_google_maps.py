import os
import json
import csv
import time
from datetime import datetime
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright

def scrape_google_maps(service: str, city: str, count: int) -> List[Dict[str, Any]]:
    count = int(count)  # Ensure count is an integer to prevent slice TypeErrors
    print(f"Scraping up to {count} '{service}' leads in {city} via Playwright...")
    leads = []
    
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US"
        )
        page = context.new_page()
        
        search_query = f"{service} in {city}".replace(" ", "+")
        
        print(f"Navigating to: https://www.google.com/maps/search/{search_query}")
        page.goto(f"https://www.google.com/maps/search/{search_query}", timeout=60000, wait_until="domcontentloaded")
        
        # Bypass EU/Google consent screens if they appear in headless Mode
        try:
            accept_btn = page.locator('button:has-text("Accept all"), button:has-text("I agree")')
            if accept_btn.count() > 0:
                print("Consent screen detected, accepting...")
                accept_btn.first.click()
                page.wait_for_timeout(2000)
        except Exception:
            pass
            
        # Wait for the results to load
        try:
            page.wait_for_selector('div[role="feed"]', timeout=15000)
        except Exception:
            print(f"Failed to find results feed. Page Title: '{page.title()}'")
            print("It might be a direct place page, consent dialog blocking, or a headless block.")
            
            # Check if we landed directly on a single place page instead of a list
            if page.locator('h1').count() > 0:
                print("Landed on a single place page directly! Extracting...")
                name = page.locator('h1').first.inner_text()
                leads.append({
                    "name": name,
                    "service": service,
                    "address": city, # Address might be harder to grab generically here, Defaulting to City
                    "website": "",
                    "rating": "N/A",
                    "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "lead"
                })
            
            browser.close()
            return leads

        # Find all result links
        unique_links = []
        feed_locator = page.locator('div[role="feed"]')
        
        # Scroll to load enough results
        while True:
            links = page.locator('div[role="feed"] a[href*="/maps/place/"]').all()
            for link in links:
                href = link.get_attribute("href")
                if href and href not in unique_links:
                    unique_links.append(href)
                    
            if len(unique_links) >= count or len(unique_links) >= 20: 
                break
            
            # Scroll down
            feed_locator.evaluate("node => node.scrollTo(0, node.scrollHeight)")
            page.wait_for_timeout(2000)

        print(f"Found {len(unique_links)} potential leads. Extracting details...")
        
        for url in unique_links[:count]:
            try:
                detail_page = context.new_page()
                detail_page.goto(url, timeout=30000)
                detail_page.wait_for_selector('h1', timeout=10000)
                
                # Extract Name
                name_elem = detail_page.locator('h1').first
                name = name_elem.inner_text() if name_elem.is_visible() else "Unknown"
                
                # Extract Address
                address_elem = detail_page.locator('button[data-item-id="address"]').first
                address = address_elem.inner_text().replace('\ue0c8', '').replace('\n', ' ').strip() if address_elem.is_visible() else "Unknown Address"
                
                # Extract Website
                website_elem = detail_page.locator('a[data-item-id="authority"]').first
                website = website_elem.get_attribute('href') if website_elem.is_visible() else ""
                
                # Extract Rating (Usually like "4.5 stars")
                rating_val = None
                rating_elem = detail_page.locator('span[aria-label*="stars"]').first
                if rating_elem.is_visible():
                    aria_label = rating_elem.get_attribute('aria-label')
                    if aria_label:
                        try:
                            rating_val = float(aria_label.split(" ")[0])
                        except:
                            pass
                            
                leads.append({
                    "name": name,
                    "service": service,
                    "address": address,
                    "website": website,
                    "rating": rating_val if rating_val is not None else "N/A",
                    "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "lead"
                })
                detail_page.close()
            except Exception as e:
                print(f"Failed to process {url}: {e}")
                
        browser.close()
        return leads

def save_to_csv(leads: List[Dict[str, Any]], filename: str):
    if not leads:
        print("No leads to save.")
        return
    
    keys = leads[0].keys()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(leads)
    print(f"Saved {len(leads)} leads to {filename}")

if __name__ == "__main__":
    TEST_SERVICE = "coffee shop"
    TEST_CITY = "Toronto"
    TEST_COUNT = 2
    
    results = scrape_google_maps(TEST_SERVICE, TEST_CITY, TEST_COUNT)
    output_path = os.path.join(".tmp", "test_leads.csv")
    save_to_csv(results, output_path)
    
    print(json.dumps(results, indent=2))
