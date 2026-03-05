import os
import json
from scrape_google_maps import scrape_google_maps
from airtable_save_leads import airtable_save_leads
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_integration():
    print("--- Starting End-to-End Test ---")
    
    service = "coffee shop"
    city = "Kandivali"
    count = 2
    
    print(f"1. Scraping up to {count} '{service}' in '{city}'...")
    leads = scrape_google_maps(service, city, count)
    
    if not leads:
        print("No leads found. Exiting.")
        return
        
    print(f"\nExtracted {len(leads)} leads:")
    print(json.dumps(leads, indent=2))
    
    print("\n2. Pushing leads to Airtable...")
    saved_count = airtable_save_leads(leads)
    
    print(f"\n--- End-to-End Test Complete ---")
    print(f"Successfully saved {saved_count} leads to Airtable.")

if __name__ == "__main__":
    test_integration()
