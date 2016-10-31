from django import forms

class WordsForm(forms.Form):
    word1 = forms.CharField(label='', max_length=100)
    word3 = forms.CharField(label=' is to ', max_length=100, required=False)
    word2 = forms.CharField(label=' as ', max_length=100, required=False)
