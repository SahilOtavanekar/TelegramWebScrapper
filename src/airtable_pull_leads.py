import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pyairtable import Api

# Load environment variables
load_dotenv()

def pull_airtable_leads(
    city: Optional[str] = None,
    service: Optional[str] = None,
    min_rating: Optional[float] = None,
    status: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Pulls a list of leads from Airtable based on filter criteria.
    Results are sorted by rating (highest first) and limited to the given 'limit'.
    """
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")

    if not all([api_key, base_id, table_name]):
        print("Error: Airtable configuration missing in environment variables.")
        return []

    try:
        api = Api(api_key)
        table = api.table(base_id, table_name)
        
        # Build the pyairtable formula 
        # Refer to https://pyairtable.readthedocs.io/en/latest/formulas.html
        filters = []
        
        if city:
            # Case-insensitive search of city within the address field
            # Example: FIND(LOWER('Kandivali'), LOWER({address})) > 0
            filters.append(f"FIND(LOWER('{city}'), LOWER({{address}})) > 0")
            
        if service:
            # Case-insensitive match for service
            # Example: LOWER({service}) = LOWER('plumber')
            filters.append(f"LOWER({{service}}) = LOWER('{service}')")
            
        if min_rating is not None:
            # Rating greater than or equal to min_rating
            filters.append(f"{{rating}} >= {min_rating}")
            
        if status:
            # Exact match for status
            filters.append(f"{{status}} = '{status}'")
            
        if filters:
            # Join all conditions with AND()
            formula_str = f"AND({', '.join(filters)})"
        else:
            formula_str = None

        print(f"Fetching up to {limit} leads from Airtable Base '{base_id}', Table '{table_name}'...")
        if formula_str:
            print(f"Applying formula: {formula_str}")
        else:
            print("No filters applied. Fetching all available records up to the limit.")

        # table.all() uses max_records instead of limit, but max_records limits the total results returned
        # Fetching sorting by rating descending ("-rating")
        records = table.all(
            formula=formula_str,
            sort=["-rating"],
            max_records=limit
        )
        
        # Extract fields from PyAirtable's return format
        results = [record["fields"] for record in records]
        
        print(f"Successfully pulled {len(results)} leads.")
        return results

    except Exception as e:
        print(f"\n--- AIRTABLE ERROR ---")
        print(f"Failed to pull leads from Airtable.")
        print(f"Error Details: {e}")
        return []

if __name__ == "__main__":
    import json
    
    print("Testing Airtable pull workflow...")
    
    # Test case: Plumbers in Kandivali with a rating >= 4, limit 2
    test_results = pull_airtable_leads(
        city="Kandivali",
        service="plumber",
        min_rating=4.0,
        limit=2
    )
    
    print("\n--- Test Results ---")
    print(json.dumps(test_results, indent=2))
