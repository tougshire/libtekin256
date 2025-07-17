import django_filters
from django_filters_stoex.filterset import StoexFilterSet
from .models import (
    Article,
    Role,
    ArticleNoteSubject,
    ArticleStatus,
    Mamodel,
    MamodelCategory
)
from django.db import models
from django import forms
from django_filters_stoex.filters import ChainableOrderingFilter, CrossFieldSearchFilter
from touglates.widgets import ClearableTextInput, DropdownSelectMultiple

class ArticleFilter(StoexFilterSet):

    filterset_common_name = forms.CharField()

    combined_text_search = CrossFieldSearchFilter(
        label="Combined Text Search(Name, Model, Index, etc..)",
        field_name="common_name, inventory_index, mamodel__brand, mamodel__name, mamodel__number, assignee__fullformalname, assignee__friendlyname, customfield01, customfield02, customfield03, customfield04, customfield05, customfield06, customfield07, customfield08, customfield09, customfield10, customfield11, customfield12, customfield13, customfield14, customfield15, customfield16",
        lookup_expr="icontains",
        help_text="General Text in the Article Record",
    )
    common_name = django_filters.CharFilter(
        label="Common Name",
        field_name="common_name",
        lookup_expr="icontains",
        help_text="Common Name",
        widget=ClearableTextInput(),
    )

    mamodel__in = django_filters.ModelMultipleChoiceFilter(
        label="Model",
        field_name="mamodel",
        queryset=Mamodel.objects.all(),
        help_text="Model",
        widget=DropdownSelectMultiple(),
    )

    mamodel__category__in = django_filters.ModelMultipleChoiceFilter(
        label="Model Category",
        field_name="mamodel__category",
        queryset=MamodelCategory.objects.all(),
        help_text="Model",
        widget=DropdownSelectMultiple(),
    )

    role__in = django_filters.ModelMultipleChoiceFilter(
        label="Role",
        field_name="category",
        queryset=Role.objects.all(),
        help_text="Role",
        widget=DropdownSelectMultiple(),
    )

    status__in = django_filters.ModelMultipleChoiceFilter(
        label="Status",
        field_name="status",
        queryset=ArticleStatus.objects.all(),
        help_text="Model",
        widget=DropdownSelectMultiple(),
    )

    note__in = django_filters.ModelMultipleChoiceFilter(
        label="Note",
        field_name="articlenote__subject",
        queryset=ArticleNoteSubject.objects.all(),
        help_text="Note",
        widget=DropdownSelectMultiple(),
    )
    
    orderbyfields_available = [
        ("status", "Status"),
        ("mamodel", "Model"),
        ("inventorydate", "Iventory Date")
    ]
    orderbyfields = ChainableOrderingFilter(fields=orderbyfields_available)
    orderbyfields1 = ChainableOrderingFilter(fields=orderbyfields_available)
    orderbyfields2 = ChainableOrderingFilter(fields=orderbyfields_available)

    class Meta:
        model = Article
        fields = []


