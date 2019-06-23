# -*- coding: utf-8 -*-
import scrapy
from ..items import SakeScrapyItem


class FukuiSpider(scrapy.Spider):
    name = 'fukui'
    allowed_domains = ['www.japansake.or.jp']

    def start_requests(self):
        url = 'http://www.japansake.or.jp/sake/app.php/makers/search/?prefcode=18'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for pos in response.css('#yw1 li.page a'):
            older_post_link = pos.css('::attr(href)').extract_first()
            if older_post_link is None:
                # リンクが取得できなかった場合は最後のページなので処理を終了
                return

            older_post_link = response.urljoin(older_post_link)
            # 次のページをのリクエストを実行する
            yield scrapy.Request(older_post_link, callback=self.parse_sake_detail)

    def parse_sake_detail(self, response):
        for pos in response.css('#yw0 table tbody tr'):
            kuramoto = pos.css('td.column-name a::text').extract_first().strip()

            for sake in pos.css('td').extract()[-1].replace('<td>', '').replace('</td>', '').replace('「', '').replace(
                    '」', '').split('、'):
                if sake:
                    yield SakeScrapyItem(
                        prefecture='福井',
                        kuramoto=kuramoto,
                        sake_name=sake
                    )