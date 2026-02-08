from app.views import *
from app.services.payment_service import *
from app.services.group_service import all_groups

@login_required
@group_required('director')
def finance_incomes(request):
    incomes = filter_confirmed_incomes()
    from_ = ''
    to = ''
    if 'filter' in request.GET:
        from_ = request.GET['from']
        to = request.GET['to'] 
        incomes = filter_incomes_by_date(incomes, from_, to)
    overall_amount = sum(incomes.values_list('amount', flat=True))
    context = {'incomes': incomes, 'overall_amount': overall_amount, 'from': from_, 'to': to}
    return render(request, 'finance/finance_incomes.html', context)    

@login_required
@group_required('director')
def finance_debtors(request):
    group_pk = request.GET['group'] if 'group' in request.GET else None
    group_pk = int(group_pk) if group_pk else group_pk
    payments = filter_debtors(group_pk)
    groups = all_groups()
    context = {'payments': payments, 'groups': groups, 'group_pk': group_pk}
    return render(request, 'finance/finance_debtors.html', context)