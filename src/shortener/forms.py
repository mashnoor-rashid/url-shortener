from django import forms
from .validators import validate_url, validate_dot_com

class SubmitUrlForm(forms.Form):
    url = forms.CharField(
            label='',
            validators=[validate_url,validate_dot_com],
            widget= forms.TextInput(
                    attrs={"placeholder":"Long URL",
                            "class":"form-control"
                        }
                )
            )

    # Doing validation within form
    # def clean(self):
    #     cleaned_data = super(SubmitUrlForm, self).clean()
    #     url = cleaned_data.get('url')
    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError("Invalid URL for this field")
    #     return url
