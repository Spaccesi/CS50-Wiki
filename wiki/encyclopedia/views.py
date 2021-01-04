from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request, entries = util.list_entries()):
    return render(request, "encyclopedia/index.html", { 
        'entries': entries
        })

def entry(request, title):
	# 1. get the content of the encyclopedia entry
	# 2. If an entry is requested that does not exist, the user should be presented with an error page
	# 3. If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.
	if util.get_entry(title) is not None:
		return render(request, "encyclopedia/entry.html", {
			"title": title.capitalize(),
			"content": markdown2.markdown(util.get_entry(title))
			})
	else: return render(request, "encyclopedia/error.html")

def search(request):
    # 1. get the value from the search bar
    # 2. if the value is found return the entry
    # 3. if is not return the posibilities and/or create new one
    q = request.GET.get('q', '')
    if util.get_entry(q) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': q }))
    else:
        posibilities = []
        for i in util.list_entries():
            if q.upper() in i.upper():
                posibilities.append(i)
        return render(request, "encyclopedia/index.html", { 
        'entries': posibilities,
        'search': True,
        'q': q
        })