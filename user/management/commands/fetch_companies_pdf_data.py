from django.core.management.base import BaseCommand
from user.models.company import Company
from user.models.document import Document
import requests
from bs4 import BeautifulSoup
import environ
from urllib.parse import urlparse
import io
import json
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('companies_list', nargs=1, type=str)

    def handle(self, *args, **options):
        companies_list = options['companies_list'][0].split()
        for company_name in companies_list:
            query = f"{company_name} investor relations"
            print(query)
            url = self.bing_search(query)
            print(f"Site Url >> {url}")
            pdf_links = self.extract_pdf_links(url)
            company, created = Company.objects.get_or_create(name=company_name)
            for pdf_link in pdf_links:
                print(f'PDF Link >>: {pdf_link}')
                if not Document.objects.filter(url=pdf_link).exists():
                    [publish_date, title, transcript] = self.extract_pdf_text(
                        pdf_link)
                    if publish_date is not None and transcript is not None:
                        new_doc = Document.objects.create(title=title, transcript=transcript,
                                                          url=pdf_link, published_at=publish_date, company=company)
                        print(f"Created Document with id: {new_doc.id}")
                    else:
                        print('Issue with the PDF')

    def bing_search(self, query):
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {
            "Ocp-Apim-Subscription-Key": env('BING_SEARCH_API_KEY')}
        params = {
            "q": query,
            "textDecorations": True,
            "textFormat": "HTML",
            "count": 1
        }
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        response_url = response.json()['webPages']['value'][0]['url']
        return response_url

    def extract_pdf_links(self, url):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdf_links = []
        for link in soup.findAll('a'):
            href = link.get('href')
            if href and href.endswith('.pdf'):
                pdf_links.append(href)
        driver.quit()
        return self.format_pdf_links(pdf_links, url)

    def format_pdf_links(self, pdf_links, url):
        parent_url = urlparse(url)
        updated_pdf_links = []
        for pdf_link in pdf_links:
            pdf_url = urlparse(pdf_link)
            pdf_link = pdf_link.strip('/')
            if not pdf_url.scheme:
                if not pdf_url.hostname:
                    pdf_link = f'https://{parent_url.hostname}/{pdf_link}'
                else:
                    pdf_link = f'https://{pdf_link}'
            updated_pdf_links.append(pdf_link)
        return updated_pdf_links

    def extract_pdf_text(self, link):
        page_json = []
        try:
            pdf_link = requests.get(link)
            with io.BytesIO(pdf_link.content) as f:
                pdf = PdfReader(f)
                info = pdf.metadata
                publish_date = self.convert_date(info.get('/ModDate') or info.get('/CreationDate'))
                title = info.get('/Title') or None
                for i, page in enumerate(pdf.pages):
                    text = " ".join(page.extract_text().split("\n"))
                    page_json.append({"number": str(i + 1), "text": text})
            return [publish_date, title, page_json]
        except TypeError:
            return [None, None, None]
        except KeyError:
            breakpoint()
            return [None, None, None]

    def convert_date(self, date):
        date_part = date[2:15]
        postgres_date_string = datetime.strptime(
            date_part, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        (postgres_date_string)
        return postgres_date_string or None