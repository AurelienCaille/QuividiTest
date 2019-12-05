from django.forms import ModelForm, Form, ModelChoiceField, IntegerField
from .models import Notation, Author
from django.core.validators import MaxValueValidator, MinValueValidator



class NoteBookForm(ModelForm):
    class Meta:
        model = Notation
        fields = '__all__'


class FilterBookForm(Form):
    
    author = ModelChoiceField(queryset=Author.objects.all())
    notation = IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])


    
