from django.test import TestCase
from django.conf import settings

from libtekin256.models import Article, Role, ArticleStatus, ArticleNote, Mamodel, MamodelCategory
from libtekin256.forms import ArticleForm, MamodelForm

class ArticleTestCase(TestCase):
    def setUp(self):

        settings.LIBTEKIN["customfields"]={
            "customfield01":{
                "label":"Serial Number",
                "help_text":"The Serial Number"
            },
            "customfield02":{
                "label":"Asset Tag",
                "help_text":"The Asset Tag"
            }
        }

        test_id = "012345"
        gad2025 = Mamodel.objects.create(brand="Tougshire", name="Gad 2025", inventory_index_twin="customfield01")
        maingadget = Article.objects.create(mamodel=gad2025, common_name="Main Gadget", customfield01=test_id )

    def test_id_twin_field(self):
        test_id = "012345"
        maingadget = Article.objects.get(inventory_index=test_id)
        self.assertEqual(maingadget.customfield01, test_id)
        self.assertEqual(maingadget.get_field("Serial Number"), test_id)

class ArticleNoteTestCase(TestCase):

    def setUp(self):
        test_id = "012345"
        gad2025 = Mamodel.objects.create(brand="Tougshire", name="Gad 2025", inventory_index_twin="customfield01")
        self.maingadget=Article.objects.create(mamodel=gad2025, common_name="Main Gadget", inventory_index=test_id )

    def test_maintenancenote_children(self):
        lead_1 = ArticleNote.objects.create(article=self.maingadget, action_taken="Started Something")
        followon_1_1 = ArticleNote.objects.create(article=self.maingadget, action_taken="Worked on Something", lead_note=lead_1)
        followon_1_2 = ArticleNote.objects.create(article=self.maingadget, action_taken="Finished Something", lead_note=lead_1)

        self.assertQuerySetEqual(lead_1.children.all(), ArticleNote.objects.exclude(action_taken="Started Something"))
        self.assertEqual(lead_1.get_lead_or_self(), lead_1)
        self.assertEqual(followon_1_1.get_lead_or_self(), lead_1)
        self.assertEqual(followon_1_2.get_lead_or_self(), lead_1)

        lead_2 = ArticleNote.objects.create(article=self.maingadget, action_taken="Started Something else")
        followon_2_1 = ArticleNote.objects.create(article=self.maingadget, action_taken="Worked on Something else", lead_note=lead_2)
        followon_2_2 = ArticleNote.objects.create(article=self.maingadget, action_taken="Finished Something else", lead_note=lead_2)

        print(ArticleNote.objects.all().order_by('-get_lead_or_self__when', '-when'))
        

class ArticleFormTestCase(TestCase):
    def setUp(self):

        settings.LIBTEKIN["customfields"]={
            "customfield01":{
                "label":"Serial Number",
                "help_text":"The Serial Number"
            },
            "customfield02":{
                "label":"Asset Tag",
                "help_text":"The Asset Tag"
            }
        }

    def test_article_form_label(self):
        article_form = ArticleForm()
        output = str(article_form)
        self.assertIn(">Serial Number:<", output)
        self.assertIn(">Asset Tag:<", output)

class MamodelFormTestCase(TestCase):

    def test_inventory_index(self):
        mamodel_form = MamodelForm()
        output = str(mamodel_form)
        self.assertIn("customfield01\">Serial Number", output)
        self.assertIn("customfield02\">Asset Tag", output)

class ArticleFormTestCase(TestCase):

    def setUp(self):

        settings.LIBTEKIN["customfields"]={
            "customfield01":{
                "label":"Serial Number",
                "help_text":"The Serial Number"
            },
            "customfield02":{
                "label":"Asset Tag",
                "help_text":"The Asset Tag"
            }
        }

        mamodel = Mamodel.objects.create(
            name="test mamodel",
            inventory_index_twin = "customfield01",

        )


    def test_inventory_index(self):
        mamodel = Mamodel.objects.get(name="test mamodel")
        article_form = ArticleForm(data={"mamodel":mamodel})
        print(article_form._meta.fields)
        self.assertEqual(article_form["mamodel"].data, mamodel)
