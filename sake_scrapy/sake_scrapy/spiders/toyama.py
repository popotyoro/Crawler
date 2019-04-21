# -*- coding: utf-8 -*-
import scrapy
from ..items import SakeScrapyItem

class ToyamaSpider(scrapy.Spider):
    name = 'toyama'
    allowed_domains = ['toyama.wekey.be']

    def start_requests(self):
        url = 'http://toyama.wekey.be/Static/jizake/index'
        yield scrapy.Request(url, callback=self.parse_kuramoto)

    def parse_kuramoto(self, response):

        for pos in response.css('div.zizake-list ul li a'):

            older_post_link = pos.css('::attr(href)').extract_first()
            if older_post_link is None:
                # リンクが取得できなかった場合は最後のページなので処理を終了
                return

            older_post_link = response.urljoin(older_post_link)
            # 次のページをのリクエストを実行する
            yield scrapy.Request(older_post_link, callback=self.parse_sake_detail)

    def parse_sake_detail(self, response):

        kuramoto = response.css('div#index_zizake h2::text').extract_first()

        for pos in response.css('div#index_zizake div.zizake-box p::text'):
            yield SakeScrapyItem(
                prefecture='富山',
                kuramoto=kuramoto,
                sake_name=pos.extract()
            )