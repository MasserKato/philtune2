from django import forms
from django.core.mail import EmailMessage
from .models import Music, Stage, Term, Concert


class MusicCreateForm(forms.ModelForm):
    class Meta:
        CHOICES = [('前',1),('中',2),('メイン',3),('その他',4)]
        model = Music
        fields = ('title', 'short_title', 'start_date', 'end_date', 'category',)
        widgets = {
            'start_date': forms.SelectDateWidget,
            'end_date': forms.SelectDateWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class StageCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Stage
        fields = ('state', 'comment',)


class TermCreateForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ('title', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.SelectDateWidget,
            'end_date': forms.SelectDateWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ConcertCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Concert
        fields = ('title', 'date', 'hall', 'url',)
        widgets = {
            'date': forms.SelectDateWidget,
        }