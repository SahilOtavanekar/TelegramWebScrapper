# Workflow: airtable_pull_leads

## Description
Pulls business leads from a specified Airtable base and table based on dynamic filtering criteria. The results are sorted by rating (highest first) and limited to the requested number of records.

## Inputs
- `city` (string, optional): The city where the business is located (matches against the `address` field).
- `service` (string, optional): The type of service, e.g., "plumber", "coffee shop".
- `min_rating` (float, optional): The minimum rating of the business.
- `status` (string, optional): The status of the lead, e.g., "confirmed", "pending".
- `limit` (int, default: 10): The maximum number of records to return.

## Outputs
- Returns a list of dictionaries, where each dictionary represents a lead containing the fields from Airtable.
- If no records match, an empty list is returned.

## Requirements
- `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, and `AIRTABLE_TABLE_NAME` must be set in `.env` or Modal secrets.
- The Airtable table must have the exact column names: `Name`, `service`, `address`, `website`, `rating`, `date_created`, and `status`.

## Execution
Run the matching Python script: `execution/airtable_pull_leads.py`.
You can pass arguments to the script programmatically via the `pull_airtable_leads(city, service, min_rating, status, limit)` function.
