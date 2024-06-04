from django.shortcuts import render,redirect
from . import util
from markdown2 import Markdown  
mardowner= Markdown()
from django import forms
class SearchForm(forms.Form):
    search = forms.CharField(min_length=1,
                              widget=forms.TextInput(attrs={'class': 'search'}))
    
class NewPageForm(forms.Form):
    title = forms.CharField(min_length=1,
                            label="Title:",
                            widget=forms.TextInput(attrs={'class': 'title'}))
    content = forms.CharField(min_length=1,
                                label="Content:",
                              widget=forms.Textarea(attrs={'class': 'content'}))
class EditPageForm(forms.Form):
    content = forms.CharField(min_length=1,
                              max_length=1000,
                                label="Content:",
                              widget=forms.Textarea(attrs={'class': ''}))

def index(request):
    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form
    })


def content(request, content):
    page = util.get_entry(content)
    form = SearchForm()
    if page is None:
        return render(request, "encyclopedia/NotFound.html",{
            "form": form
        })
    else:
        converted = mardowner.convert(page)
        return render(request, "encyclopedia/content.html", {
            "content": converted,
            "title": content,
            "form": form
        })

def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]
            search.lower()
            entries = util.list_entries()
            
            if search in entries:
                return content(request, search)
            else:
                results = []
                for entry in entries:
                    if search.lower() in entry.lower():
                        results.append(entry)
               
                if len(results) == 0:
                    return render(request, "encyclopedia/NotFound.html",{
                        "form": form
                    })
                return render(request, "encyclopedia/searchresults.html",
                              {
                                  "form":form,
                                  "entries": results,
                              })
        else:
            return index(request)
        

def NewPage(request):
    newpageForm = NewPageForm()
    form = SearchForm()
    if request.method == "POST":
        newpageForm = NewPageForm(request.POST)
        if newpageForm.is_valid():
            title = newpageForm.cleaned_data["title"]
            content = newpageForm.cleaned_data["content"]
            entries = util.list_entries()
            entries = [entry.lower() for entry in entries]
            if title.lower() in entries:
                return render(request, "encyclopedia/newpage.html",{
                    "newpage_form": newpageForm,
                    "form": form,
                    "error": "Title already exists"
                })
            else:
                util.save_entry(title, content)
                return redirect("/")
      
    else:
        return render(request, "encyclopedia/newpage.html", {
            "newpage_form": newpageForm,
            "form": form,
        })
    
def edit(request, title):
    # Fetch the entry content
    content = util.get_entry(title)
    print(content)
    if content is None:
        return render(request, "encyclopedia/NotFound.html")
    
   

    if request.method == "POST":
        # Populate form with POST data
        editPage = EditPageForm(request.POST)
        
        if editPage.is_valid():
            # Clean and strip the content again to avoid adding extra new lines
            content = editPage.cleaned_data["content"]
            content = content.replace("\r", "")
            util.save_entry(title, content)
            return redirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/editpage.html", {
                "editpage_form": editPage,
                "title": title
            })
    else:
        # GET request - populate form with existing content
        editPage = EditPageForm(initial={'content': content})
        return render(request, "encyclopedia/editpage.html", {
            "editpage_form": editPage,
            "title": title
        })



def randomPage(request):
    import random
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return content(request, random_entry)