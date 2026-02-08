from app.views import *
from app.services.payment_service import *
from app.services.student_service import *
from app.services.group_service import *

@login_required
@permission_required('app.view_payment')
@check_student_is_user()
def payment_list_by_student(request, student_pk, group_pk=None):
    student = get_student_by_pk(student_pk)
    payments = filter_payments_by_student(student, decreasing=True, group_pk=group_pk)
    group = get_group_by_pk(group_pk) if group_pk else None
    context = {'student': student, 'payments': payments, 'group': group, 'group_pk': group_pk}
    return render(request, 'payment/payment_list_by_student.html', context)

@login_required
@permission_required('app.add_income')
def payment_pay(request):
    if 'amount' in request.POST:
        amount = request.POST['amount']
        type = request.POST['type'] if request.POST['type'] in ['cash', 'card'] else 'cash'
        payment_pk = request.POST['payment']
        student_pk = request.POST['student']
        group_pk = request.POST['group']
    else:
        return redirect('main_menu')
    payment = get_payment_by_pk(payment_pk)
    income_create(payment, amount, type)
    return redirect_back(request)
    # if group_pk:
    #     return redirect(payment_list_by_student, student_pk=student_pk, group_pk=group_pk)
    # else:
    #     return redirect(payment_list_by_student, student_pk=student_pk)



@login_required
@permission_required('app.delete_income')
def payment_cancel(request, pk):
    income = get_income_by_pk(pk)
    if income_cancel(income):
        messages.success(request, get_string('payment is cancelled', request))
    return redirect(request.META.get('HTTP_REFERER'))