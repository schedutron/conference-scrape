from lxml import html
import scrapy

metadata = [
    'title', 'description', 'location',
    'time', 'tags', 'link', 'source'
]


class PapercallSpider(scrapy.Spider):
    name = "papercall"
    start_urls = [
        "https://www.papercall.io/cfps",
    ]

    def parse(self, response):
        """This is the default parsing function called for urls."""

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
