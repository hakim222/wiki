from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import markdown2


class NewTasksForm(forms.Form):
    form = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'search', 'placeholder':'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'id':'title', 'placeholder':'Title', 'class':'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'id':'content', 'placeholder':'Content', 'class':'form-control', 'rows':'18'}))
    
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
                    errmessage = "Requested page does not exist"
                    return HttpResponseRedirect(reverse("error", kwargs={"message":errmessage}))

def new(request):
    if request.method == "POST":
        entries = util.list_entries()
        new_page_form = NewPageForm(request.POST)
        if new_page_form.is_valid():
            new_title = new_page_form.cleaned_data["title"]
            new_content = new_page_form.cleaned_data["content"]
            if new_title in entries:
                errmessage = "Title already exist, please provide another title"
                return HttpResponseRedirect(reverse("error", kwargs={"message":errmessage}))
            else:
                util.save_entry(new_title, new_content)
                return HttpResponseRedirect(reverse("title", kwargs={"title":new_title}))
    else:
        new_page_form = NewPageForm()
        return render(request, "encyclopedia/new.html", {
            "new_title_form": new_page_form["title"],
            "new_content_form": new_page_form["content"],
            "search_form": search_form
        })

def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "search_form": search_form,
        "message": message
    })
