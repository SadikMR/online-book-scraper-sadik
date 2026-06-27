# Online Book Scraper

## Project Overview

Online Book Scraper is a web scraping application built with **Scrapy** to collect book information from the **Books to Scrape** website.

The scraper extracts book details from multiple categories, cleans and validates the data, stores it in a SQLite database, exports it into multiple formats (JSON, CSV, and XML), and supports deployment through **Scrapyd**. The project is fully Dockerized, allowing the scraping service to run consistently across different environments.

---

# Features

* Scrape books from multiple categories
* Extract book details:

  * Title
  * Price
  * Availability
  * Product URL
  * Image URL
  * Category
* Data cleaning and normalization
* Store scraped data in SQLite
* Export data as:

  * JSON
  * CSV
  * XML
* Deploy spiders using Scrapyd
* Dockerized Scrapyd server
* Schedule spiders through HTTP API
* Monitor jobs using Scrapyd Web UI

---

# Tech Stack

| Technology     | Purpose                 |
| -------------- | ----------------------- |
| Python 3.12    | Programming Language    |
| Scrapy         | Web Scraping Framework  |
| SQLite         | Database                |
| Scrapyd        | Spider Deployment       |
| Scrapyd Client | Deployment Tool         |
| Docker         | Containerization        |
| Docker Compose | Container Orchestration |

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/SadikMR/online-book-scraper-sadik.git
cd online-book-scraper-sadik
```

---

# Environment Setup

## Create Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Spider

Run the spider directly with Scrapy:

```bash
scrapy crawl books
```

The spider will:

* Scrape book information
* Store data in SQLite
* Export JSON
* Export CSV
* Export XML

Generated output:

```text
extracted_data/
├── books.json
├── books.csv
└── books.xml

books.db
```

---

# Docker Setup Guide

## Build Docker Image

```bash
docker compose up -d --build
```

Verify container:

```bash
docker ps
```

Stop container:

```bash
docker compose down
```

---

# Scrapyd Deployment Guide

## Local Deployment

Start Scrapyd

```bash
scrapyd
```

Open browser:

```
http://localhost:6800
```

Deploy project

```bash
scrapyd-deploy
```

Verify deployment

```bash
curl http://localhost:6800/listprojects.json
```

List spiders

```bash
curl "http://localhost:6800/listspiders.json?project=bookscraper"
```

Schedule spider

```bash
curl http://localhost:6800/schedule.json \
-d project=bookscraper \
-d spider=books
```

Monitor jobs

```bash
curl "http://localhost:6800/listjobs.json?project=bookscraper"
```

---

## Docker Deployment

Start Scrapyd

```bash
docker compose up -d --build
```

Deploy

```bash
scrapyd-deploy
```

Schedule spider

```bash
curl http://localhost:6800/schedule.json \
-d project=bookscraper \
-d spider=books
```

Check running jobs

```bash
curl "http://localhost:6800/listjobs.json?project=bookscraper"
```

---

# Output Format Description

## Local Scrapy Execution

The scraper exports:

* JSON
* CSV
* XML

Location:

```text
extracted_data/
```

SQLite database:

```text
books.db
```

## Scrapyd Execution

Scrapyd stores scraped items as JSON Lines (`.jl`) files in the configured `items_dir`.

Example:

```text
items/
└── bookscraper/
    └── books/
        └── <job_id>.jl
```

---

# Database Configuration

The project uses SQLite.

Database file:

```text
books.db
```

Schema:

| Column       | Type    |
| ------------ | ------- |
| id           | INTEGER |
| title        | TEXT    |
| price        | REAL    |
| availability | BOOLEAN |
| product_url  | TEXT    |
| image_url    | TEXT    |
| category     | TEXT    |

The SQLite pipeline:

* Creates the table automatically if it does not exist.
* Cleans and normalizes scraped data.
* Inserts each item into the database.

---

# Architecture Diagram

```text
                    +----------------------+
                    | Books to Scrape Site |
                    +----------+-----------+
                               |
                               v
                     +------------------+
                     | Scrapy Spider    |
                     +--------+---------+
                              |
                              v
                     +------------------+
                     | Item Pipeline    |
                     | - Clean Data     |
                     | - Normalize Data |
                     +--------+---------+
                              |
              +---------------+---------------+
              |                               |
              v                               v
      +---------------+              +----------------+
      | SQLite DB     |              | Feed Exports   |
      | books.db      |              | JSON / CSV/XML |
      +---------------+              +----------------+
                              |
                              v
                    +-------------------+
                    | Scrapyd Server    |
                    +-------------------+
                              |
                              v
                     HTTP API / Web UI
```

---
# Folder Structure

```text
online-book-scraper-sadik/
│
├── bookscraper/
│   ├── spiders/
│   │   └── books.py
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   └── settings.py
│
├── extracted_data/
├── docker-compose.yml
├── dockerfile
├── requirements.txt
├── scrapy.cfg
├── scrapyd.conf
├── setup.py
├── .dockerignore
├── .gitignore
└── README.md
```


---

# Design Decisions

* **Scrapy** was selected because it provides efficient crawling, request scheduling, and data extraction.
* **SQLite** was chosen because it is lightweight, serverless, and suitable for storing structured scraped data.
* **Pipelines** are responsible for data cleaning, validation, normalization, and database insertion, keeping the spider focused only on scraping.
* **Feed Exports** are configured in Scrapy to generate JSON, CSV, and XML outputs automatically during local execution.
* **Scrapyd** enables deployment and remote execution of spiders through a REST API.
* **Docker** ensures a consistent runtime environment across different machines without requiring local dependency installation.

---

# Known Limitations

* The scraper targets the static **Books to Scrape** website only.
* Scrapyd stores scheduled job outputs as JSON Lines (`.jl`) files by default rather than using the configured Scrapy feed exports.
* SQLite is intended for development and small datasets. A production deployment would typically use a database such as PostgreSQL or MySQL.
* Network interruptions or website changes may affect scraping results.
* The current spider focuses on the configured categories and does not implement automatic retry or resume functionality for interrupted jobs.

---

# License

This project was developed as part of an internship assignment to demonstrate web scraping, data storage, containerization, and Scrapyd deployment using Python and Scrapy.
