import re
import sys
import requests
import argparse
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def setup_logger():
    """
    sets up our logger, which will provide input in the terminal as the program
    runs
    """
    fmt = '%(asctime)s:%(levelname)s:%(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)


def find_urls(html_text):
    """scrapes sites for full urls or relative urls."""
    web_address = []
    soup = BeautifulSoup(html_text.text, 'html.parser')
    for w in web_address:
        for link in soup.find_all('a'):
            site = link.get('href')
            url = re.search(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                str(site))
            if url:
                web_address.append(url.group())
    return web_address


def find_phone_nums(html_text):
    """ scrapes the site for phone numbers. """

    nums = []
    text = html_text.text
    phone_nums = re.findall(
        r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?",
        text)
    for phone_num in phone_nums:
        nums.append(phone_num)
    return nums


def find_emails(html_text):
    """ scrapes site for email addresses """
    email_adrs = []
    text = html_text.text
    emails = re.findall(
        r"([a-zA-Z]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.][a-zA-Z]+)",
        text
        )
    for email in emails:
        email_adrs.append(email)
    return email_adrs


def find_imgs(html_text):
    """finds desired img links"""
    pics = []
    soup = BeautifulSoup(
        html_text.text, 'html.parser'
        )
    for img in soup.find_all('img'):
        src = img.get(
            'src'
            )
        pics.append(
            src
            )
    return pics


def create_parser():
    """ creates argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('website',
                        help='website to be scraped!!!'
                        )
    return parser


# Args parsed, website scraped and patterns matched with regex
def main(args):
    """Parse args, scrape website, scan with regex"""
    logging.info("scraping {0}.".format(__name__))
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    html_text = requests.get(parsed_args.website)

    # urls scraped!
    scraped_urls = find_urls(html_text)
    for url in scraped_urls:
        print(url)

    # Scraped Dem Digitz!
    scraped_phone_nums = find_phone_nums(html_text)
    for phone_num in scraped_phone_nums:
        print(phone_num[0] + "-" + phone_num[1] + "-" + phone_num[2])

    # emails scraped!
    scraped_emails = find_emails(html_text)
    for email in scraped_emails:
        print(email)

    # images scraped!
    scraped_imgs = find_imgs(html_text)
    for img in scraped_imgs:
        print(img)


if __name__ == '__main__':
    main(sys.argv[1:])
