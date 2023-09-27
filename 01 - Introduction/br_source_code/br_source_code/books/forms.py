from django import forms 
from .models import BookTitle
from django.core.exceptions import ValidationError

class BookTitleForm(forms.ModelForm):
    class Meta:
        model = BookTitle
        fields = ('publisher', 'author', 'title')
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'border bg-purple-200 rounded-xl p-3'}),
        #     'author': forms.Select(attrs={'class': 'border bg-purple-200 rounded-xl p-3'}),
        #     'publisher': forms.Select(attrs={'class': 'border bg-purple-200 rounded-xl p-3'})
        # }

    def clean(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            error_msg = 'the title is too short'
            self.add_error('title', error_msg)
            # raise ValidationError(error_msg)
        
        book_tile_exists = BookTitle.objects.filter(title__iexact=title).exists()

        if book_tile_exists:
            self.add_error('title', 'this book title already exists')

        return self.cleaned_data