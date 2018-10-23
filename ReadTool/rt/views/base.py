from flask import Blueprint, render_template, request, flash, redirect
from rt.rt import db
from rt.model import Article, Page
from rt.tools.base_crawler import BaseCrawler

bp = Blueprint('base', __name__)
base_crawler = BaseCrawler(db)


@bp.route('/')
def index():
    articles = Article.query.order_by(Article.count.desc()).all()
    return render_template('index.html', list=articles)


@bp.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'POST' == request.method:
        base_crawler.sync_menu()
    return redirect('/')


@bp.route('/mine')
def mine():
    pid = request.cookies.get('history')
    if not pid:
        flash('没有阅读历史')
        return redirect('/')
    page = Page.query.filter(Page.id == pid).first()
    article = Article.query.filter(Article.id == page.article_id).first()
    return render_template('history.html', item=article, page=page)


@bp.route('/list/<int:id>')
def list(id):
    article = Article.query.filter_by(id=id).first()
    pages = Page.query.filter_by(article_id=id).order_by(Page.index.desc()).all()
    return render_template('list.html', item=article, pages=pages)


@bp.route('/detail/<int:id>')
def detail(id):
    page = Page.query.filter_by(id=id).first()
    article = Article.query.filter_by(id=page.article_id).first()
    article.count += 1
    db.session.add(article)
    db.session.commit()
    next_page = Page.query.filter(Page.index > page.index, Page.article_id == page.article_id).order_by(Page.index.asc()).first()
    prev_page = Page.query.filter(Page.index < page.index, Page.article_id == page.article_id).order_by(Page.index.desc()).first()
    return render_template('detail.html', item=page, next_page=next_page, prev_page=prev_page)


@bp.route('/sync', methods=['GET', 'POST'])
def sync():
    if 'POST' == request.method:
        aid = int(request.form.get('id'))
        article = Article.query.filter_by(id=aid).first()
        base_crawler.start_download(article.url)
        flash('开始抓取')
    return redirect('/list/%d'%aid)


@bp.route('/crawler', methods=['GET', 'POST'])
def crawler():
    if 'POST' == request.method:
        url = request.form.get('url')
        base_crawler.start_download(url)
        flash('开始抓取')
    return render_template('crawler.html')