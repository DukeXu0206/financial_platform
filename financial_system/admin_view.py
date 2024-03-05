from django.shortcuts import render, redirect

from financial_system.models import User, StockInfo, News


def adm_base(request):
    return render(request, 'adm_base.html')

def adm_user(request):
    all_user = User.objects.all()
    context = {
        'all_user': all_user,
    }
    return render(request, "adm_user.html", context)

def adm_stock(request):
    all_stock = StockInfo.objects.all()[:10]
    context = {
        'all_stock': all_stock
    }
    return render(request, "adm_stock.html", context)

def adm_news(request):
    all_news = News.objects.all()
    results = []
    for news in all_news:
        results.append({
            'news_title': news.title[:30],
            'content': news.content[:30],
            'news_id': news.news_id,
            'source': news.source,
            'news_dataTime': str(news.news_dataTime)
        })
    context = {
        'results': results,
    }
    return render(request, "adm_news.html", context)

def adm_news_detail(request, news_id):
    news = News.objects.get(news_id=news_id)
    context = {
        'news': news,
    }
    return render(request, "adm_news_detail.html", context)

def adm_add_news(request):
    if request.POST:
        title = request.POST.get('news_title')
        content = request.POST.get('news_content')
        news = News.objects.create(
            title=title,
            content=content,
        )
        news.save()
    return redirect('financial_system:adm_news')

def adm_delete_news(request, news_id):
    news = News.objects.get(news_id=news_id)
    print(news, "被删除了")
    news.delete()
    return redirect('financial_system:adm_news')


def adm_edit_news(request):
    if request.POST:
        news_id = request.POST.get('news_id')
        news_title = request.POST.get('news_title')
        news_content = request.POST.get('news_content')
        news = News.objects.get(news_id=news_id)
        news.title = news_title
        news.content = news_content
        news.save()
        return redirect('financial_system:adm_news_detail', news_id=int(news_id))
    return redirect('financial_system:adm_news')