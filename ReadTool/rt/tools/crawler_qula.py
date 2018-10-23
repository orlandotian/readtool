import requests, re
from lxml import etree
from rt.tools.util import parse_title


def sync_menu():
    r = requests.get('https://www.qu.la/wanbenxiaoshuo/', timeout=5)
    r.encoding='utf-8'
    html = etree.HTML(r.text)
    items = html.xpath("//div[@class='topbooks']//li/a")

    sub_dicts = {}
    for item in items:
        href = item.get('href', '')
        if href and href.startswith('/'):
            sub_dicts['https://www.qu.la' + href] = item.text

    return sub_dicts


def entry(url):
    r = requests.get(url, timeout=5)
    base = re.findall('https?://[a-zA-z]+\.[a-zA-z]+\.[a-zA-z]+', r.url)[0]
    html = etree.HTML(r.text)
    title = html.xpath("//div[@id='info']/h1/text()")[0]
    author = html.xpath("//div[@id='info']/p[1]/text()")[0].replace('作  者：', '')
    summary = "".join(html.xpath("//div[@id='intro']/text()")).replace('\r\n', '').replace(' ', '')
    items = html.xpath("//div[@id='list']/dl/dd/a")

    sub_dicts = {}
    for item in items:
        href = item.get('href', '')
        if href and href.startswith('/'):
            sub_dicts[base + href] = item.text

    return dict(
        title=title,
        author=author,
        summary=summary,
        items=sub_dicts
    )


def detail(url):
    r = requests.get(url, timeout=5)
    base = re.findall('https?://[a-zA-z]+\.[a-zA-z]+\.[a-zA-z]+', r.url)[0]
    html = etree.HTML(r.text)
    content = "".join(html.xpath("//div[@id='content']/text()")).replace('\r\n', '').replace('\t', '').replace(' ', '').replace("　", '')
    title = html.xpath("//div[@class='bookname']/h1/text()")[0]
    index = parse_title(title)
    print(title, r.url)
    return dict(
        index=int(index),
        title=title,
        content=content
    )


if __name__ == '__main__':
    # entry('https://www.qu.la/book/85467/')
    detail('https://www.qu.la/book/85467/4563841.html')