from app.views import *
from app.services.user_service import *
from app.services.group_service import all_groups

@login_required
@permission_required('auth.view_user')
def user_list(request):
    users = users_all(exclude_superadmins=True)
    context = {'users': users}
    return render(request, 'user/user_list.html', context)

@login_required
@permission_required('auth.add_user')
def user_create(request):
    form = UserForm()
    form.fields['groups'].choices = [(g.pk, get_string(g.name, request)) for g in Group.objects.all().exclude(name='student')]

    if request.method == 'POST':
        form = UserForm(request.POST)
        form.fields['groups'].choices = [(g.pk, g.name) for g in Group.objects.all().exclude(name='student')]
        if form.is_valid():
            data = form.cleaned_data
            list_data = [data[value] for value in data]
            if create_or_update_user(None, *list_data):
                messages.success(request, get_string('successfully created user', request))
                return redirect(user_list)

            messages.warning(request, get_string('this username is taken. please type another username', request))

    context = {'form': form, 'title': 'user', 'title1': 'creating', 'header1': 'user', 'header2': 'creating'}
    return render(request, 'main/create.html', context)

@login_required
@permission_required('auth.change_user')
def user_update(request, pk):
    user = get_user_by_pk(pk)
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.fields['groups'].choices = [(g.pk, g.name) for g in Group.objects.all().exclude(name='student')]
        if form.is_valid():
            data = form.cleaned_data
            list_data = [data[value] for value in data]
            create_or_update_user(user, *list_data)
            messages.success(request, get_string('successfully updated user', request))
            return redirect(user_list)

    form = UserForm(initial={
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        # 'password': user.password,
        'groups': list(filter_groups_of_user(user).values_list('pk', flat=True)),
    })

    form.fields['groups'].choices = [(g.pk, get_string(g.name, request)) for g in Group.objects.all().exclude(name='student')]
    context = {'form': form, 'title': 'user', 'title1': 'changing', 'header1': 'user', 'header2': user.username}
    return render(request, 'main/edit.html', context)

@login_required
@permission_required('auth.delete_user')
def user_delete(request, pk):
    user = get_user_by_pk(pk)
    user.delete()
    messages.success(request, get_string('successfully deleted user', request))
    return redirect(user_list)