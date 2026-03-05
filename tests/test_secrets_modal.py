import modal
import os

app = modal.App("test-airtable-secrets")

@app.function(secrets=[modal.Secret.from_name("telegram-bot-secrets")])
def check_secrets():
    print("AIRTABLE_API_KEY:", "Set" if os.environ.get("AIRTABLE_API_KEY") else "Missing")
    print("AIRTABLE_BASE_ID:", "Set" if os.environ.get("AIRTABLE_BASE_ID") else "Missing")
    print("AIRTABLE_TABLE_NAME:", "Set" if os.environ.get("AIRTABLE_TABLE_NAME") else "Missing")

@app.local_entrypoint()
def main():
    check_secrets.remote()
