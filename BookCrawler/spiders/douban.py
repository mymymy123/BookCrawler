import scrapy
from scrapy import Request
import re
from BookCrawler.items import BookItem,CommentItem
from zoneinfo import ZoneInfo
import dateparser
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']
    tz=ZoneInfo('Asia/Shanghai')
    

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url,callback=self.parse_list)


    def parse_list(self, response):
        tags=response.xpath('//table[@class="tagCol"]//td/a/@href').getall()
        # print(tags)
        for tag in tags:
            index_url=response.urljoin(tag)
            yield  Request(url=index_url,callback=self.parse_index)

    def parse_index(self,response):
        detail_urls=response.css('.subject-list .pic a.nbg::attr(href)').getall()
        # print(detail_urls)
        for detail_url in detail_urls:
            yield Request(url=detail_url,callback=self.parse_detail)
        
        next_page=response.css('.paginator span.next a::attr(href)').get()
        # print(next_page)
        next_url=response.urljoin(next_page)
        yield Request(url=next_url,callback=self.parse_index)

    def parse_detail(self,response):
        
        book_id=re.search('/subject/(\d+)/',response.url).group(1)
        book_name=response.xpath('//h1[@class="title"]/span/text()').get().strip()
        book_publisher=response.xpath('//span[contains(text(),"出版社:") and @class="pl"]/following-sibling::text()').get()

        book_publisher=book_publisher.strip() if book_publisher else None
        book_page_number=response.xpath('//span[contains(text(),"页数:") and @class="pl"]/following-sibling::text()').get()
        book_page_number=book_page_number.strip() if book_page_number else None
        book_isbn=response.xpath('//span[contains(text(),"ISBN") and @class="pl"]/following-sibling::text()').get()
        book_isbn= book_isbn.strip() if book_isbn else None

        book_published_at=response.xpath('//span[contains(text(),"出版年:") and @class="pl"]/following-sibling::text()').get()
        book_published_at=dateparser.parse(book_published_at).replace(tzinfo=self.tz) if book_published_at else None


        book_price=response.xpath('//span[contains(text(),"定价:") and @class="pl"]/following-sibling::text()').get()
        book_price=book_price.strip() if book_price else None

        book_url=response.url
        book_authors=response.xpath('//span[contains(text(),"作者") and @class="pl"]/following-sibling::a/text()').get()
        book_translators=response.xpath('//span[contains(text(),"译者") and @class="pl"]/following-sibling::a/text()').get()
        book_translators=book_translators.strip() if book_translators else None

        book_score=response.xpath('//div[contains(@class,"rating_self")]/strong[contains(@class,"rating_num")]/text()').get()
        book_score=book_score.strip() if book_score else None
        book_catalog=''.join(response.xpath(f'//div[contains(@id,"dir_{book_id}_full")]//text()').getall())

        book_cover=response.css('#mainpic a.nbg::attr(href)').get().strip()
        book_introduction=response.xpath('//h2[contains(.,"内容简介")]/following-sibling::div[@id="link-report"]//div[@class="intro"]//p/text()').getall()
        book_introduction=''.join(book_introduction)

        book_item=BookItem({
            'id': book_id,
            'name': book_name,
            'publisher': book_publisher,
            'page_number': book_page_number,
            'isbn': book_isbn,
            'published_at': book_published_at,
            'price': book_price,
            'url': book_url,
            'authors': book_authors,
            'translators': book_translators,
            'score': book_score,
            'catalog': book_catalog,
            'cover': book_cover,
            'introduction': book_introduction,
        })
        yield book_item


        comment_items = response.css('li.comment-item')
        for item in comment_items:
            comment_id=item.xpath('./@data-cid').get()  
            comment_content=item.xpath('.//span[@class="short"]/text()').get()
            comment_item=CommentItem({
                'id':comment_id,
                'content':comment_content,
                'book_id':book_id
            })
            yield comment_item

        





