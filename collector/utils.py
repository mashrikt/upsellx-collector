import re
import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    fb = get_link_or_blank(soup, 'facebook')
    linkedin = get_link_or_blank(soup, 'linkedin')
    twitter = get_link_or_blank(soup, 'twitter')
    instagram = get_link_or_blank(soup, 'instagram')
    youtube = get_link_or_blank(soup, 'youtube')
    pinterest = get_link_or_blank(soup, 'pinterest')
    data = {
        'fb': fb,
        'linkedin': linkedin,
        'twitter': twitter,
        'instagram': instagram,
        'youtube': youtube,
        'pinterest': pinterest
    }
    return data


def get_link_or_blank(soup, channel):
    elem = soup.select_one(f"a[href*={channel}]")
    if elem and elem["href"]:
        return elem["href"]
    return ""


def scrape_fb_about(url):
    page = requests.get(url+'about/')
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('meta', property="og:title")['content']
    if title == "Log in or sign up to view":
        print("\n\nFB Blocked!!!!!!\n\n")
        return {}
    founded = get_founded_year(soup)
    email = soup.find(text=re.compile("^\S+@\S+\.\S+$")) or ""
    phone = get_phone(soup)
    about = get_about(soup)
    categories = get_categories(soup)

    meta_description = soup.find('meta', property="og:description")

    return {
        "title": title,
        "founded": founded,
        "email": email,
        "phone": phone,
        "about": about,
        "categories": categories,
        "likes": get_number_from_description(meta_description, 'likes'),
        "talking": get_number_from_description(meta_description, 'talking'),
        "awards": get_text_of_tag(soup, "Awards"),
        "mission": get_text_of_tag(soup, "Mission"),
        "products": get_text_of_tag(soup, "Products")
    }


def get_founded_year(soup):
    founded = soup.body.find(text=re.compile('^Founded in ([0-9]{4})$'))
    if founded:
        return founded.split(' ')[2]
    return get_text_of_tag(soup, "Founding date")


def get_phone(soup):
    phone_text = soup.find(text=re.compile("^Call [0-9 +-]+$"))
    if not phone_text:
        return ""
    return phone_text.replace("Call", "").strip()


def get_about(soup):
    divs = soup.findAll("div", text="About")
    if not divs:
        return ""
    return divs[-1].find_next('div').get_text()


def get_categories(soup):
    u_tag = soup.find("u", text="categories")
    if not u_tag:
        return ""
    return u_tag.find_parent('div').find_next('div').get_text()


def get_number_from_description(meta_description, category):
    if not meta_description:
        return ""
    description = meta_description['content']
    pattern = re.compile("[0-9,K]+ " + category)
    match = re.search(pattern, description)
    if not match:
        return ""
    count_str = match.group()  # format "19,000 likes"
    count = count_str.split()[0]  # get the number only "19,000"
    count.replace(",", '')  # converting again to "19000" without commas
    return count


def get_text_of_tag(soup, tag):
    elem = soup.find("div", text=tag)
    if elem:
        return elem.find_next_sibling('div').get_text()
    return ""
