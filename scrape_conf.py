"""Script to scrape worldwide conferences' info"""

from lxml import html
import requests

# Maybe later we can add conference image icons as well.
metadata = ['title', 'description', 'location', 'time', 'tags', 'link', 'source']

def from_papercall():
    """
    Function to scrape conferences' info from www.papercall.io
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
    except:
        pass
    # This gets the conference location.
    try:
        if len(title_with_loc) > 1:
            data['location'] = title_with_loc[-1]
    except:
        pass
    # This gets the conference time.
    try:
        time_prefix = ele.xpath('.//h4[1]/text()')[0].strip()
        time_value = ele.xpath('.//h4[1]/time/text()')[0].strip()
        data['time'] = time_prefix + ' ' + time_value
    except:
        pass
    #This gets the conference link.
    try:
        data['link'] = ele.xpath('.//h4[2]/a/@href')[0]
    except:
        pass
    # This gets the conference tags.
    try:
        data['tags'] = ele.xpath('.//h4[last()]/span/text()')[0].strip().split(', ')
    except:
        pass
    # This gets the conference description.
    try:
        des_prefix = ele.xpath('.//h4[last()-1]/text()')[0].strip() # Has info on travel assistance etc.
        description = ele.xpath('.//div[@class="event__links"]/text()')[0].strip().lstrip('# ')
        if des_prefix:
            description = des_prefix + '; ' + description
        if description:
            data['description'] = description
    except:
        pass

    return data
