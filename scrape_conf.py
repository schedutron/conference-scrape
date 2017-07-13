"""Script to scrape worldwide conferences' info
Sources:
https://www.papercall.io - Done
https://www.oreilly.com/conferences/ - Done
https://opensource.com/resources/conferences-and-events-monthly - Done
http://www.pycon.org (PyCon Calender) - Done
http://lanyrd.com/topics/open-source/
http://events.linuxfoundation.org
https://twitter.com/PythonEvents
"""
from lxml import html
# import requests, datetime, ... can be used but it's against PEP8.
import datetime
import json
import re
import requests

# Duplicates can be removed by comparing links.
# Timezone problems must be addressed, if any.
# If tags are absent, they can be added by analysing description.
# Maybe later we can add conference image icons as well.
metadata = [
    'title', 'description', 'location',
    'time', 'tags', 'link', 'source'
]


def check(attrib):
    """
    Function to check parsing functions for correctness.
    Helpful in debugging. Used in complete_check().
    """
    count = 0
    for data in total:  # total must be defined.
        if data[attrib] is None:
            print(json.dumps(data, indent=4))
            count += 1
    print("Total: %s" % count)


def complete_check():
    """
    Function to check parsing functions's correctness
    for each attribute in metadata.
    """
    for attrib in metadata:
        print(attrib)
        check(attrib)
        print('-*-'*33)


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
        prefix = ele.xpath(
            './/a[@class="btn btn--tag btn--accepted-l"]/text()'
            )
        title_with_loc = title_header[-1].xpath('./text()')[0].strip()
        title_with_loc = title_with_loc.split(' - ')
        title = title_with_loc[0]
        if prefix:
            title = prefix[0] + ': ' + title  # Adds 'Pro Event: ' if present.
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
    # This gets the conference link.
    try:
        data['link'] = ele.xpath('.//h4[2]/a/@href')[0]
    except Exception:
        pass
    # This gets the conference tags.
    try:
        data['tags'] = ele.xpath('.//h4[last()]/span/text()')[0].strip()
        data['tags'] = data['tags'].split(', ')
    except Exception:
        pass
    # This gets the conference description.
    try:
        # Following line gets possible info on travel assistance etc.
        des_prefix = ele.xpath('.//h4[last()-1]')[0].text_content().strip()
        description = ele.xpath('.//div[@class="event__links"]/text()')[0]
        description = description.strip().lstrip('# ')
        if des_prefix:
            description = des_prefix + '; ' + description
        if description:
            data['description'] = description
    except Exception:
        pass

    return data


