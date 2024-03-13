import random
from faker import Faker

fake = Faker()

def generate_stock_news():
    stock_names = ['Apple Inc.', 'Microsoft Corporation', 'Alphabet Inc.', 'Amazon.com Inc.', 'Tesla Inc.']
    news_titles = ['Announces Quarterly Earnings', 'Launches New Product', 'CEO Resigns Unexpectedly',
                   'Stock Price Surges After Positive Earnings Report', 'Investors React to Market Volatility']

    stock_news = []

    for _ in range(30):
        news_item = {
            'stock_name': random.choice(stock_names),
            'title': random.choice(news_titles),
            'content': fake.text(max_nb_chars=300),
            'published_date': fake.date_this_year(),  # 随机生成当前年份内的日期
            'source': fake.company()  # 随机生成公司名作为虚构的新闻来源
        }
        stock_news.append(news_item)

    return stock_news

# 生成虚拟的股票金融新闻
virtual_stock_news = generate_stock_news()

# 打印生成的新闻
for index, news in enumerate(virtual_stock_news, start=1):
    print(f"{index}. {news['stock_name']} - {news['title']} ({news['published_date']})")
    print(f"   {news['content']}")
    print(f"   Source: {news['source']}")
    print()
