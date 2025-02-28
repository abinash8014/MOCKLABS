from django import forms
from hr.models import *

class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Schedulings
        exclude = ['slot_id']
        