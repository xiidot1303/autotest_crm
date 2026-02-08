from app.services import *
from django.contrib.auth.models import User, Group
from django.db import IntegrityError

def is_user_in_group(request, *groups):
    return request.user.groups.filter(name__in=groups).exists() or request.user.is_superuser

def is_superuser(request):
    return request.user.is_superuser

def users_all(exclude_superadmins=False):
    users = User.objects.all()
    if exclude_superadmins:
        users = users.exclude(is_superuser=True)
    return users

def get_user_by_pk(pk):
    return get_object_or_404(User, pk=pk)

def filter_groups_of_user(user):
    return user.groups.all()

def create_or_update_user(user, username, first_name, last_name, groups_id, email, password):
    if not user:
        # create
        user = User.objects.create()

    user.username=username
    user.first_name=first_name
    user.last_name=last_name
    user.email=email

    # set password if available
    if password:
        user.set_password(password)
    try:
        user.save()
    except:
        user.delete()
        return None

    # remove available groups
    for group in filter_groups_of_user(user):
        user.groups.remove(group)

    # add groups
    [
        user.groups.add(
            Group.objects.get(pk=group_id)
        )
        for group_id in groups_id

    ]
    return user