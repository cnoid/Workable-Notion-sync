# Workable2Notion
Sends Workable jobs to a Notion database, giving overview for HR and Corp of current open jobs.


Usage:

Replace:

- ACCESS_TOKEN with your Workable API token
- NOTION_TOKEN with your Notion API token
- WORKABLE_SUBDOMAIN with your subdomain. That means only the part that's in your subdomain, if your workable subdomain is "https://example.workable.com" you should put in 'example'
- NOTION_DATABASE_ID with the ID of the database. First create a database in your pages (create table->convert to database), then copy link to database - it'll be the first string after notion.so/ until before "?v=" This will be an inline database.

Prerequisites:
- Python: requests, notion_client
- Notion: Set up "Title" (text), "Location" (text), "Link" (url)

More can be added, for example:
`"Remote": "Yes" if job['location']['workplace_type'] == "remote" else "No",`
```py
                                "Remote": {
                                    "checkbox": job["Remote"] == "Yes"
                                },
```
As you can see, you'll add a "checkbox" with value "Remote" in Notion for this one.


Docker version has a 24h sleep, but you should probably just run it as a cron job
