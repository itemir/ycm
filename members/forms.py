from django import forms

class MemberForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name', 'style': 'width: 250px;', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name', 'style': 'width: 250px;', 'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'style': 'width: 200px;', 'class': 'form-control'}), required=False)
    website = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Website', 'style': 'width: 300px;', 'class': 'form-control'}), required=False)
    instagram_url = forms.CharField(label='Instagram Link', widget=forms.TextInput(attrs={'placeholder': 'Instagram', 'style': 'width: 400px;', 'class': 'form-control'}), required=False)
    facebook_url = forms.CharField(label='Facebook Link', widget=forms.TextInput(attrs={'placeholder': 'Facebook', 'style': 'width: 400px;', 'class': 'form-control'}), required=False)
    boat_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Boat name', 'style': 'width: 300px;', 'class': 'form-control'}), required=False)
    make_and_model = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Make and model', 'style': 'width: 300px;', 'class': 'form-control'}), required=False)
    year_built = forms.CharField( widget=forms.NumberInput(attrs={'placeholder': 'Year built', 'style': 'width: 300px;', 'class': 'form-control'}), required=False)
    boat_mmsi = forms.CharField(label='Boat MMSI', widget=forms.NumberInput(attrs={'placeholder': 'MMSI', 'style': 'width: 300px;', 'class': 'form-control'}), required=False)
    boat_tracking_url = forms.CharField(label='Tracking Link', widget=forms.TextInput(attrs={'placeholder': 'Tracking link (Garmin or PredictWind)', 'style': 'width: 350px;', 'class': 'form-control'}), required=False)
    privacy_mode = forms.BooleanField(label='Hide Personal Details', required=False)
    boat_privacy_mode = forms.BooleanField(label='Hide Boat Details', required=False)
