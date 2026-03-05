import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from pyairtable import Api
from pyairtable.formulas import match

# Load environment variables
load_dotenv()

def airtable_save_leads(leads: List[Dict[str, Any]]) -> int:
    """
    Saves a list of leads to Airtable using the pyairtable SDK.
    """
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")

    if not all([api_key, base_id, table_name]):
        print("Error: Airtable configuration missing in environment variables.")
        return 0

    try:
        api = Api(api_key)
        table = api.table(base_id, table_name)
        
        # PyAirtable automatically batches creation in chunks of 10
        print(f"Attempting to upload {len(leads)} leads to Airtable Base '{base_id}', Table '{table_name}'...")
        
        # Verify permissions/existence by fetching a single record (if any) or simply accessing the table
        try:
           table.first()
        except Exception as e:
           print(f"Warning: Could not fetch initial records from table (might be empty or permissions issue): {e}")

        # 📝 Map local keys to exact Airtable Column Names based on the user's screenshot
        mapped_leads = []
        for lead in leads:
            raw_rating = lead.get("rating")
            parsed_rating = None
            if raw_rating and raw_rating != "N/A":
                try:
                    parsed_rating = float(raw_rating)
                except ValueError:
                    pass
            
            mapped_leads.append({
                "Name": lead.get("name"),
                "service": lead.get("service"),
                "address": lead.get("address"),
                "website": lead.get("website"),
                "rating": parsed_rating,
                "date_created": lead.get("date_created").split(" ")[0] if lead.get("date_created") else None,
                "status": "Lead" # Hardcode to capitalized 'Lead' since it's an Airtable Single Select
            })
            
        created_records = table.batch_create(mapped_leads)
        
        count = len(created_records)
        print(f"Successfully uploaded {count} leads.")
        return count
        
    except Exception as e:
        print(f"\n--- AIRTABLE ERROR ---")
        print(f"Failed to upload leads to Airtable.")
        print(f"Error Details: {e}")
        print("\nCommon Causes for 403 Forbidden / Not Found:")
        print("1. Token lacks 'data.records:write' permission.")
        print("2. Token is not explicitly granted access to this specific Base.")
        print(f"3. The table '{table_name}' does not exist exactly as spelled (case-sensitive).")
        print("4. One of the column names being pushed does not exist exactly in Airtable:")
        if leads:
            print(f"   Fields being pushed: {list(leads[0].keys())}")
        return 0

if __name__ == "__main__":
    test_leads = [
        {
            "name": "Test Coffee Shop",
            "service": "coffee shop",
            "address": "123 Test St, Test City",
            "website": "https://test.com",
            "rating": "4.5",
            "date_created": "2026-03-04 18:04:00",
            "status": "confirmed"
        }
    ]
    
    print("Testing Airtable save workflow...")
    result = airtable_save_leads(test_leads)
    print(f"Total leads saved: {result}")
