from app.views import *
from app.services.course_service import *

@login_required
@permission_required('app.view_course')
def course_list_all(request):
    courses = all_courses()
    context = {'courses': courses}
    return render(request, 'course/course_list_all.html', context)

class CourseCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'app.add_course'
    model = Course
    form_class = CourseForm
    template_name = 'main/create.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'course | creating'
        context['header1'] = 'course'
        context['header2'] = 'creating'
        return context
    
    def get_success_url(self) -> str:
        messages.success(self.request, text_successfully_created(self.request))
        return reverse_lazy('course_list_all')

class CourseEditView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'app.change_course'
    model = Course
    form_class = CourseForm
    template_name = 'main/edit.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = context['object']
        context['title'] = 'course | changing'
        context['header1'] = 'course'
        context['header2'] = obj.title
        return context
    
    def get_success_url(self) -> str:
        messages.success(self.request, text_successfully_changed(self.request))
        return reverse_lazy('course_list_all')

@permission_required('app.delete_course')
@login_required
def course_delete(request, pk):
    course = get_course_by_pk(pk)
    try:
        course.delete()
        messages.success(request, text_successfully_deleted(request))
    except:
        messages.warning(request, text_can_not_delete_sth(request, sth='course', bcoz='group'))

    return redirect(course_list_all)