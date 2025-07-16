import uuid

import re
import logging

from django.db import IntegrityError
from django.http import HttpResponseRedirect

from django_filters_stoex.forms import FilterstoreRetrieveForm, FilterstoreSaveForm
from django_filters_stoex.views import FilterView
from libtekin256.forms import LocationForm
from libtekin256.filterset import ArticleFilter
from .models import ArticleCategory, Article, ArticleNoteSubject, ArticleSnap, ArticleStatus, ArticleLink, ArticleNote, Location, Mamodel, MamodelCategory
from .forms import ArticleForm, ArticleNoteSubjectForm, ArticleSnapForm, ArticleCategoryForm, ArticleLinkForm, ArticleStatusForm, ArticleNoteForm, MamodelForm, MamodelCategoryForm
from django.forms.utils import pretty_name
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.forms import inlineformset_factory
from django.apps import apps

logger = logging.getLogger(__name__)

def get_pretty_labels(Model):

    labels = {}
    fields = Model._meta.get_fields()

    for field in fields:

        if field.name[:11]=="customfield":
            try:
                labels[field.name]=settings.LIBTEKIN["customfields"][field.name]["label"]
            except KeyError:
                pass
        else:
            try:
                labels[field.name] = pretty_name(Model._meta.get_field(field.name).verbose_name)
            except AttributeError as e:
                labels[field.name] = pretty_name(Model._meta.get_field(field.name).related_name)

    return labels

class ArticleCategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "libtekin256.add_articlecategory"
    model = ArticleCategory
    form_class = ArticleCategoryForm

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("libtekin256:articlecategory-update", kwargs={"pk": self.object.pk})

class ArticleCategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "libtekin256.change_articlecategory"
    model = ArticleCategory
    form_class = ArticleCategoryForm

    def get_success_url(self):
        return reverse_lazy("libtekin256:articlecategory-detail", kwargs={"pk": self.object.pk})

class ArticleCategoryDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "libtekin256.view_articlecategory"
    model = ArticleCategory

class ArticleCategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "libtekin256.delete_articlecategory"
    model = ArticleCategory

    def get_success_url(self):
        return reverse_lazy("libtekin256:articlecategory-list", kwargs={"pk": self.object.pk})

class ArticleCategoryListView(PermissionRequiredMixin, ListView):
    permission_required = "libtekin256.view_articlecategory"
    model = ArticleCategory

class LocationCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "libtekin.add_location"
    model = Location
    form_class = LocationForm

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("libtekin256:location-detail", kwargs={"pk": self.object.pk})


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "libtekin256.add_article"
    model = Article
    form_class = ArticleForm

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        formsetclasses = {
            "articlelinks": inlineformset_factory(Article, ArticleLink, ArticleLinkForm, extra=3),
            "maintenancenotes": inlineformset_factory(Article, ArticleNote, ArticleNoteForm, extra=1)

        }

        for formsetclass in formsetclasses:

            if self.request.POST:            
                context_data[formsetclass] = formsetclasses[formsetclass](self.request.POST, instance=self.object)
            else:
                context_data[formsetclass] = formsetclasses[formsetclass](instance=self.object)

        return context_data

    def form_valid(self, form):
    
        response = super().form_valid(form)
        formsets_valid = True
    
        formsetclasses = {
            "articlelinks": inlineformset_factory(Article, ArticleLink, ArticleLinkForm, extra=3),
            "maintenancenotes": inlineformset_factory(Article, ArticleNote, ArticleNoteForm, extra=1)
        }

        formsets={}
        for formsetclass in formsetclasses:
            if self.request.POST:            
                formsets[formsetclass] = formsetclasses[formsetclass](self.request.POST, instance=self.object)
            else:
                formsets[formsetclass] = formsetclasses[formsetclass](instance=self.object)

            if formsets[formsetclass].is_valid():
                formsets[formsetclass].save()
            else:
                logger.critical(formsets[formsetclass].errors)
                formsets_valid = False


        if not formsets_valid:
            return self.form_invalid(form)

        return response


    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("libtekin256:article-detail", kwargs={"pk": self.object.pk})

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "libtekin256.change_article"
    model = Article
    form_class = ArticleForm

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        formsetclasses = {
            "articlelinks": inlineformset_factory(Article, ArticleLink, ArticleLinkForm, extra=1),
            "maintenancenotes": inlineformset_factory(Article, ArticleNote, ArticleNoteForm, extra=1)
        }

        for formsetclass in formsetclasses:

            if self.request.POST:            
                context_data[formsetclass] = formsetclasses[formsetclass](self.request.POST, instance=self.object)
            else:
                context_data[formsetclass] = formsetclasses[formsetclass](instance=self.object)


        return context_data

    def form_valid(self, form):
    
        response = super().form_valid(form)
        formsets_valid = True
    
        formsetclasses = {
            "articlelinks": inlineformset_factory(Article, ArticleLink, ArticleLinkForm, extra=1),
            "maintenancenotes": inlineformset_factory(Article, ArticleNote, ArticleNoteForm, extra=1)
        }

        formsets={}
        for formsetclass in formsetclasses:
            if self.request.POST:            
                formsets[formsetclass] = formsetclasses[formsetclass](self.request.POST, instance=self.object)
            else:
                formsets[formsetclass] = formsetclasses[formsetclass](instance=self.object)

            if formsets[formsetclass].is_valid():
                formsets[formsetclass].save()
            else:
                logger.critical(formsets[formsetclass].errors)
                formsets_valid = False


        if not formsets_valid:
            return self.form_invalid(form)

        return response

            
    def get_success_url(self):

        return reverse_lazy("libtekin256:article-detail", kwargs={"pk": self.object.pk})

class ArticleDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "libtekin256.view_article"
    model = Article

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["labels"] = {
            'article':get_pretty_labels(Article),
            'articlelink':get_pretty_labels(ArticleLink),
            'maintenancenote':get_pretty_labels(ArticleNote)
        }

      
        return context_data

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "libtekin256.delete_article"
    model = Article
    def get_success_url(self, *args, **kwargs):
        return reverse('libtekin256:article-list')

class ArticleListView(PermissionRequiredMixin, FilterView):

    permission_required = "libtekin256.view_article"
    filterset_class = ArticleFilter
    filterstore_urlname = "libtekin256:article-filterstore"
    template_name_suffix = "_list"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["labels"] = {'article':get_pretty_labels(Article)}

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()

        return context_data

class ArticleCopyView(PermissionRequiredMixin, DetailView):
    permission_required = "libtekin256.view_article"
    model = Article

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.pk = None
        self.object.common_name = self.object.common_name + "_copy"  
        try:
            self.object.inventory_index = self.object.inventory_index + "_copy"  
            setattr(self.object, self.object.mamodel.inventory_index_twin, self.object.inventory_index ) 
            self.object.save()
        except IntegrityError:
            self.object.inventory_index = f"{self.object.inventory_index}_{uuid.uuid1()}"
            setattr(self.object, self.object.mamodel.inventory_index_twin, self.object.inventory_index ) 
            self.object.save()

        return HttpResponseRedirect(reverse('libtekin256:article-update', kwargs={"pk":self.object.pk}))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["labels"] = {
            'article':get_pretty_labels(Article),
            'articlelink':get_pretty_labels(ArticleLink),
            'maintenancenote':get_pretty_labels(ArticleNote)
        }

        context_data["copybutton"] = True  

        return context_data


class ArticleNoteSubjectCreateView(PermissionRequiredMixin, CreateView):
    model = ArticleNoteSubject
    permission_required = "libtekin256.add_articlenotesubject"
    form_class=ArticleNoteSubjectForm

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("libtekin256:articlesubject-detail", kwargs={"pk": self.object.pk})

    
class MamodelCategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "libtekin256.add_mamodelcategory"
    model = MamodelCategory
    form_class = MamodelCategoryForm

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("libtekin256:mamodelcategory-update", kwargs={"pk": self.object.pk})


class MamodelCategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "libtekin256.change_mamodelcategory"
    model = MamodelCategory
    form_class = MamodelCategoryForm

    def get_success_url(self):
        return reverse_lazy("libtekin256:mamodelcategory-detail", kwargs={"pk": self.object.pk})

class MamodelCategoryDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "libtekin256.view_mamodelcategory"
    model = MamodelCategory

class MamodelCategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "libtekin256.delete_mamodelcategory"
    model = MamodelCategory

    def get_success_url(self):
        return reverse_lazy("libtekin256:mamodelcategory-list", kwargs={"pk": self.object.pk})

class MamodelCategoryListView(PermissionRequiredMixin, ListView):
    permission_required = "libtekin256.view_mamodelcategory"
    model = MamodelCategory


class MamodelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "libtekin.add_mamodel"
    model = Mamodel
    form_class = MamodelForm

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                    "to_field_value": "-",
                    "callback": "decorateIndexTwin",
                    "attrs":"data-inventory_index_twin=" + self.object.inventory_index_twin,
                },
            )
        return reverse_lazy("libtekin256:mamodel-detail", kwargs={"pk": self.object.pk})

class MamodelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "libtekin.change_mamodel"
    model = Mamodel
    form_class = MamodelForm

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("libtekin256:mamodel-detail", kwargs={"pk": self.object.pk})


class MamodelDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "libtekin256.view_mamodel"
    model = Mamodel

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["labels"] = {'mamodel':get_pretty_labels(Mamodel)}

        return context_data
    
class MamodelListView(PermissionRequiredMixin, ListView):
    permission_required = "libtekin256.view_mamodel"
    model = Mamodel

