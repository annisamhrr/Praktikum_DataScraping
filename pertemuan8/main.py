import requests
from bs4 import BeautifulSoup

def scrape_bolasport():
    url = 'https://www.bolasport.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find_all('div', class_='news-list__item clearfix')


def scrape_detik_jatim():
    url = 'https://www.detik.com/jatim'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find_all('article')


def scrape_detik_jateng():
    url = 'https://www.detik.com/jateng'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find_all('article')


def scrape_detik_jabar():
    url = 'https://www.detik.com/jabar'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find_all('article')


def scrape_liputan6():
    url = 'https://www.liputan6.com/citizen6'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = soup.find_all('article', class_='articles--iridescent-list--text-item')
    data = []
    seen = set()

    for article in articles:
        link_tag = article.find('a', class_='articles--iridescent-list--text-item__title-link')
        title_span = article.find('span', class_='articles--iridescent-list--text-item__title-link-text')
        img_tag = article.find('img')

        if not link_tag or not title_span:
            continue

        title = title_span.get_text(strip=True)
        link = link_tag['href']

        image = ''
        if img_tag:
            image = (
                img_tag.get('data-src') or
                img_tag.get('src') or
                img_tag.get('data-original') or
                ''
            )

        if title not in seen:
            data.append({'title': title, 'link': link, 'image': image})
            seen.add(title)

    return data


def scrape_cnnindonesia():
    url = 'https://www.cnnindonesia.com/gaya-hidup'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    data = []
    anchors = soup.find_all('a', class_='flex group items-center gap-4')

    for anchor in anchors:
        link = anchor.get('href')
        img_tag = anchor.find('img')
        h2_tag = anchor.find('h2')

        if not link or not img_tag or not h2_tag:
            continue

        image = img_tag.get('src', '')
        title = h2_tag.get_text(strip=True)

        data.append({
            'title': title,
            'link': link,
            'image': image
        })

    return data


def scrape_detail_berita(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Liputan6
    title = soup.find('h1', class_='read-page--header--title')
    if title:  
        title = title.get_text(strip=True)

        img_url = ''
        gallery_div = soup.find('div', class_='read-page--photo-gallery--item__content')
        if gallery_div:
            img_tag = gallery_div.find('img')
            if img_tag:
                img_url = img_tag.get('data-src') or img_tag.get('src') or ''

        content_div = soup.find('div', class_='article-content-body__item-page')
        content_html = str(content_div) if content_div else ''

        return {'title': title, 'image': img_url, 'content': content_html}

    # CNN Indonesia
    title = soup.find('h1', class_='mb-2 text-[32px] text-cnn_black font-merriweather')
    if title:  
        title = title.get_text(strip=True)
        img_tag = soup.find('img', class_='w-full')
        img_url = img_tag.get('src', '') if img_tag else ''
        content_div = soup.find('div', class_='detail-text text-cnn_black text-sm grow min-w-0')
        content_html = str(content_div) if content_div else ''
        return {'title': title, 'image': img_url, 'content': content_html}

    return {'title': 'Berita tidak ditemukan', 'image': '', 'content': ''}