from django import forms
from django.core.mail import EmailMessage
from .models import Schedule, Reaction


class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class ScheduleCreateForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('title', 'detail', 'location', 'url', 'date', 'start_at', 'end_at', 'music')
        widgets = {
            'date': forms.SelectDateWidget,
            'start_at': forms.TimeInput(format='%H:%M'),
            'end_at': forms.TimeInput(format='%H:%M'),
            'music': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
"""

class ReactionCreateForm(forms.ModelForm):
    CHOICES = [('出席','出席'),('欠席','欠席'),('遅刻','遅刻'),('早退','早退')]
    state = forms.ChoiceField(label='回答', choices=CHOICES,widget=forms.RadioSelect)
    comment = forms.CharField(label='コメント', required=False)

    class Meta:
        model = Reaction
        fields = ('state', 'comment',)

    def clean_email(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 40:
            raise forms.ValidationError('コメントは40文字以内にしてください。')