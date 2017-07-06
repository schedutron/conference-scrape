"""Script to scrape worldwide conferences' info
Sources:
https://www.papercall.io - Done
https://www.oreilly.com/conferences/ - Done
https://opensource.com/resources/conferences-and-events-monthly
http://lanyrd.com/topics/open-source/
"""
from lxml import html
import requests

# Duplicates can be removed by comparing links.
# If tags are absent, they can be added by analysing description.
# Maybe later we can add conference image icons as well.
metadata = ['title', 'description', 'location', 'time', 'tags', 'link', 'source']

def from_papercall():
    """
    Function to scrape conferences' info from https://www.papercall.io
    Loads the page, gets the conference info tags, and sends each tag
    to parse_papercall() for parsing
    """
    # Following list to accumulate conferences' info in json.
    total = []
    page_no = 1
    # This loop paginates to gather all conference info blocks
    while True:
        page = requests.get('https://www.papercall.io/cfps?page=%s' % page_no)
        tree = html.fromstring(page.content)
        conf_list = tree.xpath("//div[@class='box']")
        if not conf_list:
            break
        for ele in conf_list:
            total.append(parse_papercall(ele))
        page_no += 1
    return total


def parse_papercall(ele):
    """
    Function to parse info passed by from_papercall() function.
    Returns conference info in a JSON format.
    """
    data = dict.fromkeys(metadata)
    data['source'] = 'https://www.papercall.io'
    # This gets the conference title.
    try:
        title_header = ele.xpath('.//h3/a')
        prefix = ele.xpath('.//a[@class="btn btn--tag btn--accepted-l"]/text()')
        title_with_loc = title_header[-1].xpath('./text()')[0].strip().split(' - ')
        title = title_with_loc[0]
        if prefix:
            title = prefix[0] + ': ' + title # Adds 'Pro Event: ' if present.
        data['title'] = title
    except Exception:
        pass
    # This gets the conference location.
    try:
        if len(title_with_loc) > 1:
            data['location'] = title_with_loc[-1]
    except Exception:
        pass
    # This gets the conference time.
    try:
        time_prefix = ele.xpath('.//h4[1]/text()')[0].strip()
        time_value = ele.xpath('.//h4[1]/time/text()')[0].strip()
        data['time'] = time_prefix + ' ' + time_value
    except Exception:
        pass
    #This gets the conference link.
    try:
        data['link'] = ele.xpath('.//h4[2]/a/@href')[0]
    except Exception:
        pass
    # This gets the conference tags.
    try:
        data['tags'] = ele.xpath('.//h4[last()]/span/text()')[0].strip().split(', ')
    except Exception:
        pass
    # This gets the conference description.
    try:
        des_prefix = ele.xpath('.//h4[last()-1]')[0].text_content().strip() # Has info on travel assistance etc.
        description = ele.xpath('.//div[@class="event__links"]/text()')[0].strip().lstrip('# ')
        if des_prefix:
            description = des_prefix + '; ' + description
        if description:
            data['description'] = description
    except Exception:
        pass

    return data


def from_oreilly():
    """
    Function to scrape conferences' info from https://www.oreilly.com/conferences/
    Loads the page, gets the conference info tags, and sends each tag
    to parse_oreilly() for parsing
    """
    page = requests.get('https://www.oreilly.com/conferences/')
    tree = html.fromstring(page.content)
    conf_list = tree.xpath('//li[@class="conf_event"]')
    total = []
    for ele in conf_list:
        total.append(parse_oreilly(ele))
    return total


def parse_oreilly(ele):
    """
    Function to parse info passed by from_oeilly() function.
    Returns conference info in a JSON format, like other parser functions.
    """
    data = dict.fromkeys(metadata)
    data['source'] = 'https://www.oreilly.com/conferences/'
    # This gets the conference title.
    try:
        text = ele.xpath('.//h3//text()')
        data['title'] = text[0].strip()
    except Exception:
        pass
    # This gets the conference date.
    try:
        start_date = str(text[2]).replace('\xa0', ' ')
        remaining_date_with_loc = text[3].strip()
        comma_pos = remaining_date_with_loc.find(',')
        comma_pos = remaining_date_with_loc.find(',', comma_pos+1)
        remaining_date = remaining_date_with_loc[:comma_pos].strip('\u2013')
        data['time'] = start_date + ' - ' + remaining_date
        # Following adds training dates.
        training_dates = text[4]
        training_dates = training_dates.strip()
        training_dates = training_dates.replace('\xa0', ' ').replace('\u2013', '-')
        data['time'] += ' ' + training_dates
    except Exception:
        pass
    # This gets the conference location.
    try:
        data['location'] = remaining_date_with_loc[comma_pos+1:].strip()
    except Exception:
        pass
    # This gets the conference link.
    try:
        data['link'] = ele.xpath('.//h3/a/@href')[0]
    except Exception:
        pass
    # This gets the conference description.
    try:
        data['description'] = ele.xpath('.//p')[0].text_content().strip()
    except Exception:
        pass

    return data


def from_opensource():
    """
    Function to scrape conferences' info from:
    https://opensource.com/resources/conferences-and-events-monthly
    Loads the page, gets the conference info elements, and sends each element
    to parse_opensource() for parsing
    """
    # This list accumulates all the conference info elements while pagination.
    all_ele = []
    next_page_link = "https://opensource.com/resources/conferences-and-events-monthly"
    # Following loop paginates and accumulates the conference info elements.
    while 1:
        page = requests.get(next_page_link)
        tree = html.fromstring(page.content)
        container = tree.xpath('//*[@id="mini-panel-conferences_events_content"]/div[1]/div/div/div/div[2]')
        stuff = container[0].xpath('./div')
        if not stuff:
            break
        all_ele.extend(stuff)
        next_page_link = tree.xpath('//*[@id="mini-panel-conferences_events_content"]/div[1]/div/div/div/div[3]/div/ul/li[2]/a/@href')[0]
    # This list accumulates JSON data to be returned.
    total = [parse_opensource(ele) for ele in all_ele]
    return total


def parse_opensource(ele):
    """
    Function to parse info passed by from_opensource() function.
    Returns conference info in a JSON format, like other parser functions.
    """
    data = dict.fromkeys(metadata)
    data['source'] = "https://opensource.com/resources/conferences-and-events-monthly"
    # This gets the conference title.
    try:
        data['title'] = ele.xpath('.//b/text()')[0].strip()
    except Exception:
        pass
    # This gets the conference description.
    try:
        des = '\n'.join([item.text_content() for item in ele.xpath('.//p')])
        if len(des) > 500:
            des = des[:497] + '...'
        data['description'] = des
    except Exception:
        pass
    # This gets the conference date(s)
    try:
        dates = ele.xpath('./div[4]/div/span/text()')
        data['time'] = ' to '.join(dates).strip()
    except Exception:
        pass
    # This gets the conference location
    try:
        data['location'] = ele.xpath('./div[5]/div/text()')[0].strip()
    except Exception:
        pass
    # This gets the conference link
    try:
        data['link'] = ele.xpath('./div[6]/div/a/text()')[0]
    except Exception:
        pass

    return data
