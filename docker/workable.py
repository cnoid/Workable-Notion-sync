import time
import requests
from notion_client import Client

# Replace with your actual tokens and subdomain
ACCESS_TOKEN = 'Workable API Token'
NOTION_TOKEN = 'Notion API Token'
WORKABLE_SUBDOMAIN = 'subdomain'
NOTION_DATABASE_ID = 'Notion Database ID'

workable_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

notion = Client(auth=NOTION_TOKEN)

def fetch_jobs_from_workable():
    response = requests.get(f"https://{WORKABLE_SUBDOMAIN}.workable.com/spi/v3/jobs?state=published", headers=workable_headers)
    response.raise_for_status()
    return response.json()['jobs']

def reformat_job_data(jobs):
    reformatted_data = []
    for job in jobs:
        if job['state'] == 'published':  # Ensure job is in the 'published' state
            reformatted_data.append({
                "Title": job['title'],
                "Location": job['location']['country'],
                "Link": job['shortlink']
            })
    return reformatted_data


def clear_existing_entries():
    query = {"database_id": NOTION_DATABASE_ID}
    response = notion.databases.query(**query)

    for page in response['results']:
        notion.pages.update(page_id=page['id'], archived=True)

def create_notion_pages(notion_data):
    for job in notion_data:
        notion.pages.create(parent={"database_id": NOTION_DATABASE_ID},
                            properties={
                                "Title": {
                                    "title": [{"text": {"content": job["Title"]}}]
                                },
                                "Location": {
                                    "rich_text": [{"text": {"content": job["Location"]}}]
                                },
                                "Link": {
                                    "url": job["Link"]
                                }
                            })

def main():
    while True:
        jobs = fetch_jobs_from_workable()
        notion_data = reformat_job_data(jobs)
        clear_existing_entries()
        create_notion_pages(notion_data)
        print("Notion database has been refreshed with new data.")
        time.sleep(86400)  # Sleep for 24 hours

if __name__ == "__main__":
    main()
