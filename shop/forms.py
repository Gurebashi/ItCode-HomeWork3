from django.contrib.auth.forms import UserCreationForm
from shop import models



class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields+('email',)
