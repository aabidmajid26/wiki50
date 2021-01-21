import markdown2

from django.shortcuts import render
from django.http import HttpResponse
from random import randint


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
    
