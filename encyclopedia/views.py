from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import markdown2


class NewTasksForm(forms.Form):
    form = forms.CharField(label="search form", widget=forms.TextInput(attrs={'class':'search', 'placeholder':'Search Encyclopedia'}))

search_form = NewTasksForm()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": search_form
    })

def title(request, title):
    
    title = util.get_entry(title)

    if title is not None:
        return render(request, "encyclopedia/title.html", {
            "entry": markdown2.markdown(title),
            "title": title,
            "search_form": search_form
        })
    
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        searched_form = NewTasksForm(request.POST)
        if searched_form.is_valid():
            search = searched_form.cleaned_data["form"]
            if search in entries:
                return HttpResponseRedirect(reverse("title", kwargs={"title":search}))
            else:
                results = []
                for entry in entries:
                    if search in entry:
                        results.append(entry)
                if len(results) > 0:
                    return render(request, "encyclopedia/search.html", {
                        "entries": results,
                        "search_form": search_form
                    })            
                else:
                    return render(request, "encyclopedia/error.html", {
                        "search_form": search_form
                    })