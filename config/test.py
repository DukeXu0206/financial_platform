
def gen_news():
    ua = UserAgent()
    user_agent = ua.random()

    referer = 'https://tushare.pro/login?next=%2Fnews%2Fnews_sina'

    headers = {
        'User-Agent': user_agent,
        'Host': 'tushare.pro',
        'Origin': 'https://tushare.pro',
        'Referer': referer
    }

    stockPageRequest = request.urlopen('http://finance.eastmoney.com/news/cdfsd.html')
    htmlTitleContent = str(stockPageRequest.read(), 'utf-8')
    # 正则匹配标题
    titlePattern = re.compile('<span class="l3 a3">title="(.*?)"</span>', re.S)
    p_title = 'title="(.*?)"(.*?)'
    title = re.findall(p_title, htmlTitleContent)
    title = [t[0] for t in title if not t[0].find('【')]

    news = []
    for t in title:
        a = t.find('【')
        b = t.find('】')
        news.append({'title': t[a+1:b], 'content': t[b+1:]})
    # news = News.objects.all()
    return news


news_list = gen_news()

print(news_list)