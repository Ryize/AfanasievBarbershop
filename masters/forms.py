from django import forms


class ChairMonForm(forms.Form):
    chair_num = forms.IntegerField(widget=forms.HiddenInput())
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'input_style', 'disabled': 'disabled',
                                                               'value': '09:00'}))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'input_style', 'disabled': 'disabled',
                                                             'value': '15:00'}))
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'input_style', 'disabled': 'disabled'}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'class': 'input_style', 'disabled': 'disabled'}))
