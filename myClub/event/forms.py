# This file is used to create a form for the Vanue model. This form is used to create a new Vanue object in the database.
from django import forms
from .models import Vanue, Event


class VanueForm(forms.ModelForm):
    class Meta:
        model = Vanue
        fields = ('name', 'address', 'phone', 'map_reference', 'image')

        labels = {
            'name':'',
            'address':'',
            'phone':"",
            'map_reference':"",
            'image':"",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vanue Name'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Vanue Address'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'map_reference': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
            'image': forms.FileInput(attrs={'class':'form-control', 'placeholder':'Vanue Image'})
        }
# for superuser
class EventFormAdmin(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title',  'date', 'manager', 'vanue', 'attend', 'description',)

        labels = {
            'title':'',
            'date':"YYYY-MM-DD HH:MM:SS",
            'manager':"Manager",
            'vanue':"Vanue",
            'attend':"",
            'description':'',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Title'}),
            'date': forms.DateTimeInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Event Manager'}),
            'vanue': forms.Select(attrs={'class':'form-select', 'placeholder':'Event Vanue'}),
            'attend': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Event Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Event Description'})
        }
    
#For normal user
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title',  'date', 'vanue', 'attend', 'description', )

        labels = {
            'title':'',
            'date':"YYYY-MM-DD HH:MM:SS",
            'vanue':"Vanue",
            'attend':"",
            'description':'',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Title'}),
            'date': forms.DateTimeInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'vanue': forms.Select(attrs={'class':'form-select', 'placeholder':'Event Vanue'}),
            'attend': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Event Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Event Description'})
        }