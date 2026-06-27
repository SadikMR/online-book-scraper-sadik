import random
from bookscraper.items import BookItem
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # Get all category elements
        categories = response.css('.side_categories ul li ul li a')

        category_data = []

        # Extract category name and relative URL
        for category in categories:
            category_name = category.css('::text').get().strip()
            category_url = category.xpath('./@href').get()

            category_data.append({
                "name": category_name,
                "url": category_url,
            })

        # Randomly select 5 categories
        selected_categories = random.sample(category_data, 5)

        # Visit each selected category
        for category in selected_categories:
            yield response.follow(
                url=category["url"],
                callback=self.parse_category,
                meta={
                    "books": [],
                    "category": category["name"],
                },
            )


    def parse_category(self, response):

        books = response.meta["books"]

        # Collect books from current page
        current_books = response.css('article h3 a')

        # Appending new books
        for book in current_books:
            books.append({
                "url": response.urljoin(book.xpath("./@href").get()),
            })

        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()

        #pagination
        if next_page_url:
            yield response.follow(
                next_page_url,
                callback=self.parse_category,
                meta={
                    "category": response.meta["category"],
                    "books": books,
                },
            )
        else:
            #selecting random 5 books
            selected_books = random.sample(
                books,
                min(5, len(books))
            )

            #visit each book
            for book in selected_books:
                yield response.follow(
                    book["url"],
                    callback=self.parse_book,
                    meta={
                        "category": response.meta["category"]
                    },
                )

        
    def parse_book(self, response):

        category = response.meta["category"]
        image_url = response.urljoin( response.xpath('//div[@class="item active"]/img/@src').get())

        product = response.css('.product_main')
        title = product.css('h1::text').get().strip()
        price = product.css('.price_color::text').get()
        availability = "".join(product.xpath('./p[contains(@class,"availability")]//text()').getall()).strip()

        item = BookItem()

        item["title"] = title
        item["price"] = price
        item["availability"] = availability
        item["product_url"] = response.url
        item["image_url"] = image_url
        item["category"] = category

        yield item