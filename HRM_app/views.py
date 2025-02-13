from django.shortcuts import render
from .models import Department,HRM_Users
from django.views.generic.edit import CreateView
from django.views.generic import ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import UserForm,UserEditForm
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin ,LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class DeptList(ListView):
    model = Department
    template_name = 'dept_list.html'
    context_object_name = 'depts'
    
    def get_queryset(self):
        return Department.objects.all()
    
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

def is_admin(user):
    return user.is_superuser
    
@login_required
@user_passes_test(is_admin)
def UserCreate(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['role']  # Use role as username
            user.save()
            return redirect('user_list')
    else:
        user_form = UserForm()
    return render(request, 'user_create.html', {'user_form': user_form})



class UserList(ListView):
    model = HRM_Users
    template_name = 'user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return HRM_Users.objects.filter(is_superuser=False)
    
    
@login_required
def edit_user(request, pk):
    user = get_object_or_404(HRM_Users, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # This saves all fields, including role and description
            messages.success(request, "User updated successfully!")
            return redirect('user_list')  # Redirect to the user list
    else:
        form = UserEditForm(instance=user)

    return render(request, 'user_update.html', {'form': form})


@login_required
def deactivate_user(request, pk):
    user = get_object_or_404(HRM_Users, pk=pk)
    user.is_active = False  # Deactivate the user
    user.save()
    messages.success(request, "User deactivated successfully!")
    return redirect('user_list')


