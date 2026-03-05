# How to Create an Airtable Personal Access Token (PAT)

1. **Log in to Airtable**: Go to [airtable.com](https://airtable.com/).
2. **Open Personal Access Tokens**: Click on your profile icon in the top right, then select **Admin Panel** or go directly to [airtable.com/create/tokens](https://airtable.com/create/tokens).
3. **Create New Token**:
   - Click the **+ Create new token** button.
   - **Name**: e.g., "Telegram Lead Bot".
   - **Scopes**: Add the following scopes:
     - `data.records:read`
     - `data.records:write`
     - `schema.bases:read`
   - **Access**: Select the specific Base you want the bot to access (or "All current and future bases").
4. **Copy Token**: Click **Create token** and copy the resulting string immediately. **You will not be able to see it again.**
5. **Update .env**: Paste the token into your `.env` file:
   ```env
   AIRTABLE_API_KEY=YOUR_TOKEN_HERE
   ```
6. **Find Base & Table ID**:
   - Open your Airtable base in the browser.
   - The URL will look like: `https://airtable.com/appXXXXXXXXXXXXXX/tblYYYYYYYYYYYYYY/viwZZZZZZZZZZZZZZ`.
   - `appXXXXXXXXXXXXXX` is your **Base ID**.
   - `tblYYYYYYYYYYYYYY` is your **Table ID** (or just use the Table Name).
   - Add these to your `.env` as well.
