# Getting Your RapidAPI Key (Using GitHub)

## Step 1: Sign Up with GitHub
1. Go to **[RapidAPI.com](https://rapidapi.com)** in your browser
2. Click **"Sign Up"** button (top right)
3. Select **"Sign up with GitHub"** option
4. You'll be redirected to GitHub login
5. Log in with your GitHub credentials (or create a free GitHub account if you don't have one)
6. Authorize RapidAPI to access your GitHub profile
7. RapidAPI will create your account automatically

## Step 2: Find Your API Key
1. After signing up, you're in the RapidAPI Dashboard
2. Look for your **profile icon** (top right corner)
3. Click it and select **"API Keys"** or go to **https://rapidapi.com/settings/api-keys**
4. You'll see your default API key displayed
5. **Copy this key** (click the copy icon or select and copy)

Example of what your key looks like:
```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Step 3: Find an Internships API on RapidAPI
1. Click **"Browse APIs"** or go to **https://rapidapi.com/search/internship**
2. Search for **"internship"** or **"job board"**
3. Popular options:
   - **Internships API** - Real internship listings
   - **JSearch** - Job/internship search API
   - **Rapid Job Search** - Job listings API
4. Click on an API to view details
5. Click **"Subscribe to Test"** (usually free tier available)
6. Note the **Host** value (shown in API documentation)
   - Example: `internships-api.p.rapidapi.com`

## Step 4: Get Your API Host
1. In the API details page, look for "Request URL" or "Base URL"
2. The host is the domain part
   - Example from RapidAPI page: 
     ```
     https://internships-api.p.rapidapi.com/search
     ```
   - Host is: `internships-api.p.rapidapi.com`

## Step 5: Add to Your .env File
1. Open `backend/.env` in a text editor
2. Add your credentials:
   ```
   RAPID_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   RAPID_API_HOST=internships-api.p.rapidapi.com
   ```
3. Save the file
4. **Restart your backend server** for changes to take effect

## Step 6: Test Your Setup
Run this PowerShell command to test:
```powershell
curl.exe "http://localhost:8000/scrape/internships?query=internship&limit=5"
```

Expected response (if configured correctly):
```json
{
  "source": "RapidAPI Internships",
  "count": 5,
  "inserted": 5,
  "items": [
    {
      "title": "...",
      "company": "...",
      "location": "...",
      "saved": true,
      "skills": [...]
    }
  ]
}
```

## Troubleshooting

### "RAPID_API_KEY not configured"
- Check that `backend/.env` has `RAPID_API_KEY=your_key`
- Make sure it's not empty
- Restart the backend after editing `.env`
- Verify the key is copied correctly (no extra spaces)

### "RapidAPI request failed"
- Verify your API key is correct (copy from RapidAPI dashboard again)
- Check that you've subscribed to the API (click "Subscribe")
- Ensure your RapidAPI account has available API calls (free tier has limits)
- Check network connectivity

### "Failed to parse RapidAPI response"
- The API response format may differ from expected
- Try a different Internships/Job API from RapidAPI
- Some APIs return data in different field names

### No internships returned
- Try different query keywords: `"internship"`, `"graduate"`, `"entry level"`
- Increase the `limit` parameter: `/scrape/internships?query=internship&limit=50`
- Check RapidAPI API documentation for response format

## Finding Your API Key in RapidAPI Dashboard

Your dashboard should look like this:
```
┌─────────────────────────────────────────┐
│ RapidAPI Dashboard                      │
├─────────────────────────────────────────┤
│ Your Subscriptions                      │
│ - Internships API (subscribed)          │
│ - [Other APIs you subscribed to]        │
├─────────────────────────────────────────┤
│ Your Profile                            │
│ - API Keys                              │
│   Default Key: xxxxxxxxxx...           │
│   [Copy Button]                         │
└─────────────────────────────────────────┘
```

## Quick Copy-Paste Template

Once you have your key and host, use this template:

```powershell
# 1. Open your .env file
notepad C:\Users\ACER\Downloads\ai-internship-matcher\backend\.env

# 2. Add these lines (replace with YOUR actual values):
# RAPID_API_KEY=your_key_from_rapidapi_dashboard_here
# RAPID_API_HOST=internships-api.p.rapidapi.com

# 3. Save and close
# 4. Restart backend
```

## Common RapidAPI Internship/Job APIs

| API Name | Host | Free Tier |
|----------|------|-----------|
| Internships API | `internships-api.p.rapidapi.com` | Yes (100/month) |
| JSearch | `jsearch.p.rapidapi.com` | Yes (100/month) |
| Rapid Job Search | `job-search.p.rapidapi.com` | Yes (50/month) |

## Next Steps
1. ✅ Sign up with GitHub
2. ✅ Copy your API Key
3. ✅ Find an Internships API and note the Host
4. ✅ Update `backend/.env` with your credentials
5. ✅ Restart the backend
6. ✅ Test with the curl command above
7. ✅ Upload a resume and see AI-powered recommendations!

Questions? Check the [RapidAPI Documentation](https://docs.rapidapi.com/)
