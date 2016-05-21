# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib
import datetime
import dateutil.parser
import re
def parse_item(item):
    title = item.xpath("./title")[0].text
    link = item.xpath("./link")[0].text
    pub_date = item.xpath("./pubDate")[0].text
    place, quality = title.split(" was rated as ")
    place = place.strip()
    quality = quality.strip()
    m = re.match('([^\)]*)\((.*)\)', quality)
    grade_detail =  m.group(2)
    grade = m.group(1)
    date_str = dateutil.parser.parse(pub_date).strftime('%Y-%m-%d')
    scraperwiki.sqlite.save(unique_keys=["place", "date"], data={"place": place, "grade": grade, "grade_detail": grade_detail, "date": date_str})
    print place, grade, grade_detail, date_str

def parse_rss(url):
    html = scraperwiki.scrape(url)
    parser = lxml.etree.XMLParser(strip_cdata=False)
    root = lxml.etree.fromstring(html, parser)
    for item in root.xpath('//rss/channel/item'):
        parse_item(item)

parse_rss("http://beachwq.gov.hk/en/rss2.aspx")
