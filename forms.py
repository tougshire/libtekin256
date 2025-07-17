from django import forms
from django.conf import settings
from django.urls import reverse_lazy

from .models import Role, Article, ArticleLink, ArticleNoteSubject, ArticleSnap, ArticleStatus, ArticleNote, Location, Mamodel, MamodelCategory

from touglates.widgets import TouglatesRelatedSelect

class RoleForm(forms.ModelForm):
    class Meta:
        model=Role
        fields=[
            "name",
        ]

class LocationForm(forms.ModelForm):
    class Meta:
        model=Location
        fields=[
            "full_name",
            "abbreviation",
        ]



class MamodelSelect(TouglatesRelatedSelect):
 
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-inventory_index_twin"] = value.instance.inventory_index_twin
        return option

class ArticleForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        init = super().__init__(*args, **kwargs)
        popfields=[]
        # relabel custom fieds in accordance with settings
        for field in self.fields:
            if field[:11]=="customfield":
                try:
                    self.fields[field].label=settings.LIBTEKIN["customfields"][field]["label"]
                    try:
                        self.fields[field].help_text=settings.LIBTEKIN["customfields"][field]["help_text"]
                    except KeyError:
                        pass
                except KeyError:
                    popfields.append(field)
        for field in popfields:

            self.fields.pop(field)


        return init

    required_css_class = 'required'

    class Meta:
        model=Article
        fields=[
            "mamodel",
            "common_name",
            "role",
            "status",
            "statusdate",
            "inventorydate",
            "home_location",
            "assignee",
            "responsible_party",
            "customfield01",
            "customfield02",
            "customfield03",
            "customfield04",
            "customfield05",
            "customfield06",
            "customfield07",
            "customfield08",
            "customfield09",
            "customfield10",
            "customfield11",
            "customfield12",
            "customfield13",
            "customfield14",
            "customfield15",
            "customfield16",
        ]
        widgets={
            "mamodel":MamodelSelect(
                related_data={
                    "model_name": "Mamodel",
                    "app_name": "libtekin256",
                    "add_url": reverse_lazy("libtekin256:mamodel-popup"),
                },
                add_filter_input=True,
            ),
            "role":TouglatesRelatedSelect(
                related_data={
                    "model_name": "Role",
                    "app_name": "libtekin256",
                    "add_url": reverse_lazy("libtekin256:role-popup"),
                },
            ),
            "home_location":TouglatesRelatedSelect(
                related_data={
                    "model_name": "Location",
                    "app_name": "libtekin256",
                    "add_url": reverse_lazy("libtekin256:location-popup"),
                },
            ),
            "assignee":TouglatesRelatedSelect(
                related_data={
                    "model_name": "Entity",
                    "app_name": "libstaff256",
                    "add_url": reverse_lazy("libstaff256:entity-popup"),
                },
            )

        }

class ArticleSnapForm(forms.ModelForm):
    class Meta:
        model=ArticleSnap
        fields=[
            'article', 
            'when', 
            'mamodel', 
            'common_name', 
            'role', 
            'status', 
            'statusdate', 
            'inventorydate',
            'customfield01', 
            'customfield02',
            'customfield03',
            'customfield04',
            'customfield05',
            'customfield06',
            'customfield07',
            'customfield08',
            'customfield09',
            'customfield10',
            'customfield11',
            'customfield12',
            'customfield13',
            'customfield14',
            'customfield15',
            'customfield16',
        ]

class ArticleStatusForm(forms.ModelForm):
    class Meta:
        model=ArticleStatus
        fields=[
            "name",
            "orderpos",
            "show",
        ]

class MamodelForm(forms.ModelForm):
    class Meta:
        model=Mamodel
        fields=[
            "inventory_index_twin",
            "brand",
            "name",
            "number",
            "category",
        ]
        widgets={
            'category':TouglatesRelatedSelect(
                related_data={
                    "model_name": "MamodelCategory",
                    "app_name": "libtekin256",
                    "add_url": reverse_lazy("libtekin256:mamodelcategory-popup"),
                },
                add_filter_input=True,
            )
        }
        

class MamodelCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        init = super().__init__(*args, **kwargs)
        popfields=[]

        for field in self.fields:
            if field[:4]=="hide":
                try:
                    self.fields[field].label = "Don't use " + settings.LIBTEKIN["customfields"][field.replace("hide","customfield")]["label"]
                    try:
                        self.fields[field].help_text = "Don't use " + settings.LIBTEKIN["customfields"][field.replace("hide","customfield")]["label"] + " for articles of this category type "
                    except KeyError:
                        pass
                except KeyError:
                    popfields.append(field)
        for field in popfields:
            self.fields.pop(field)

    class Meta:
        model = MamodelCategory
        fields = [
            "name",
            "hide01",
            "hide02",
            "hide03",
            "hide04",
            "hide05",
            "hide06",
            "hide07",
            "hide08",
            "hide09",
            "hide10",
            "hide11",
            "hide12",
            "hide13",
            "hide14",
            "hide15",
            "hide16",
        ]

class ArticleLinkForm(forms.ModelForm):

    class Meta:
        model = ArticleLink
        fields = [
            "article",
            "name",
            "url"
        ]

class ArticleNoteSubjectForm(forms.ModelForm):
    class Meta:
        model = ArticleNoteSubject
        fields = [
            "subject_line"
        ]

class ArticleNoteForm(forms.ModelForm):
    
    class Meta:
        model = ArticleNote
        fields = [
            "article",
            "subject",
            "description",
            "when",
            "is_pinned",
        ]
        widgets = {
            "subject":TouglatesRelatedSelect(
                related_data={
                    "model_name": "ArticleNoteSubject",
                    "app_name": "libtekin256",
                    "add_url": reverse_lazy("libtekin256:articlenotesubject-popup"),
                },
                add_filter_input=True,
            ),
            "description":forms.TextInput(attrs={"class":"wide"}),
            "when":forms.DateTimeInput(attrs={"input_type":"datetime-local"})
        }
    










