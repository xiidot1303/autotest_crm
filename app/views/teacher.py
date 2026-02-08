from app.views import *
from app.services.teacher_service import *

@permission_required('app.view_teacher')
@login_required
def teacher_list_all(request):
    teachers = all_teachers()
    context = {'teachers': teachers}
    return render(request, 'teacher/teacher_list_all.html', context)

class TeacherEditView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'app.change_teacher'
    form_class = TeacherForm
    model = Teacher
    template_name = 'main/edit.html'
    # success_url = reverse_lazy('teacher_list_all')
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        teacher = context['object']
        context['title'] = 'teacher | changing'
        context['header1'] = 'teacher'
        context['header2'] = teacher.name
        return context
    
    def get_success_url(self) -> str:
        messages.add_message(self.request, messages.SUCCESS, text_successfully_changed(self.request))
        return reverse_lazy('teacher_list_all')

class TeacherCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = ['app.add_teacher']
    form_class = TeacherForm
    model = Teacher
    template_name = 'main/create.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'teacher | creating'
        context['header1'] = 'teacher'
        context['header2'] = 'creating'
        return context

    def get_success_url(self) -> str:
        messages.add_message(self.request, messages.SUCCESS, text_successfully_created(self.request))
        return reverse_lazy('teacher_list_all')

@permission_required('app.delete_teacher')
@login_required
def teacher_delete(request, pk):
    teacher = get_teacher_by_pk(pk)
    try:
        teacher.delete()
        messages.success(request, text_successfully_deleted(request))
    except:
        teacher.status = 0
        teacher.save()
        messages.success(request, text_successfully_deleted(request))
        # messages.warning(request, text_can_not_delete_sth(request, sth='teacher', bcoz='group'))
    
    return redirect(teacher_list_all)