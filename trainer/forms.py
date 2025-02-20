from django import forms
from hr.models import StudentRating

class RatingForm(forms.ModelForm):
    class Meta:
        model = StudentRating
        exclude = ['conducted_by']