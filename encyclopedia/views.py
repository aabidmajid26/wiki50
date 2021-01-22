import markdown2
import re

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from random import randint
from django.urls import reverse


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title" : "Encyclopedia"
    })

def open_entry(request,name):
    z = util.get_entry(name)
    if not z:
        z = util.get_entry(name.capitalize())
    if not z:
        z = util.get_entry(name.upper())
    if (z):
        return render(request, 'encyclopedia/entry.html', {
            "content":markdown2.markdown(z),
            "title" : name
        })
    else:
        return render(request, 'encyclopedia/notfound.html', {
            "error" : "Oops! Page Not Found!",
            "title" : "Sorry"
        })


def random(request):
    all_entries = util.list_entries()
    i = randint(0,len(all_entries)-1)
    if len(all_entries)==0:
        return render(request, 'encyclopedia/notfound.html', {
            "error" : "No Entry to Show!",
            "title" : "Sorry"
        })
    else:
        z = all_entries[i]
        return open_entry(request, z)
    return HttpResponse(z)

def new_entry(request):
    if request.method == 'POST':
        filename = request.POST['topic_name'].split()[0]
        if filename in util.list_entries(): 
            return render(request, 'encyclopedia/notfound.html',{
                "error" : "Sorry! This Page Already Exists!",
                "title" : "Collision"
        })
        content = request.POST['body']
        util.save_entry(filename, content)
        return HttpResponseRedirect(reverse('open_entry',args=(filename,)))


    return render(request, 'encyclopedia/new_entry.html')

def search(request):
    query = request.GET['q'].lower()
    all_names = util.list_entries()
    case_insens = [name.lower() for name in all_names]
    if query in case_insens:
        return open_entry(request, query)
    search_results = []
    for s in all_names:
        sr = re.search(rf"{query}[0-9a-zA-Z]*",s, re.IGNORECASE)
        if sr != None:
            search_results.append((s,sr.start()))
    search_results = list(sorted(search_results, key= lambda x : x[1]))
    search_results = [sr[0] for sr in search_results]
    if not len(search_results):
        return render(request, "encyclopedia/notfound.html", {
            "error" : "No Match Found for the Query! If you want to write an article about this; click on Create New Page",
            "title" : "Try Again!"
        })
    return render(request, "encyclopedia/index.html", {
        "entries" : search_results,
        "title"   : "Search Results"
    })

    