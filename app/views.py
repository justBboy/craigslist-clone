import requests
import re
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_URL = 'https://losangeles.craigslist.org/search/?query={}'

# Create your views here.

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    response = requests.get(BASE_URL.format(quote_plus(search)))
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_="result-image").get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)

        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_postings.append((post_title, post_url, post_image_url))
    context = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'app/new_search.html', context)