def from_oreilly():
    """
    Function to scrape conferences' info from
    https://www.oreilly.com/conferences/
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
        start_date = text[2]
        remaining_date_with_loc = text[3].strip()
        comma_pos = remaining_date_with_loc.find(',')
        comma_pos = remaining_date_with_loc.find(',', comma_pos+1)
        remaining_date = remaining_date_with_loc[:comma_pos].strip('\u2013')
        data['time'] = start_date + remaining_date
        # Following adds training dates.
        training_dates = text[4].strip()
        data['time'] += ' ' + training_dates
    except Exception as e:
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
    next_page_link = \
        "https://opensource.com/resources/conferences-and-events-monthly"
    # Following loop paginates and accumulates the conference info elements.
    while 1:
        page = requests.get(next_page_link)
        tree = html.fromstring(page.content)
        container = tree.xpath(
            '//*[@id="mini-panel-conferences_events_content"]/'
            + 'div[1]/div/div/div/div[2]'
            )
        stuff = container[0].xpath('./div')
        if not stuff:
            break
        all_ele.extend(stuff)
        next_page_link = tree.xpath(
            '//*[@id="mini-panel-conferences_events_content"]/'
            + 'div[1]/div/div/div/div[3]/div/ul/li[2]/a/@href'
            )[0]
    # This list accumulates JSON data to be returned.
    total = [parse_opensource(ele) for ele in all_ele]
    return total


def parse_opensource(ele):
    """
    Function to parse info passed by from_opensource() function.
    Returns conference info in a JSON format, like other parser functions.
    """
    data = dict.fromkeys(metadata)
    data['source'] = \
        "https://opensource.com/resources/conferences-and-events-monthly"
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


def from_pycon_calender():
    """
    Function to get Python events calender from http://www.pycon.org
    Sends calender contents to parse_pycon_calender() function for parsing.
    """
    calender = requests.get(
        'https://www.google.com/calendar/ical/j7gov1cmnqr9tvg14k621j7t5c%40'
        + 'group.calendar.google.com/public/basic.ics'
    )
    calender_text = calender.text
    # This splits the calender_text string into individual event infos
    events = calender_text.split('BEGIN:VEVENT')[1:]
    today = datetime.datetime.today().strftime('%Y%m%d')
    # This loop used for stripping out previous events
    for i in range(len(events)):
        item = events[i]
        dtend = re.search(r'DTEND(;VALUE=DATE)?:?(\S+)\r\n', item).groups()[-1]
        if dtend < today:
            break
    events = events[:i]
    total = [parse_pycon_calender(event) for event in events]
    return total


def parse_pycon_calender(ele):
    """
    Function to parse info passed by from_pycon_calender() function.
    Returns conferences' info in a JSON format, like other parser functions.
    """
    data = dict.fromkeys(metadata)
    data['source'] = 'http://www.pycon.org'
    # This gets the conference time.
    try:
        dtstart = re.search(r'DTSTART(;VALUE=DATE)?:?(\S+)\r\n', ele)
        dtstart = dtstart.groups()[-1].rstrip()
        dtend = re.search(r'DTEND(;VALUE=DATE)?:?(\S+)\r\n', ele)
        dtend = dtend.groups()[-1].rstrip()
        data['time'] = dtstart + ' - ' + dtend
    except Exception:
        pass
    # This gets the conference link.
    try:
        data['link'] = re.search(r'DESCRIPTION:<a href="(\S+?)>', ele)
        data['link'] = data['link'].groups()[0][:-1]
    except Exception:
        pass
    # This gets the conference location.
    try:
        data['location'] = re.search(r'LOCATION:([\s\S]+)SEQUENCE', ele)
        data['location'] = data['location'].groups()[0].rstrip()
        data['location'] = data['location'].replace('\r\n ', '')
        data['location'] = data['location'].replace('\\', '')
    except Exception:
        pass
    # This gets the conference title.
    try:
        data['title'] = re.search(r'SUMMARY:([\s\S]+)TRANSP:', ele).groups()[0]
        data['title'] = data['title'].rstrip().replace('\r\n ', '')
        data['title'] = data['title'].replace('\\', '')
    except Exception:
        pass

    return data


def from_lanyrd():
    """
    Function to scrape conferences' info from:
    http://lanyrd.com/topics/open-source
    Loads the page, gets the conference info elements, and sends each element
    to parse_lanyrd() for parsing
    """
    page = requests.get('http://lanyrd.com/topics/open-source')
    tree = html.fromstring(page.content)
    conf_list = tree.xpath('//li[@class="conference vevent"]')
    total = [parse_lanyrd(ele) for ele in conf_list]
    return total


def parse_lanyrd(ele):
    """
    Function to parse info passed by from_lanyrd() function.
    Returns conferences' info in a JSON format, like other parser functions.
    """
    data = dict.fromkeys(metadata)
    data['source'] = 'http://lanyrd.com/topics/open-source'
    # This gets the conference title.
    try:
        title_ele = ele.xpath('.//h4/a')[0]
        data['title'] = title_ele.text_content().strip()
    except Exception:
        pass
    # This gets the conference link.
    try:
        data['link'] = data['source'] + title_ele.attrib['href']
    except Exception:
        pass
    # This gets the conference location.
    try:
        reversed_location_chunks = ele.xpath(
            './/p[@class="location"]/a/text()'
            )
        data['location'] = ', '.join(
            [chunk.strip() for chunk in reversed_location_chunks[1:][::-1]]
            )
    except Exception:
        pass
    # This gets the conference time.
    try:
        data['time'] = ele.xpath('.//p[@class="date"]')[0].text_content()
    except Exception:
        pass
    # This gets the conference tags.
    try:
        data['tags'] = ele.xpath(
            './/ul[@class="tags inline-tags meta"]/li/a/text()'
            )
    except Exception:
        pass

    return data


def from_linuxfoundation():
    """
    Function to scrape conferences' info from:
    http://events.linuxfoundation.org
    Loads the page, gets the conference info elements, and sends each element
    to parse_linuxfoundation() for parsing
    """
    page = requests.get('http://events.linuxfoundation.org')
    tree = html.fromstring(page.content)
    conf_list = tree.xpath('//div[@class="view-content"]')[2].xpath('./*')
    for i in range(len(conf_list)):
        if conf_list[i].xpath('name()') == 'h3':
            break
    conf_list = conf_list[:i]
    total = [parse_linuxfoundation(ele) for ele in conf_list]
    return total


def parse_linuxfoundation(ele):
    """
    Function to parse info passed by from_linuxfoundation() function.
    Returns conferences' info in a JSON format, like other parser functions.
    """
    data = dict.fromkeys(metadata)
    data['source'] = 'http://events.linuxfoundation.org'
    # This gets the conference title.
    try:
        title = ele.xpath('.//a')[1]
        data['title'] = title.text_content().strip()
    except Exception:
        pass
    # This gets the conference link.
    try:
        data['link'] = title.attrib['href']
    except Exception:
        pass
    # This gets the conference time.
    try:
        date_with_loc = ele.xpath(
            './/div[@class="views-field views-field-field-events-date"]'
            )[0]
        date_with_loc = date_with_loc.text_content().strip().split('|')
        data['time'] = date_with_loc[0].strip()
    except Exception:
        pass
    # This gets the conference location.
    try:
        data['location'] = date_with_loc[1].strip()
    except Exception:
        pass
    # This gets the conference description.
    try:
        data['description'] = ele.xpath(
            './/div[@class="field field-type-text-with-summary"]/text()'
            )[0].strip()
    except Exception:
        pass

    return data
