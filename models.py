import uuid
from datetime import date
from django.utils import timezone
from django.db import IntegrityError, models
from django.conf import settings
from libstaff256.models import Entity
    
class ArticleStatus(models.Model):
    name = models.CharField("name", max_length=60, help_text="The name of this status")
    orderpos = models.IntegerField("list position", default=0, help_text="The position for default sorting")
    show = models.BooleanField("show by default", default=True, help_text = "If articles of this status should be shown by default")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ("orderpos",)
    
class Location(models.Model):

    full_name = models.CharField("name", max_length=80, help_text="The full name of this location")
    abbreviation = models.CharField("abbreviation", max_length=10, blank=True, help_text="An abbreviation of the name")

    def __str__(self):
        return self.full_name

class MamodelCategory(models.Model):
        
    name = models.CharField("name", max_length=80, help_text="The name of this category for make/models")
    hide01 = models.BooleanField("hide customfield01", default=False, help_text="Hide custom field 01")
    hide02 = models.BooleanField("hide customfield02", default=False, help_text="Hide custom field 02")
    hide03 = models.BooleanField("hide customfield03", default=False, help_text="Hide custom field 03")
    hide04 = models.BooleanField("hide customfield04", default=False, help_text="Hide custom field 04")
    hide05 = models.BooleanField("hide customfield05", default=False, help_text="Hide custom field 05")
    hide06 = models.BooleanField("hide customfield06", default=False, help_text="Hide custom field 06")
    hide07 = models.BooleanField("hide customfield07", default=False, help_text="Hide custom field 07")
    hide08 = models.BooleanField("hide customfield08", default=False, help_text="Hide custom field 08")
    hide09 = models.BooleanField("hide customfield09", default=False, help_text="Hide custom field 09")
    hide10 = models.BooleanField("hide customfield10", default=False, help_text="Hide custom field 10")
    hide11 = models.BooleanField("hide customfield11", default=False, help_text="Hide custom field 11")
    hide12 = models.BooleanField("hide customfield12", default=False, help_text="Hide custom field 12")
    hide13 = models.BooleanField("hide customfield13", default=False, help_text="Hide custom field 13")
    hide14 = models.BooleanField("hide customfield14", default=False, help_text="Hide custom field 14")
    hide15 = models.BooleanField("hide customfield15", default=False, help_text="Hide custom field 15")
    hide16 = models.BooleanField("hide customfield16", default=False, help_text="Hide custom field 16")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name",]

class Mamodel(models.Model):

    def get_inventory_index_twin_choices():

        inventory_index_twin_choices=[
            ("common_name", "Common Name"),
        ]
        for fieldnum in range(1,17):
            fieldname=f'customfield{fieldnum:02}'
            try:
                fieldlabel = settings.LIBTEKIN["customfields"][fieldname]["label"]
                inventory_index_twin_choices.append((fieldname, fieldlabel))
            except KeyError:
                pass
            
        return inventory_index_twin_choices

    inventory_index_twin = models.CharField("Index field", choices=get_inventory_index_twin_choices, max_length=60, help_text="The article field to be mated with the inventory id.  Ex: If there is a Serial Number field and Serial Number is chosen, then this field and Serial Number will be kept identical")
    category = models.ForeignKey(MamodelCategory, null=True, blank=True, on_delete=models.SET_NULL, help_text="The category of this model")
    brand = models.CharField("Brand", blank=True, max_length=50, help_text="The brand name")
    name = models.CharField("Name",max_length=60, blank=True, help_text="The common name for the model")
    number = models.CharField("Model number",max_length=60, blank=True, help_text="The common name for the model")

    def __str__(self):
        name = self.name if self.name else self.number
        return '{} {}'.format(self.brand, name)
    

class Role(models.Model):

    name = models.CharField("name", max_length=60, help_text="The name of this role")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name",]

