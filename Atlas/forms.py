class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'emotional_tone', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }
