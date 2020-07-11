from django.shortcuts import render

from . import util
import markdown2


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

