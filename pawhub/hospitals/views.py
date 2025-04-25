from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Hospital, Doctor
from .forms import HospitalForm, DoctorForm

# Create your views here.

class HospitalListView(ListView):
    model = Hospital
    template_name = 'hospitals/hospital_list.html'
    context_object_name = 'hospitals'

class HospitalDetailView(DetailView):
    model = Hospital
    template_name = 'hospitals/hospital_detail.html'
    context_object_name = 'hospital'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = self.object.doctors.all()
        return context

class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    template_name = 'hospitals/hospital_form.html'
    form_class = HospitalForm
    success_url = reverse_lazy('hospitals:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Hospital'
        return context

class HospitalUpdateView(LoginRequiredMixin, UpdateView):
    model = Hospital
    template_name = 'hospitals/hospital_form.html'
    form_class = HospitalForm
    success_url = reverse_lazy('hospitals:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Hospital'
        return context

class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = Hospital
    template_name = 'hospitals/hospital_confirm_delete.html'
    success_url = reverse_lazy('hospitals:list')

@login_required
def doctor_create(request, hospital_pk):
    hospital = get_object_or_404(Hospital, pk=hospital_pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.hospital = hospital
            doctor.save()
            messages.success(request, 'Doctor added successfully!')
            return redirect('hospitals:detail', pk=hospital.pk)
    else:
        form = DoctorForm()
    return render(request, 'hospitals/doctor_form.html', {
        'form': form,
        'hospital': hospital,
        'title': 'Add New Doctor'
    })

@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor information updated successfully!')
            return redirect('hospitals:detail', pk=doctor.hospital.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospitals/doctor_form.html', {
        'form': form,
        'hospital': doctor.hospital,
        'title': 'Edit Doctor Information'
    })

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    hospital_pk = doctor.hospital.pk
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor removed successfully!')
        return redirect('hospitals:detail', pk=hospital_pk)
    return render(request, 'hospitals/doctor_confirm_delete.html', {'doctor': doctor})
