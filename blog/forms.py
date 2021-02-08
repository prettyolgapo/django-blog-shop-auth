from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class ContactForm(forms.Form):
    my_default_errors = {
        'required': 'This field is required',
        'invalid': 'Enter a valid value'
    }  # в шаблоне contact.html отменить встроенную проверку данных, добавив аттрибут novalidate

    error_css_class = "has-error"

    name = forms.CharField(help_text="Введите свое имя",
                           widget=forms.TextInput(attrs={'placeholder': 'Enter Your Name',
                                                         "class": "form-control name"}),
                           error_messages=my_default_errors)

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Your E-Mail',
                                                            "class": "form-control email"}),
                             error_messages=my_default_errors)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Your Message',
                                                           "class": "form-control"}),
                              error_messages=my_default_errors)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass





