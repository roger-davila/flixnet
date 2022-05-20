from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self:
            visible.field.widget.attrs.update(
                {'class': 'form-control tbd-bg-secondary text-white'})


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self:
            visible.field.widget.attrs.update(
                {'class': 'form-control tbd-bg-secondary text-white'})