class Article(models.Model):

    inventory_index = models.CharField("index", unique=True, max_length=128)
    mamodel = models.ForeignKey(Mamodel, verbose_name="model", null=True, on_delete=models.SET_NULL, help_text="The make and model of this article")
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, help_text="The role of this article")
    status = models.ForeignKey(ArticleStatus, null=True, on_delete=models.SET_NULL, help_text="The status of this article")
    statusdate = models.DateField("status date", null=True, default=date.today, help_text="The date of the current status")
    inventorydate = models.DateField("inventory date", null=True, default=date.today, help_text="The date of the latest confirmation of possetion of this article")
    home_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name="home_articles", help_text="The home location of the article")
    assignee = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_articles", help_text="The person or organization to whom this article is assigned for use")
    responsible_party = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL, related_name="responsible_for", help_text="The person or organization responsible for the condition and availability of this article")
    common_name = models.CharField("common name", max_length=60, blank=True, help_text="The common name, ex:\"Director's Laptop\", \"Meeting Room Projector\"")
    customfield01 = models.CharField("customfield 1", blank=True, max_length=128)
    customfield02 = models.CharField("customfield 2", blank=True, max_length=128)
    customfield03 = models.CharField("customfield 3", blank=True, max_length=128)
    customfield04 = models.CharField("customfield 4", blank=True, max_length=128)
    customfield05 = models.CharField("customfield 5", blank=True, max_length=128)
    customfield06 = models.CharField("customfield 6", blank=True, max_length=128)    
    customfield07 = models.CharField("customfield 7", blank=True, max_length=128)
    customfield08 = models.CharField("customfield 8", blank=True, max_length=128)
    customfield09 = models.CharField("customfield 9", blank=True, max_length=128)
    customfield10 = models.CharField("customfield 10", blank=True, max_length=128)
    customfield11 = models.CharField("customfield 11", blank=True, max_length=128)
    customfield12 = models.CharField("customfield 12", blank=True, max_length=128)    
    customfield13 = models.CharField("customfield 13", blank=True, max_length=128)    
    customfield14 = models.CharField("customfield 14", blank=True, max_length=128)    
    customfield15 = models.CharField("customfield 15", blank=True, max_length=128)    
    customfield16 = models.CharField("customfield 16", blank=True, max_length=128)    

    def __str__(self):

        return self.common_name if self.common_name > "" else self.inventory_index
    
    def get_label(self, customfieldname):
        labelfieldname = "label" + customfieldname[-2]
        return getattr(self.mamodel, labelfieldname)

    def get_field(self, label):
        if label in [
            "mamodel",
            "common_name",
            "role",
            "status",
        ]:
            return getattr(self, label)
        else:
            fields = settings.LIBTEKIN["customfields"]
            for key in fields:
                if fields[key]["label"] == label:
                    return getattr(self, key)

    def save(self, **kwargs):

        self.inventory_index = getattr(self,self.mamodel.inventory_index_twin )
        
        super().save(**kwargs)

        ArticleSnap.objects.create(
            article = self,
            inventory_index=self.inventory_index,
            mamodel=self.mamodel,
            role=self.role,
            common_name=self.common_name,
            status=self.status,
            statusdate=self.statusdate,
            inventorydate=self.inventorydate,
            home_location=self.home_location,
            assignee =self.assignee,
            responsible_party=self.responsible_party,
            customfield01=self.customfield01,
            customfield02=self.customfield02,
            customfield03=self.customfield03,
            customfield04=self.customfield04,
            customfield05=self.customfield05,
            customfield06=self.customfield06,
            customfield07=self.customfield07,
            customfield08=self.customfield08,
            customfield09=self.customfield09,
            customfield10=self.customfield10,
            customfield11=self.customfield11,
            customfield12=self.customfield12,
            customfield13=self.customfield13,
            customfield14=self.customfield14,
            customfield15=self.customfield15,
            customfield16=self.customfield16,
        )


    class Meta:

        ordering = ("mamodel", "common_name",)


