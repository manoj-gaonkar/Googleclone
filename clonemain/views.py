from django.shortcuts import render
from bs4 import BeautifulSoup as bs
from django.http import HttpResponse
import requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        res = requests.get('https://www.ask.com/web?q='+search)
        soup = bs(res.text, 'lxml')

        related_list = soup.find_all('li',{'class':'PartialRelatedSearch-item'})
        result_list = soup.find_all('div',{'class':'PartialSearchResults-item'})
        recommend_list = soup.find_all('li',{'class':'ac_even'})

        rec_list = []
        results = []
        related_results = []
        for result in result_list:
            res_title = result.find(class_ = 'PartialSearchResults-item-title').text
            res_url = result.find('a').get('href')
            res_desc = result.find(class_ = 'PartialSearchResults-item-abstract').text
            results.append({'res_title':res_title, 'res_url': res_url, 'res_desc': res_desc})

        for result in related_list:
            rel_title = result.find('a').find(class_ = 'PartialRelatedSearch-item-link-text').text
            rel_url = result.find('a').get('href')
            related_results.append({'rel_title':rel_title, 'rel_url':rel_url , 'ok':"die"})

        for result in recommend_list:
            rec_title = result.find('a').find('span')
            rec_url = result.find('a').get('href')

            recommend_list.append({'rec_title':rec_title,'rec_url':rec_url})
        context = {
            'results':results,
            'related_results': related_results,
        }
        return render(request,'search.html',context)
    else:
        return render(request,'search.html' )
