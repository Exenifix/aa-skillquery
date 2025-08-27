from django import forms


class SkillForm(forms.Form):
    skill_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control skill-name", "placeholder": "Enter skill name", "autocomplete": "off"}
        ),
    )
    skill_id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={"class": "skill-id"}))


class SkillsetForm(forms.Form):
    skill_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control skill-name", "placeholder": "Enter skill name", "autocomplete": "off"}
        ),
    )
    skill_id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={"class": "skill-id"}))
    min_level = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control level-input", "placeholder": "Level", "min": "1", "max": "5"}
        ),
    )
