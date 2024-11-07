from captcha.fields import CaptchaField
from django import forms

from .models import Address, Tarif, Electro, Water
from .utils import DataMixin


class VibAddressForm( forms.ModelForm ):
    # объекты адреса -> выбранный объект
    vib_adr = forms.ModelChoiceField( queryset=Address.objects.all(), empty_label="Выбрать адрес", label="Адрес" )

    class Meta:
        model = Address
        fields = ['vib_adr']

# -----------------------------------------------------
class AddElectroForm( forms.ModelForm ):
    class Meta:
        model = Electro
        fields = [ 'date_reading', 'nighttime', 'daytime']
        widgets = {
            'date_reading': forms.DateInput(attrs={'type': 'date'}),
        }
# -----------------------------------------------------
class AddElectroDaylyForm( forms.ModelForm ):
    class Meta:
        model = Electro
        fields = [ 'date_reading', 'dayly']
        widgets = {
            'date_reading': forms.DateInput(attrs={'type': 'date'}),
        }
# -----------------------------------------------------
class NewElectroForm( forms.ModelForm ):
    #addr = forms.ModelChoiceField( queryset=Address.objects.all(), empty_label="Выбрать адрес", label="Адрес" )
    tar = forms.ModelChoiceField(queryset=Tarif.objects.all(), empty_label="Выбрать тариф", label="Тариф")
    #tar_txt = forms

    class Meta:
        model = Electro
        fields = ['tar', 'date_reading','nighttime', 'daytime', 'dayly']
        widgets = {
            'date_reading': forms.DateInput(attrs={'type': 'date'}),
        }
# -----------------------------------------------------
class AddWaterForm(forms.ModelForm ):
    class Meta:
        model = Water
        fields = ['date_reading','hot', 'cold']
        widgets = {
            'date_reading': forms.DateInput(attrs={'type': 'date'}),
        }
# -----------------------------------------------------
class NewWaterForm(forms.ModelForm ):
    class Meta:
        model = Water
        fields = ['date_reading','hot', 'cold']
        widgets = {
            'date_reading': forms.DateInput(attrs={'type': 'date'}),
        }



#------------------------------------------------------------------------
class ItemElectroForm(forms.ModelForm ):
    class Meta:
        model = Electro
        fields = ['date_reading','nighttime', 'daytime', 'dayly']

#------------------------------------------------------------------------
class ItemWaterForm(forms.ModelForm ):
    class Meta:
        model = Water
        fields = ['date_reading','hot', 'cold']

# ------------------------------
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()