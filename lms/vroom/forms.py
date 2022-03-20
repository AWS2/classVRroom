from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    print(self.fields['username'].label)
    self.fields['username'].widget.attrs.update(
      {'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600'}
    )