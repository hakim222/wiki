from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import markdown2


class NewTasksForm(forms.Form):
    form = forms.CharField(label="New Task")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    
    title = util.get_entry(title)

    if title is not None:
        return render(request, "encyclopedia/title.html", {
            "entry": markdown2.markdown(title),
            "title": title
        })
    
    else:
        return render(request, "encyclopedia/error.html")

# def search(request):
#     if request.method == "POST":
#         search = NewTasksForm(request.POST)
#         if search.is_valid():
#             search = search.cleaned_data["form"]
#             return HttpResponseRedirect(reverse("title", [search]))
  