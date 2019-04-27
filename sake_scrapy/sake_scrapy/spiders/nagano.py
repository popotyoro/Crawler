# -*- coding: utf-8 -*-
import scrapy
from ..items import SakeScrapyItem


class NaganoSpider(scrapy.Spider):
    name = 'nagano'
    allowed_domains = ['www.nagano-sake.or.jp']

    def start_requests(self):
        url = 'https://www.nagano-sake.or.jp/kura/'
        yield scrapy.Request(url, callback=self.parse_kuramoto)

    def parse_kuramoto(self, response):
        for pos in response.css('#menu li a'):
            older_post_link = pos.css('::attr(href)').extract_first()
            if older_post_link is None:
                # リンクが取得できなかった場合は最後のページなので処理を終了
                return

            older_post_link = response.urljoin(older_post_link)
            # 次のページをのリクエストを実行する
            yield scrapy.Request(older_post_link, callback=self.parse_kuramoto_details)

    def parse_kuramoto_details(self, response):

        for pos in response.css('#contents_wide div.clearfix.p_b10.heightLineParent'):
            kuramoto_left = pos.css('div.kuramoto_left')
            name = kuramoto_left.css('div.title div.fright span.kuraname::text').extract_first()
            if name is None:
                #LINKになっている場合がある
                name = kuramoto_left.css('div.title div.fright span.kuraname a::text').extract_first()
            sake = kuramoto_left.css('table.kura_all tr')[0].css('td::text').extract_first().strip()
            yield SakeScrapyItem(
                prefecture='長野',
                kuramoto=name,
                sake_name=sake
            )

            kuramoto_right = pos.css('div.kuramoto_right')
            if kuramoto_right.extract_first() is None:
                continue
            name = kuramoto_right.css('div.title div.fright span.kuraname::text').extract_first()
            if name is None:
                #LINKになっている場合がある
                name = kuramoto_right.css('div.title div.fright span.kuraname a::text').extract_first()
            sake = kuramoto_right.css('table.kura_all tr')[0].css('td::text').extract_first().strip()
            yield SakeScrapyItem(
                prefecture='長野',
                kuramoto=name,
                sake_name=sake
            )
