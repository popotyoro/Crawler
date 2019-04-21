# -*- coding: utf-8 -*-
import scrapy


class SakeSpiderSpider(scrapy.Spider):
    name = 'sake_spider'
    allowed_domains = ['niigata-sake.or.jp']
    start_urls = ['http://niigata-sake.or.jp/kuramoto/index.html']

    def parse(self, response):

        for pos in response.css('.a_type.clearfix dd a'):
            # 酒造クローリング
            print('HIT!!!!!!!')
            print(pos.css('::text').extract_first())

            # 再帰的にページングを辿るための処理
            older_post_link = pos.css('::attr(href)').extract_first()
            if older_post_link is None:
                # リンクが取得できなかった場合は最後のページなので処理を終了
                return

            print('URLは:' + older_post_link)
            # URLが相対パスだった場合に絶対パスに変換する
            older_post_link = response.urljoin(older_post_link)
            # 次のページをのリクエストを実行する
            yield scrapy.Request(older_post_link, callback=self.parse)

        for pos in response.css('.seihin_box.clearfix .setumei p strong::text'):
            print("酒HIT！！！")
            print(pos.extract())
