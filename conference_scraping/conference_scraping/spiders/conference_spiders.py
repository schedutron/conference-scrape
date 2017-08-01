from constants import *  # Gets metadata info.
from lxml import html
import scrapy


class PapercallSpider(scrapy.Spider):
    name = "papercall"
    start_urls = [
        "https://www.papercall.io/cfps",
    ]

    def parse(self, response):
        """This is the default parsing function called for start urls."""

        def parse_papercall(ele):
            """
            Helper function to parse info passed by self.parse() method.
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
                    # Following line adds 'Pro Event: ' if present.
                    title = prefix[0] + ': ' + title
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
                data['tags'] = ele.xpath('.//h4[last()]/span/text()')[0]
                data['tags'] = data['tags'].strip().split(', ')
            except Exception:
                pass
            # This gets the conference description.
            try:
                # Following line gets possible info on travel assistance etc.
                des_prefix = ele.xpath('.//h4[last()-1]')[0].text_content()
                des_prefix = des_prefix.strip()
                description = ele.xpath('.//div[@class="event__links"]/text()')
                description = description[0].strip().lstrip('# ')
                if des_prefix:
                    description = des_prefix + '; ' + description
                if description:
                    data['description'] = description
            except Exception:
                pass

            return data

        # Following gets the conference info blocks.
        conf_list = response.xpath("//div[@class='box']")
        for ele in conf_list:
            yield parse_papercall(html.fromstring(ele.extract()))
        # Following performs pagination.
        next_page = response.xpath("//li[@class='next']/a/@href")
        if next_page is not None:
            yield response.follow(
                next_page.extract_first(),
                callback=self.parse
            )


class OreillySpider(scrapy.Spider):
    name = "oreilly"
    start_urls = [
        'https://www.oreilly.com/conferences/',
    ]

    def parse(self, response):
        """This is the default parsing function called for start urls."""

        def parse_oreilly(ele):
            """
            Helper function to parse info passed by sel.parse() method.
            Returns conference info in a JSON format, like other helper parser
            functions.
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
                remaining_date = remaining_date_with_loc[:comma_pos]
                data['time'] = start_date + remaining_date.strip('\u2013')
                # Following adds training dates.
                training_dates = text[4].strip()
                data['time'] += ' ' + training_dates
            except Exception as e:
                pass
            # This gets the conference location.
            try:
                data['location'] = remaining_date_with_loc[comma_pos+1:]
                data['location'] = data['location'].strip()
            except Exception:
                pass
            # This gets the conference link.
            try:
                data['link'] = ele.xpath('.//h3/a/@href')[0]
            except Exception:
                pass
            # This gets the conference description.
            try:
                data['description'] = ele.xpath('.//p')[0].text_content()
                data['description'] = data['description'].strip()
            except Exception:
                pass

            return data

        conf_list = response.xpath("//li[@class='conf_event']")
        for ele in conf_list:
            yield parse_oreilly(html.fromstring(ele.extract()))


class OpensourceSpider(scrapy.Spider):
    name = "opensource"
    start_urls = [
        "https://opensource.com/resources/conferences-and-events-monthly",
    ]

    def parse(self, response):
        "As usual, the default parsing function for response text."

        def parse_opensource(ele):
            """
            Helper function to parse info passed by sefl.parse() method.
            Returns conference info in a JSON format, like other parser
            functions.
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
                des = '\n'.join(
                    [item.text_content() for item in ele.xpath('.//p')]
                    )
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

        container = response.xpath(
            '//*[@id="mini-panel-conferences_events_content"]/'
            + 'div[1]/div/div/div/div[2]'
            )
        conf_list = container[0].xpath('./div')
        for ele in conf_list:
            yield parse_opensource(html.fromstring(ele.extract()))

        # Pagination stuff below.
        next_page_link = response.xpath(
            '//*[@id="mini-panel-conferences_events_content"]/'
            + 'div[1]/div/div/div/div[3]/div/ul/li[2]/a/@href'
            ).extract_first()

        if (next_page_link is not None) and conf_list:
            yield response.follow(next_page_link, callback=self.parse)
