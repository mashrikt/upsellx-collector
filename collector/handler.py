import json
import uuid

from .models import CollectorModel
from .utils import scrape_website, scrape_fb_about, format_url


def create(event, context):
    data = json.loads(event['body'])
    if not data or "url" not in data:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_message": "Please enter a valid URL"})
        }
    url = data['url']
    url = format_url(url)

    try:
        a_collection = CollectorModel.get(url)
    except CollectorModel.DoesNotExist:
        website = scrape_website(url)
        fb = website.get("fb", {})
        if fb:
            fb = scrape_fb_about(fb)

        a_collection = CollectorModel(
            id=str(uuid.uuid1()),
            url=url,
            website=website,
            fb=fb
        )
        a_collection.save()

    response = {
        "statusCode": 201,
        "body": json.dumps(a_collection.__dict__["attribute_values"], default=str)
    }
    return response
