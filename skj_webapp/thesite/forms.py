from django import forms

class EmployeeForm(forms.Form):
    
    roles = [
    ('Zaměstnanec', 'Zaměstnanec'),
    ('Pořadatel', 'Pořadatel'),
    ]
    
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    role = forms.CharField(label='Role', widget=forms.Select(choices=roles))
    
class TicketForm(forms.Form):
    
    categories = [
        ('Standard', 'Standard'),
        ('VIP', 'VIP'), 
    ]
    category = forms.CharField(label='Kategorie', widget=forms.Select(choices=categories))
    valid_from = forms.IntegerField()
    valid_to = forms.IntegerField()
    username = forms.CharField(max_length=128)
    
class ValidateTicketForm(forms.Form):
    username = forms.CharField(max_length=128)
    
class TicketListForm(forms.Form):
    categories = [
        ('Standard', 'Standard'),
        ('VIP', 'VIP'), 
    ]
    category = forms.CharField(label='Kategorie', widget=forms.Select(choices=categories))

class FestivalForm(forms.Form):
    name = forms.CharField(max_length=128)
    address = forms.CharField(max_length=128)
    day = forms.IntegerField()
    month = forms.IntegerField()
    year = forms.IntegerField()
    