# -*- coding: utf-8 -*-
import scrapy
from ..items import SakeScrapyItem

class SakeSpiderSpider(scrapy.Spider):
    name = 'niigata'
    allowed_domains = ['niigata-sake.or.jp']

    def start_requests(self):
        url = 'http://niigata-sake.or.jp/kuramoto'
        yield scrapy.Request(url, callback=self.parse_niigata_area)

    def parse(self, response):

        for pos in response.css('dl.a_type.clearfix dd a'):

            # 再帰的にページングを辿るための処理
            older_post_link = pos.css('::attr(href)').extract_first()
            if older_post_link is None:
                # リンクが取得できなかった場合は最後のページなので処理を終了
                return

            # URLが相対パスだった場合に絶対パスに変換する
            older_post_link = response.urljoin(older_post_link)
            # 次のページをのリクエストを実行する
            yield scrapy.Request(older_post_link, callback=self.parse_niigata_kuramoto)

    def parse_niigata_kuramoto(self, response):

        kuramoto = response.css('div.bgg #name::text').extract_first()

        for pos in response.css('.seihin_box.clearfix .setumei p strong::text'):
            yield SakeScrapyItem(
                prefecture='新潟',
                kuramoto=kuramoto,
                sake_name=pos.extract()
            )

    def parse_niigata_area(self, response):
        for pos in response.css('#sideBar ul li a'):
            older_post_link = pos.css('::attr(href)').extract_first()
            if older_post_link is None:
                # リンクが取得できなかった場合は最後のページなので処理を終了
                return

            # URLが相対パスだった場合に絶対パスに変換する
            older_post_link = response.urljoin(older_post_link)
            # 次のページをのリクエストを実行する
            yield scrapy.Request(older_post_link, callback=self.parse)

