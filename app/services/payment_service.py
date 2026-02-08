from app.services import *
from app.models import Payment, Group_member, Group, Income
from django.db.models import Exists, OuterRef

def get_payment_by_pk(pk):
    obj = get_object_or_404(Payment, pk=pk)
    return obj

def calculate_monthly_payment(group, student, start_date, discount):
    lessons = group.course.lessons
    stop = False
    while not stop:
        days = days_of_month_by_weekday(
            start_date, 
            get_date_last_day_of_month(start_date),
            list(group.weekdays.all().values_list(flat=True))
            )
        member = group.members.get(student=student)
        if lessons - len(days) <= 0:
            # end payment
            payment_days = lessons
            stop = True
        else:
            lessons -= len(days)
            payment_days = len(days)

        # create payments
        amount = make_discount(
            group.course.one_lesson_price * payment_days,
            discount
        )

        create_payment_of_member(member, amount, start_date)

        # set start date to 1st day of next month
        start_date = get_date_next_month_1st_day(start_date)

def calculate_full_payment(group: Group, student, start_date, discount):
    member = group.member
    price = make_discount(group.course.price, discount)
    create_payment_of_member(member, price, start_date)

def create_payment_of_member(member, amount, due_date):
    if amount:
        member.payments.create(
            amount=amount,
            due_date=due_date
        )

def get_first_payable_payment_of_member(member):
    payment = member.payments.filter(payed=False).first()
    return payment

def get_payable_remaining_amount_of_member(member):
    payment = get_first_payable_payment_of_member(member)
    return payment.remaining_amount if payment else 0

def get_payable_due_date_of_member(member):
    payment = get_first_payable_payment_of_member(member)
    return payment.due_date if payment else today()

def pay_next_payment_of_member(member, amount, type):
    while True:
        payment = get_first_payable_payment_of_member(member)
        if amount <= payment.remaining_amount:
            income_create(payment, amount, type)
            break
        else:
            amount -= payment.remaining_amount
            income_create(payment, payment.remaining_amount, type)

def filter_payments_by_group(group_pk, payments=Payment.objects):
    query = payments.filter(
        Exists(
            Group_member.objects.filter(
                Exists(Group.objects.filter(pk=group_pk).filter(members__pk=OuterRef('pk')))
            ).filter(
                payments__pk=OuterRef('pk')
                )
        )
    )
    return query

def filter_payments_by_student(student, decreasing=False, group_pk=None):
    
    payments = Payment.objects.filter(
        Exists(Group_member.objects.filter(student = student).filter(payments__pk=OuterRef('pk')))
    )
    
    # filter payments which are to next month
    to_date = get_date_next_month_1st_day(today())
    payments = payments.filter(
        due_date__range = ["1000-10-10", to_date.strftime("%Y-%m-%d")],
    )
    if group_pk:
        payments = filter_payments_by_group(group_pk, payments)

    return payments.order_by('-due_date') if decreasing else payments

def filter_debtors(group_pk=None):
    if group_pk:
        payments = filter_payments_by_group(group_pk)
    else:
        payments = Payment.objects.all()
    
    payments = payments.filter(
        payed = False,
        due_date__lte = today()
    )
    return payments

def delete_empty_payments_of_member(member):
    for payment in member.payments.all():
        if not payment.payed:
            if payment.incomes.all():
                payment.amount = payment.payed_amount
                payment.save()
            else:
                payment.delete()


# INCOME

def income_create(payment, amount, type):
    payment.incomes.create(amount=amount, type=type)
    payment.save()

def income_cancel(income):
    if not income.cancelled and income.amount > 0:
        income_create(
            income.payment,
            0-income.amount,
            income.type
        )
        income.cancelled = True
        income.save()
        return True
    return False

def income_confirm(income):
    income.conf = True
    income.save()

def income_reject(income):
    income.conf = None
    income.save()

def get_income_by_pk(pk):
    income = get_object_or_404(Income, pk=pk)
    return income

def filter_unconfirmed_incomes():
    incomes = Income.objects.filter(conf=False, amount__gte=0).exclude(cancelled=True)
    return incomes

def filter_confirmed_incomes():
    incomes = Income.objects.filter(conf=True, amount__gte=0).exclude(cancelled=True)
    return incomes

def filter_incomes_by_date(incomes, from_, to):
    try:
        if from_ and to:
            result = incomes.filter(datetime__range=(from_, to))
        elif from_:
            result = incomes.filter(datetime__gte=from_)
        elif to:
            result = incomes.filter(datetime__lte=to)
        else:
            result = incomes

        return result
    except:
        return incomes
