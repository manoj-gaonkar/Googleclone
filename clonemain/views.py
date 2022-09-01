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

        result_list = soup.find_all('div',{'class':'PartialSearchResults-item'})

        results = {}
        for result in result_list:
            res_title = result.find(class_ = 'PartialSearchResults-item-title').text
            res_url = result.find('a').get('href')
            res_desc = result.find(class_ = 'PartialSearchResults-item-abstract').text

            results = {'res_title':res_title, 'res_url': res_url, 'res_desc': res_desc}

        context = {
            'results':results,
        }
        return render(request,'search.html',context)
    else:
        return render(request,'search.html' )
