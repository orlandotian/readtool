from rt.model import Article, Page
from rt.tools import crawler_qula as qula
from rt.tools.util import parse_title
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from datetime import datetime

executor = ThreadPoolExecutor(max_workers=10)


class BaseCrawler:

    def __init__(self, db):
        self.db = db

    def start_download(self, url):
        if 'www.qu.la' in url:
            op = qula
        else:
            return None

        re_article = op.entry(url)
        article = Article.query.filter_by(url=url).first()
        if not article:
            article = Article()
        article.title = re_article.get('title')
        article.author = re_article.get('author')
        article.summary = re_article.get('summary')
        article.url = url
        article.last_update = datetime.now()

        self.db.session.add(article)
        self.db.session.commit()

        all_task = []
        for key, value in re_article.get('items').items():
            e = executor.submit(self.sub_download, op, key, value, article.id)
            all_task.append(e)

        wait(all_task, return_when=ALL_COMPLETED)
        pass

    def sub_download(self, op, key, value, id):
        index = parse_title(value)
        page = Page.query.filter_by(index=int(index), article_id=id).first()
        if page:
            return
        re_page = op.detail(key)
        page = Page()
        page.article_id = id
        page.index = re_page.get('index')
        page.url = key
        page.title = value
        page.content = re_page.get('content')
        self.db.session.add(page)
        self.db.session.commit()

    def sync_menu(self):
        items = qula.sync_menu()
        for key, value in items.items():
            article = Article.query.filter_by(url=key).first()
            if not article:
                article = Article()
                article.title = value
                article.url = key
                self.db.session.add(article)
                self.db.session.commit()

