from app.views import *
from app.services.payment_service import (
    filter_unconfirmed_incomes,
    get_income_by_pk, 
    income_confirm,
    income_reject
)

@login_required
@group_required('accounter')
def accounter_page(request):
    incomes = filter_unconfirmed_incomes()
    start_datetime = incomes.first().datetime if incomes else None
    end_datetime = incomes.last().datetime if incomes else None
    overall_amount = sum(incomes.values_list('amount', flat=True))
    context = {
        'incomes': incomes, 'start_datetime': start_datetime, 
        'end_datetime': end_datetime, 'overall_amount': overall_amount
    }
    return render(request, 'accounter/accounter_page.html', context)

@login_required
@group_required('accounter')
def accounter_confirm_income(request, pk):
    income = get_income_by_pk(pk)
    income_confirm(income)
    messages.success(request, get_string('confirmed', request))
    return redirect_back(request)

@login_required
@group_required('accounter')
def accounter_confirm_incomes_all(request):
    incomes = filter_unconfirmed_incomes()
    [
        income_confirm(income)
        for income in incomes
    ]
    messages.success(request, get_string('confirmed', request))
    return redirect_back(request)


@login_required
@group_required('accounter')
def accounter_reject_income(request, pk):
    income = get_income_by_pk(pk)
    income_reject(income)
    messages.success(request, get_string('rejected', request))
    return redirect_back(request)