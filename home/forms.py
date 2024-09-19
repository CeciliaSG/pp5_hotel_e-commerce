from django import forms


class ContactForm(forms.Form):
    """
    A Django form for handling contact submissions.

    This form collects the user's name, email address, and message.
    It is intended to be used in a contact page where users can submit
    their inquiries or feedback.

    Fields:
    - name: A CharField to capture the user's name, limited to 100 characters.
    - email: An EmailField to capture the user's email address, ensuring it is
    in a valid email format.
    - message: A CharField with a Textarea widget to capture the user's message
    or inquiry, allowing for multiline text input.
    """

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
