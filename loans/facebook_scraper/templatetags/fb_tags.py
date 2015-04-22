
from django import template

# facebook_scraper
from facebook_scraper.utils import get_profile_picture

register = template.Library()

@register.filter
def get_relationship(uid):
    j = get_profile_picture(uid)
    return j.get('url')