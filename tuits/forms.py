from django import forms


class NewTuitForm(forms.Form):
    tuit_text = forms.CharField(label='Enter yout tuit here', max_length=280)

