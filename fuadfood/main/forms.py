from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    title       = forms.CharField(label='', widget=forms.TextInput(attrs={
                                                            "placeholder":"Your Title"
                                                }))
    description = forms.CharField(
                                    required=False, 
                                    widget=forms.Textarea(
                                        attrs={
                                            "placeholder":"Your Description",
                                            "rows":10,
                                            "cols":20
                                        }
                                    ))     
    price       = forms.DecimalField(initial=199.99, required=True) 
    class Meta:
        model=Item
        fields=[
             'title',
             'description',
             'price', 
             'image',
             'created_by',
             'label',
             'label_colour'
         ]

