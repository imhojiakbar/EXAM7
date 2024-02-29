from django import forms

from apps.main.models import Product


class ProductCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                    {"class": "form-control", "placeholder": f"Enter the {str(field)}"})

    class Meta:
        model = Product
        fields = ("title", "description", "price", 'category','ends_in','owner', 'image')


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("title", "description", "price", 'category','ends_in','owner', 'image')