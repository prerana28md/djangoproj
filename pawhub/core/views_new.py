from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Pet, Listing, HealthRecord, MarketplaceItem, AdoptionRequest, Cart, CartItem, Order, OrderItem
from lost_found.models import LostFound
from .forms import PetForm, ListingForm, HealthRecordForm, MarketplaceItemForm, AdoptionRequestForm, AdoptionRequestResponseForm, CartItemForm, OrderForm, MarketplaceSearchForm
from lost_found.forms import LostPetForm, FoundPetForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from users.forms import UserRegistrationForm
from django.http import JsonResponse
from django.db.models.deletion import ProtectedError
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField

# ... existing code ... 