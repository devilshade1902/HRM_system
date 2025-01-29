from django.shortcuts import render
from .models import Department,HRM_Users
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import UserForm
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin ,LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class DeptList(ListView):
    model = Department
    template_name = 'dept_list.html'
    context_object_name = 'depts'
    
    def get_queryset(self):
        return Department.objects.filter(status=True)
    
class DeptCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Department
    template_name = 'dept_create.html'
    fields = ['dept_name','description']
    success_url = reverse_lazy('dept_list')
    
    permission_required = 'HRM_app.can_add_department'
    
class DeptDetailView(UpdateView):
    model = Department
    template_name = 'dept_update.html'
    fields = ['dept_name','description']
    success_url = reverse_lazy('dept_list')
    
def soft_delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)

    # Check if employees are linked to the department
    # if department.employee_set.exists():
    #     messages.warning(
    #         request, 
    #         "This department has assigned employees. Please reassign them before deactivating."
    #     )
    #     return redirect('dept_list')

    # Perform soft delete by setting status to False (inactive)
    department.status = False
    department.save()

    messages.success(request, "Department successfully deactivated.")
    return redirect('dept_list')


@login_required
def assign_permission_to_user(request):
    # user1
    user = get_object_or_404(HRM_Users,Username = "dhruv")
    permission = Permission.objects.get(codename = 'can add department')
    user.user_permissions.add(permission)
    
    
def UserCreate(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['fname']  # or use 'fname'
            user.set_password(user_form.cleaned_data['password1'])  # Hash password
            user.save()
            return redirect('dept_list')
    
    else:
        user_form = UserForm()
    
    return render(request,'user_create.html',{'user_form':user_form})