class ArticleNoteSubject(models.Model):
    subject_line = models.CharField("subject", max_length=63, help_text="The subject of the note")    
    last_used = models.DateTimeField("date/time", default=timezone.now, help_text="The date of the most recent note")

    def __str__(self):
        return self.subject_line

    class Meta:
        ordering=('last_used',)

class ArticleNote(models.Model):

    lead_note_limit_choices_to={"lead_note__isnull":True}

    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey(ArticleNoteSubject, verbose_name="subject", blank=True, null=True, on_delete=models.CASCADE, help_text="The subject of this note", related_name="children")
    description = models.CharField("description", max_length=255, blank=True, help_text="The description of the note, if appropriate")
    when = models.DateTimeField("date/time", default=timezone.now, help_text="The time that the event occured or the action was taken if appliable, or the time that this note was made")
    is_pinned = models.BooleanField("pinned", default=False, help_text="If this note is both current and important - for examples: for example, if the article is under watch due to problems, has a special condition or feature, is on loan, etc..")

    
    def __str__(self):
        return f'{self.when}: { self.subject }'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.when > self.subject.last_used:
            self.subject.last_used = self.when
            self.subject.save()

    class Meta:
        ordering=('-when',)

class ArticleLink(models.Model):


    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.SET_NULL)
    name=models.CharField("Link Name", max_length=65, blank=True, help_text="The name of the link")
    url=models.URLField(help_text="The URL")

    
    def __str__(self):
        return f'{self.name}: { self.url}' if self.name else self.url

    class Meta:
        ordering=('name','url')

class ArticleSnap(models.Model):

    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.SET_NULL)
    when = models.DateTimeField("date/time", default=timezone.now )
    inventory_index = models.CharField("unique id", max_length=80, help_text="The unique ID to be used for this system. You'll likely want to use the manufacturer's serial number, your organization's inventory number, or bios number, IMEI, etc..")
    mamodel = models.ForeignKey(Mamodel, verbose_name="model", null=True, on_delete=models.SET_NULL, help_text="The make and model of this article")
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, help_text="The role of this article")
    status = models.ForeignKey(ArticleStatus, null=True, on_delete=models.SET_NULL, help_text="The status of this article")
    statusdate = models.DateField("status date", null=True, help_text="The date of the current status")
    inventorydate = models.DateField("status date", null=True, help_text="The date of the current status")
    home_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name="home_location_history", help_text="The article's home location")
    assignee = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_item_history", help_text="The person or organization to whom this article is assigned for use")
    responsible_party = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL, related_name="responsible_for_history", help_text="The person or organization responsible for the condition and availability of this article")
    common_name = models.CharField("common name", max_length=60, help_text="The common name, ex:\"Director's Laptop\", \"Meeting Room Projector\"")
    customfield01 = models.CharField("customfield 1", max_length=128)
    customfield02 = models.CharField("customfield 2", max_length=128)
    customfield03 = models.CharField("customfield 3", max_length=128)
    customfield04 = models.CharField("customfield 4", max_length=128)
    customfield05 = models.CharField("customfield 5", max_length=128)
    customfield06 = models.CharField("customfield 6", max_length=128)    
    customfield07 = models.CharField("customfield 7", max_length=128)
    customfield08 = models.CharField("customfield 8", max_length=128)
    customfield09 = models.CharField("customfield 9", max_length=128)
    customfield10 = models.CharField("customfield 10", max_length=128)
    customfield11 = models.CharField("customfield 11", max_length=128)
    customfield12 = models.CharField("customfield 12", max_length=128)    
    customfield13 = models.CharField("customfield 13", max_length=128)
    customfield14 = models.CharField("customfield 14", max_length=128)
    customfield15 = models.CharField("customfield 15", max_length=128)
    customfield16 = models.CharField("customfield 16", max_length=128)


    def __str__(self):

        return f"{self.when} snap of {self.article}"
            
    class Meta:

        ordering = ("article","when")
