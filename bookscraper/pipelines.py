import sqlite3


class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("books.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                availability BOOLEAN,
                product_url TEXT,
                image_url TEXT,
                category TEXT
            )
            """)

        self.connection.commit()

    def process_item(self, item, spider):
        # Remove whitespace
        item["title"] = item["title"].strip()
        item["category"] = item["category"].strip()

        # Normalize price
        price = item["price"].replace("£", "").strip()
        item["price"] = float(price)

        # Normalize availability
        availability = item["availability"].strip().lower()
        item["availability"] = availability.startswith("in stock")

        # Insert into SQLite
        self.cursor.execute("""
            INSERT INTO books
            (title, price, availability, product_url, image_url, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["title"],
            item["price"],
            item["availability"],
            item["product_url"],
            item["image_url"],
            item["category"],
        ))

        self.connection.commit()

        return item

    def close_spider(self, spider):
        self.connection.close()