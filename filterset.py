import django_filters
from django_filters_stoex.filterset import StoexFilterSet
from .models import (
    Article,
    ArticleStatus,
    Mamodel
)
from django.db import models
from django import forms
from django_filters_stoex.filters import ChainableOrderingFilter, CrossFieldSearchFilter
from touglates.widgets import DropdownSelectMultiple

class ArticleFilter(StoexFilterSet):

    filterset_common_name = forms.CharField()
    combined_text_search = CrossFieldSearchFilter(
        label="Combined Text Search(Name, Model, Index, etc..)",
        field_name="common_name, inventory_index, mamodel__brand, mamodel__name, mamodel__number, assignee__fullformalname, assignee__friendlyname, customfield01, customfield02, customfield03, customfield04, customfield05, customfield06, customfield07, customfield08, customfield09, customfield10, customfield11, customfield12, customfield13, customfield14, customfield15, customfield16",
        lookup_expr="icontains",
        help_text="General Text in the Article Record",
    )
    common_name = django_filters.CharFilter(
        label="Combined Text Search(Name, Model, Index, etc..)",
        field_name="common_name, inventory_index, mamodel__brand, mamodel__name, mamodel__number, assignee__fullformalname, assignee__friendlyname, customfield01, customfield02, customfield03, customfield04, customfield05, customfield06, customfield07, customfield08, customfield09, customfield10, customfield11, customfield12, customfield13, customfield14, customfield15, customfield16",
        lookup_expr="icontains",
        help_text="General Text in the Article Record",
    )

    mamodel__in = django_filters.ModelMultipleChoiceFilter(
        label="Model",
        field_name="mamodel",
        queryset=Mamodel.objects.all(),
        help_text="Model",
        widget=DropdownSelectMultiple(),
    )

    status__in = django_filters.ModelMultipleChoiceFilter(
        label="Status",
        field_name="status",
        queryset=ArticleStatus.objects.all(),
        help_text="Model",
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


