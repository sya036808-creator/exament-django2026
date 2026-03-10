from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Project, Task
from .forms import TaskForm
from django.db.models import Count, Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@login_required
def dashboard(request):
    user = request.user
    status_filter = request.GET.get('status')
    user_filter = request.GET.get('user')
    search_query = request.GET.get('q')
    
    # Base querysets
    projects = Project.objects.filter(Q(creator=user) | Q(members=user)).distinct()
    all_visible_tasks = Task.objects.filter(project__in=projects)
    
    # Apply filters
    tasks_to_display = all_visible_tasks
    if status_filter:
        tasks_to_display = tasks_to_display.filter(status=status_filter)
    if user_filter:
        tasks_to_display = tasks_to_display.filter(assigned_to_id=user_filter)
    if search_query:
        tasks_to_display = tasks_to_display.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
        
    # Stats for the logged in user's assigned tasks
    user_tasks = Task.objects.filter(assigned_to=user)
    total_tasks = user_tasks.count()
    todo_tasks = user_tasks.filter(status='TODO').count()
    in_progress_tasks = user_tasks.filter(status='IN_PROGRESS').count()
    done_tasks = user_tasks.filter(status='DONE').count()
    
    # Recent tasks (from filtered list or all visible)
    recent_tasks = tasks_to_display.order_by('-updated_at')[:8]
    
    # Get all potential members for the user filter
    team_members = list(CustomUser.objects.filter(projects__in=projects).distinct())
    
    selected_status = request.GET.get('status', '')
    selected_user = request.GET.get('user', '')
    
    status_choices = [
        {'value': '', 'label': 'Tous les statuts', 'selected': selected_status == ''},
        {'value': 'TODO', 'label': 'À Faire', 'selected': selected_status == 'TODO'},
        {'value': 'IN_PROGRESS', 'label': 'En Cours', 'selected': selected_status == 'IN_PROGRESS'},
        {'value': 'DONE', 'label': 'Terminé', 'selected': selected_status == 'DONE'},
    ]
    
    for member in team_members:
        member.is_selected = str(member.id) == selected_user
    
    context = {
        'projects': projects,
        'tasks': tasks_to_display,
        'team_members': team_members,
        'status_choices': status_choices,
        'total_tasks': total_tasks,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'tasks/dashboard.html', context)

# --- Gestion des Projets ---

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        # On ne récupère que les projets où l'utilisateur est créateur ou membre
        return Project.objects.filter(Q(creator=self.request.user) | Q(members=self.request.user)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for project in context['projects']:
            project.is_creator = (project.creator == user)
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_creator'] = self.object.creator == user
        
        tasks_list = self.object.tasks.all()
        now = timezone.now()
        for t in tasks_list:
            t.can_edit = (self.object.creator == user) or (t.assigned_to == user)
            t.is_overdue = (t.deadline < now and t.status != 'DONE')
            if t.status == 'TODO':
                t.status_css = 'badge-todo'
            elif t.status == 'IN_PROGRESS':
                t.status_css = 'badge-in-progress'
            else:
                t.status_css = 'badge-done'
                
        context['tasks'] = tasks_list
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'tasks/project_form.html'
    fields = ['name', 'description', 'members']
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'tasks/project_form.html'
    fields = ['name', 'description', 'members']

    def test_func(self):
        # Seul le créateur peut modifier
        return self.get_object().creator == self.request.user

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'tasks/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.get_object().creator == self.request.user

# --- Gestion des Tâches ---

class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_pk'] = self.kwargs.get('project_pk')
        return context

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return project.creator == self.request.user

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        
        # Un étudiant ne peut pas assigner un prof (règle métier)
        assigned_user = form.cleaned_data.get('assigned_to')
        if self.request.user.role == 'STUDENT' and assigned_user and assigned_user.role == 'PROFESSOR':
            form.add_error('assigned_to', "Un étudiant ne peut pas assigner un professeur à une tâche.")
            return self.form_invalid(form)
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs['project_pk']})

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        task = self.get_object()
        # Si c'est pas le créateur, on ne peut changer que le statut
        if task.project.creator != self.request.user:
            for field_name in list(form.fields.keys()):
                if field_name != 'status':
                    del form.fields[field_name]
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_pk'] = self.object.project.pk
        return context

    def test_func(self):
        task = self.get_object()
        # Allow access if the user is the creator, the assigned user, OR a member of the project
        return (task.project.creator == self.request.user or 
                task.assigned_to == self.request.user or 
                self.request.user in task.project.members.all())

    def form_valid(self, form):
        if 'assigned_to' in form.cleaned_data:
            assigned_user = form.cleaned_data.get('assigned_to')
            if self.request.user.role == 'STUDENT' and assigned_user and assigned_user.role == 'PROFESSOR':
                form.add_error('assigned_to', "Un étudiant ne peut pas assigner un professeur à une tâche.")
                return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    def test_func(self):
        return self.get_object().project.creator == self.request.user

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})

# --- Statistiques et calcul des Primes ---

@login_required
def statistics_view(request):
    user = request.user
    now = timezone.now()
    year = now.year
    
    # On regarde les tâches de l'année en cours
    annual_tasks = Task.objects.filter(assigned_to=user, deadline__year=year)
    total_annual = annual_tasks.count()
    completed_annual = annual_tasks.filter(status='DONE').count()
    
    # Calcul du taux de réussite dans les délais
    completed_in_time_annual = 0
    for task in annual_tasks.filter(status='DONE'):
        if task.updated_at <= task.deadline:
            completed_in_time_annual += 1
            
    annual_rate = (completed_in_time_annual / total_annual * 100) if total_annual > 0 else 0
    
    # Statistiques du trimestre
    quarter = (now.month - 1) // 3 + 1
    quarter_tasks = Task.objects.filter(
        assigned_to=user, 
        deadline__year=year,
        deadline__month__gte=(quarter-1)*3 + 1,
        deadline__month__lte=quarter*3
    )
    total_quarter = quarter_tasks.count()
    completed_in_time_quarter = 0
    for task in quarter_tasks.filter(status='DONE'):
        if task.updated_at <= task.deadline:
            completed_in_time_quarter += 1
            
    quarter_rate = (completed_in_time_quarter / total_quarter * 100) if total_quarter > 0 else 0
    
    # Calcul de la prime (seulement pour les profs)
    prime = 0
    prime_status = ""
    if user.role == 'PROFESSOR':
        if annual_rate == 100:
            prime = 100000
            prime_status = "Bravo ! Prime de 100 000 CFA validée (100% de réussite)."
        elif annual_rate >= 90:
            prime = 30000
            prime_status = "Prime de 30 000 CFA validée (plus de 90% de réussite)."
        else:
            prime_status = "Objectif non atteint pour la prime (moins de 90%)."
    else:
        prime_status = "Section réservée aux enseignants pour les primes."

    context = {
        'total_annual': total_annual,
        'completed_in_time_annual': completed_in_time_annual,
        'annual_rate': round(annual_rate, 2),
        'total_quarter': total_quarter,
        'completed_in_time_quarter': completed_in_time_quarter,
        'quarter_rate': round(quarter_rate, 2),
        'prime': prime,
        'prime_status': prime_status,
        'current_year': year,
        'current_quarter': quarter,
    }
    
    return render(request, 'tasks/statistics.html', context)
