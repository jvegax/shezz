from django import forms


class ProductForm(forms.Form):
    palabras_clave = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'top, azul, flecos, blusa, camiseta...'}))
    talla = forms.ChoiceField(choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), (
        'XXL', 'XXL')], widget=forms.Select(attrs={'class': 'select-input'}), required=True)
    precio_desde = forms.IntegerField(min_value=0, max_value=100, widget=forms.TextInput(
        attrs={'placeholder': 'Precio mínimo'}), required=True)
    precio_hasta = forms.IntegerField(min_value=0, max_value=100, widget=forms.TextInput(
        attrs={'placeholder': 'Precio máximo'}), required=True)

class ProductRecommendationForm(forms.Form):
    idProducto = forms.IntegerField(label='ID del producto', min_value=1)
    
    
class SigninForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)
     
class SignupForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='Nombre', max_length=100)
    last_name = forms.CharField(label='Apellidos', max_length=100)