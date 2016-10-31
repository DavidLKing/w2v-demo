from django.http import HttpResponseRedirect
# from django.template import loader
from django.shortcuts import render
from .forms import WordsForm
import os
import gensim

directory = os.path.abspath(os.path.dirname(__file__))
print("Loading vectors")
vectors = gensim.models.Word2Vec.load_word2vec_format(os.path.join(directory, './vectors/vectors.bin'), binary=True)

# def index(request):
    # return render(request, open('templates/index.html', 'r'))
    # template = loader.get_templates('similarity/index.html')
    # return render(request, 'similarity/index.html')
    # return HttpResponse(template.render())

# def get_sim(request):
def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print("We got a POST! Request:", request)
        form = WordsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("And it's valid")
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')
            # wordsObj = form.save()
            # print("wordsOBJ", wordsObj)
            # print("valid form", form)
            # print("request.POST", request.POST)
            # return render(request, 'similarity/index.html')
            w1 = request.POST['word1'].lower()
            w2 = request.POST['word2'].lower()
            w3 = request.POST['word3'].lower()
            # all are there
            if w2 != '' and w3 != '':
                if w1 not in vectors or w2 not in vectors or w3 not in vectors:
                    sim = "One of your words is not in vocabulary"
                else:
                    sim = results2html(vectors.most_similar([w1, w2], [w3], topn=10))
            # w1 + w2
            elif w2 != '' and w3 == '':
                if w1 not in vectors or w2 not in vectors:
                    sim = "One of your words is not in vocabulary"
                else:
                    sim = results2html(vectors.most_similar([w1, w2], [], topn=10))
            # w1 - w3
            elif w2 == '' and w3 != '':
                if w1 not in vectors or w3 not in vectors:
                    sim = "One of your words is not in vocabulary"
                else:
                    sim = results2html(vectors.most_similar([w1], [w3], topn=10))
            # w1 only
            elif w2 == '' and w3 == '':
                if w1 not in vectors:
                    sim = "One of your words is not in vocabulary"
                else:
                    sim = results2html(vectors.most_similar([w1], [], topn=10))
            print("sim", sim)
                # sim = "One of those words was never mentioned in Wikipedia"
    # if a GET (or any other method) we'll create a blank form
    else:
        print("We got NO POST")
        form = WordsForm()
        sim = "Please enter 1-3 words first"
    # html = add_results(diff)
    # return render(request, html, {'form': form})
    csspath = 'similarity/css/bootstrap.min.css'
    return render(request, 'similarity/index.html', {'form': form, 'sim': sim, 'csspath': csspath})

def results2html(results):
    print("results", results)
    outstring = ""
    for result in results:
        outstring += result[0] + ": " + str(result[1]) + "<br>"
    return outstring