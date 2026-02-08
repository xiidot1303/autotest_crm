from app.views import *
from app.services.group_service import *
from app.services.student_service import *
from app.services.payment_service import *
from app.services.course_service import *
from app.services.user_service import is_user_in_group

@permission_required('app.view_group')
@group_forbid('student')
@login_required
def group_list_all(request):
    groups = all_groups()
    context = {'groups': groups}

    return render(request, 'group/group_list_all.html', context)

@login_required
@permission_required('app.view_group')
def group_page(request, pk, month=today().month, year=today().year):
    group = get_group_by_pk(pk)
    # filter students who are not in this group 
    students = filter_students_who_are_not_in_group(group)

    if request.method == 'POST':
        form = Adding_student_to_groupForm(request.POST)
        form.fields['student'].choices = [(s.pk, s.name) for s in students]
        form.fields['payment_method'].choices = [
            ('full', get_string('full', request)),
            ('monthly', get_string('monthly', request)),
        ]

        if form.is_valid():
            student_pk = form.cleaned_data['student']
            payment_method = form.cleaned_data['payment_method']
            discount = form.cleaned_data['discount']
            
            student = get_student_by_pk(student_pk)
            add_student_to_group(group, student, payment_method, discount)
            messages.success(request, get_string(
                '{student} is added to group {group}', request
                ).format(student=student.name, group=group.title))
    
    # updated students list
    students = filter_students_who_are_not_in_group(group)

    # attendance
    current_month_text = month_by_index(month, request)
    # lessons = filter_lessons_monthly(group, month, year)
    lessons = filter_lessons_by_group(group)
    dates = get_distinct_dates_of_lessons(group)

    # new form
    form = Adding_student_to_groupForm()
    form.fields['student'].choices = [(s.pk, s.name) for s in students]
    form.fields['payment_method'].choices = [
        ('full', get_string('full', request)),
        ('monthly', get_string('monthly', request)),
    ]
    context = {'group': group, 'form': form, 'lessons': lessons, 'dates': dates}
    return render(request, 'group/group_page.html', context)

@login_required
@permission_required('app.add_payment', 'app.view_group')
def group_pay(request):
    amount = request.POST['amount']
    type = request.POST['type'] if request.POST['type'] in ['cash', 'card'] else 'cash'
    member_pk = request.POST['member']
    member = get_group_member_by_pk(member_pk)
    group = request.POST['group']

    pay_next_payment_of_member(member, int(amount), type)
    return redirect(group_page, pk=int(group))

@login_required
@permission_required('app.change_group')
def group_remove_student(request, group_pk, member_pk):
    delete_group_member(member_pk=member_pk)
    return redirect(group_page, pk=group_pk)

class GroupCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'app.add_group'
    model = Group
    form_class = GroupForm
    template_name = 'main/create.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'group'
        context['title'] = 'creating'
        context['header1'] = 'group'
        context['header2'] = 'creating'
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        obj = form.instance
        if check_teacher_has_lesson(data, obj):
            messages.warning(self.request, get_string('teacher has lesson in this time', self.request))
            return self.render_to_response(self.get_context_data(form=form))
        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        # create lesson if start date is today
        obj = self.object
        if obj.start_date == today():
            weekday = datetime_now().weekday()
            if obj.weekdays.filter(day=weekday):
                if obj.start_time > time_now():
                    create_lesson(group=obj)
                elif obj.start_time < time_now() < obj.end_time:
                    lesson = create_lesson(group=obj)
                    start_lesson(lesson)
                    
        messages.success(self.request, text_successfully_created(self.request))
        return reverse_lazy('group_list_all')

class GroupEditView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'app.change_group'
    model = Group
    form_class = GroupForm
    template_name = 'main/edit.html'
    
    def get_form(self, form_class=GroupForm):
        form = super().get_form(form_class)
        obj = form.instance
        
        if check_group_has_lesson(obj):
            form.fields['start_date'].widget.input_type = 'hidden'
            form.fields['start_date'].label = ''
        
        return form

    def form_valid(self, form):
        data = form.cleaned_data
        obj = form.instance
        if check_teacher_has_lesson(data, obj):
            messages.warning(self.request, get_string('teacher has lesson in this time', self.request))
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = context['object']
        context['title'] = 'group'
        context['title1'] = 'changing'
        context['header1'] = 'group'
        context['header2'] = ''
        return context
    
    def get_success_url(self) -> str:
        messages.success(self.request, text_successfully_changed(self.request))
        return reverse_lazy('group_list_all')


@permission_required('app.delete_group')
@login_required
def group_delete(request, pk):
    group = get_group_by_pk(pk)
    try:
        group.delete()
        messages.success(request, text_successfully_deleted(request))
    except:
        w = 0

    return redirect(group_list_all)


@login_required
@permission_required('app.add_student_to_group')
def group_set_student_to_new_group(request: HttpRequest):
    if request.method == 'POST':
        students = filter_students_active()
        teachers = all_teachers()
        courses = all_courses()
        form = Setting_student_to_groupForm(request.POST)
        form.fields['student'].choices = [(s.pk, s.name) for s in students]
        form.fields['teacher'].choices = [(t.pk, t.name) for t in teachers]
        form.fields['course'].choices = [(c.pk, c.title) for c in courses]
        if form.is_valid():
            student_pk = form.cleaned_data['student']
            teacher_pk = form.cleaned_data['teacher']
            course_pk = form.cleaned_data['course']
            discount = form.cleaned_data['discount']

            student = get_student_by_pk(student_pk)
            teacher = get_teacher_by_pk(teacher_pk)
            course = get_course_by_pk(course_pk)
            group = create_group(
                title=student.name,
                course=course,
                teacher=teacher,

            )
            set_student_to_group(group, student, discount)
            create_lessons(group)
            messages.success(request, get_string(
                '{student} is added to lessons', request
            ).format(student=student.name))

    return redirect_back(request)