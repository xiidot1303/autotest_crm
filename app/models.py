from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date, datetime


STATUS_CHOICES = (
    [0, 'inactive'],
    [1, 'active'],
)

class Language(models.Model):
    user_ip = models.CharField(null=True, blank=False, max_length=32)
    LANG_CHOICES = [(0, 'uz'), (1, 'ru')]
    lang = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)

class Student(models.Model):
    name = models.CharField(null=True, blank=False, max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)
    age = models.IntegerField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True, max_length=32)
    registred_date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    status = models.IntegerField(null=True, blank=False, choices=STATUS_CHOICES, default=1)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    password = models.CharField(null=True, blank=True, max_length=255)
    
    def __str__(self) -> str:
        phone = self.phone or ''
        return self.name + ' ' + str(phone)

    def add_student_to_lessons(self):
        student = self
        lessons = Lesson.objects.filter(
            end_datetime=None, group__members__student__pk=student.pk
            ).exclude(journal__student__pk=student.pk)
        for lesson in lessons:
            lesson.journal.create(student=student)

    def save(self, *args, **kwargs):
        # add student to lesson if status = 1
        self.add_student_to_lessons()
        return super(Student, self).save(*args, **kwargs)

class Course(models.Model):
    title = models.CharField(null=True, blank=False, max_length=255)
    description = models.TextField(null=True, blank=True)
    lessons = models.IntegerField(null=True, blank=False)
    price = models.BigIntegerField(null=True, blank=False)
    def __str__(self) -> str:
        return self.title

    @property
    def one_lesson_price(self):
        return self.price // self.lessons

class Teacher(models.Model):
    name = models.CharField(null=True, blank=False, max_length=255)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    specialty = models.CharField(null=True, blank=True, max_length=255)
    phone = PhoneNumberField(null=True, blank=True, max_length=32)
    registred_date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    status = models.IntegerField(null=True, blank=False, choices=STATUS_CHOICES, default=1)

    def __str__(self) -> str:
        return self.name

class Group_member(models.Model):
    student = models.ForeignKey('app.Student', null=True, blank=False, on_delete=models.PROTECT)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    status = models.IntegerField(null=True, blank=False, choices=STATUS_CHOICES, default=1)
    payments = models.ManyToManyField('app.Payment')

    @property
    def payable_amount(self):
        payment = self.payments.filter(due_date__lte=date.today()).last()
        return payment.remaining_amount if payment else 0

class Group(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    members = models.ManyToManyField('app.Group_member', related_name='group_members')
    member = models.OneToOneField('app.Group_member', null=True, related_name='group', on_delete=models.PROTECT)
    teacher = models.ForeignKey('app.Teacher', null=True, blank=False, on_delete=models.PROTECT)
    course = models.ForeignKey('app.Course', null=True, blank=False, on_delete=models.PROTECT)
    weekdays = models.ManyToManyField('app.Weekday')
    remaining_lessons = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    status = models.IntegerField(null=True, blank=False, choices=STATUS_CHOICES, default=1)

    class Meta:
        permissions = [
            ("add_student_to_group", "Can add student to group"),
        ]

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = date.today()

        if not self.remaining_lessons:
            self.remaining_lessons = self.course.lessons
        return super(Group, self).save(*args, **kwargs)


class Lesson(models.Model):
    group = models.ForeignKey('app.Group', null=True, blank=False, related_name='lessons', on_delete=models.CASCADE)
    journal = models.ManyToManyField('app.Journal')
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("start_lesson", "Can start lesson"),
            ("end_lesson", "Can end lesson"),
        ]

class Journal(models.Model):
    student = models.ForeignKey('app.Student', null=True, blank=False, on_delete=models.PROTECT)
    attended = models.BooleanField(null=True, blank=True)
    feedback = models.CharField(null=True, blank=True, max_length=255, default = '')

    def __str__(self) -> str:
        return self.student.name + ' ' + str(self.attended)

class Payment(models.Model):
    amount = models.BigIntegerField(null=True, blank=False)
    incomes = models.ManyToManyField('app.Income')
    due_date = models.DateField(null=True, blank=True)
    payed = models.BooleanField(null=True, blank=False, default=False)
    payed_datetime = models.DateTimeField(null=True, blank=True)

    @property
    def remaining_amount(self):
        return self.amount - sum([i.amount for i in self.incomes.all().exclude(conf=None)])
    
    @property
    def payed_amount(self):
        return sum([i.amount for i in self.incomes.all().exclude(conf=None)])
    
    @property
    def waiting_incomes(self):
        return sum([i.amount for i in self.incomes.filter(conf=False)])

    @property
    def member(self):
        return Group_member.objects.get(payments__pk=self.pk)

    def save(self, *args, **kwargs):
        try:
            if self.remaining_amount <= 0:
                self.payed_datetime = datetime.now() if not self.payed else self.payed_datetime
                self.payed = True
            else:
                self.payed = False
        except:
            None
        
        return super(Payment, self).save(*args, **kwargs)

class Income(models.Model):
    TYPES = [
        ('cash', 'cash'),
        ('card', 'card'),
    ]
    amount = models.BigIntegerField(null=True, blank=False)
    datetime = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    type = models.CharField(null=True, blank=False, max_length=16, choices=TYPES)
    conf = models.BooleanField(null=True, blank=False, default=True) # confirmed
    cancelled = models.BooleanField(null=True, blank=True)
    
    @property
    def payment(self):
        return Payment.objects.get(incomes__pk=self.pk)

    @property
    def student(self):
        return Group_member.objects.get(payments__incomes__pk=self.pk).student

    @property
    def group(self):
        return Group_member.objects.get(payments__incomes__pk=self.pk).group



    def __str__(self) -> str:
        return str(self.amount)


class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='')
    username = models.CharField(null=True, blank=True, max_length=256)
    firstname = models.CharField(null=True, blank=True, max_length=256)
    phone = models.CharField(null=True, blank=True, max_length=16, default='')
    lang = models.CharField(null=True, blank=True, max_length=4)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()






# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
class WeekdayManager(models.Manager):
    def get_queryset(self):
        query = super().get_queryset()
        try:
            if not query.all():
                [query.create(day=i) for i in range(7)]
        except:
            None
        return query

class Weekday(models.Model):
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = models.IntegerField(null=True, blank=True)
    objects = WeekdayManager()
    
    def __str__(self) -> str:
        string = self.weekdays[self.day]
        return string

    def title(self):
        return self.weekdays[self.day]