from django import forms 
from django.forms import ModelForm
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'value',)

        labels = {
                'value': 'Поставьте оценку проекту',
                'body': 'Добавьте отзыв о проекте'
            }

    def init(self, *args, **kwargs):
        super(ReviewForm, self).init(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})