# Workflow: scrape_google_maps

## Description
Scrapes business leads from Google Maps based on a service category and location.

## Inputs
- `service` (string): The type of business (e.g., "plumber", "coffee shop").
- `city` (string): The location to search in (e.g., "Miami", "Toronto").
- `count` (int): The exact number of leads to return.

## Outputs
Returns a list of dictionaries, each representing a lead with the following fields:
- `name`: Business name.
- `service`: The service type.
- `address`: Full address.
- `website`: URL (if available).
- `rating`: Customer rating (if available).
- `date_created`: Timestamp of when the data was scraped.
- `status`: Default is "lead".

## Execution
Run the matching Python script: `execution/scrape_google_maps.py`.
