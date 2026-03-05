# Workflow: airtable_save_leads

## Description
Uploads business leads to a specified Airtable base and table.

## Inputs
- `leads` (list of dicts): A list of lead objects containing:
  - `name`
  - `service`
  - `address`
  - `website`
  - `rating`
  - `date_created`
  - `status`

## Outputs
- Returns the number of successfully uploaded records.

## Requirements
- Columns in Airtable must match the field names exactly.
- `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, and `AIRTABLE_TABLE_NAME` must be set in `.env` or Modal secrets.

## Execution
Run the matching Python script: `execution/airtable_save_leads.py`.
