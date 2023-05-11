from mrq.task import Task
from .views import scrape_data

class ScrapeDataTask(Task):
    def run(self, url):
        scrape_data(url)