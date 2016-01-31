##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    GENDER_CHOICES = (
        ('F',_('Female')),
        ('M',_('Male')),
        ('U',_('Unknown')))

    external_id = models.CharField(max_length = 100,blank = True, null = True)
    user        = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    global_id   = models.CharField(max_length = 10,blank = True, null = True)
    gender      = models.CharField(max_length = 1, blank = True, null = True, choices = GENDER_CHOICES, default = 'U')
    national_id = models.CharField(max_length = 25,blank = True, null = True)
    first_name  = models.CharField(max_length = 50,blank = True, null = True)
    middle_name = models.CharField(max_length = 50,blank = True, null = True)
    last_name   = models.CharField(max_length = 50,blank = True, null = True)

    def username(self):
        if self.user is None :
            return None
        return self.user.username

    def find_person(person_id):
        return Person.objects.get(id=person_id)

    def __str__(self):
        first_name = ""
        middle_name = ""
        last_name = ""
        if self.first_name :
            first_name = self.first_name
        if self.middle_name :
            middle_name = self.middle_name
        if self.last_name :
            last_name = self.last_name + ","

        return u"%s %s %s" % (last_name.upper(), first_name, middle_name)


class Tutor(models.Model):
    external_id = models.CharField(max_length = 100, blank = True, null = True)
    person      = models.ForeignKey(Person)

    def find_by_user(user):
        try:
            person = Person.objects.filter(user=user)
            tutor = Tutor.objects.get(person = person)
            return tutor
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return u"%s" % self.person


class Student(models.Model):
    external_id     = models.CharField(max_length = 100,blank = True, null = True)
    registration_id = models.CharField(max_length=10)
    person          = models.ForeignKey(Person)

    def __str__(self):
        return u"%s (%s)" % (self.person, self.registration_id)


class Organization(models.Model):
    external_id = models.CharField(max_length = 100, blank = True, null = True)
    name        = models.CharField(max_length = 255)
    acronym     = models.CharField(max_length = 15)

    def __str__(self):
        return self.name


class Structure(models.Model):
    external_id  = models.CharField(max_length = 100, blank = True, null = True)
    acronym      = models.CharField(max_length = 15)
    title        = models.CharField(max_length = 255)
    organization = models.ForeignKey(Organization, null = True)
    part_of      = models.ForeignKey('self', null = True, blank = True)

    def __str__(self):
        return u"%s - %s" % (self.acronym, self.title)


class ProgrammeManager(models.Model):
    person  = models.ForeignKey(Person)
    faculty = models.ForeignKey(Structure)

    def find_faculty_by_user(user):
        programme_manager = ProgrammeManager.objects.filter(person__user=user).first()
        if programme_manager:
            return programme_manager.faculty
        else:
            return None

    def __str__(self):
        return u"%s - %s" % (self.person, self.faculty)


class AcademicYear(models.Model):
    external_id = models.CharField(max_length = 100,blank = True, null = True)
    year        = models.IntegerField()

    def __str__(self):
        return u"%s-%s" % (self.year, self.year + 1)

    def find_academic_year(id):
        return AcademicYear.objects.get(pk=id)


EVENT_TYPE = (
    ('ACADEMIC_YEAR', 'Academic Year'),
    ('DISSERTATIONS_SUBMISSION_SESS_1', 'Submission of academic dissertations - exam session 1'),
    ('DISSERTATIONS_SUBMISSION_SESS_2', 'Submission of academic dissertations - exam session 2'),
    ('DISSERTATIONS_SUBMISSION_SESS_3', 'Submission of academic dissertations - exam session 3'),
    ('EXAM_SCORES_SUBMISSION_SESS_1', 'Submission of exam scores - exam session 1'),
    ('EXAM_SCORES_SUBMISSION_SESS_2', 'Submission of exam scores - exam session 2'),
    ('EXAM_SCORES_SUBMISSION_SESS_3', 'Submission of exam scores - exam session 3'),
    ('DELIBERATIONS_SESS_1', 'Deliberations - exam session 1'),
    ('DELIBERATIONS_SESS_2', 'Deliberations - exam session 2'),
    ('DELIBERATIONS_SESS_3', 'Deliberations - exam session 3'),
    ('EXAM_SCORES_DIFFUSION_SESS_1', 'Diffusion of exam scores - exam session 1'),
    ('EXAM_SCORES_DIFFUSION_SESS_2', 'Diffusion of exam scores - exam session 2'),
    ('EXAM_SCORES_DIFFUSION_SESS_3', 'Diffusion of exam scores - exam session 3'),
    ('EXAM_ENROLLMENTS_SESS_1', 'Exam enrollments - exam session 1'),
    ('EXAM_ENROLLMENTS_SESS_2', 'Exam enrollments - exam session 2'),
    ('EXAM_ENROLLMENTS_SESS_3', 'Exam enrollments - exam session 3'))


class AcademicCalendar(models.Model):
    external_id   = models.CharField(max_length = 100,blank = True, null = True)
    academic_year = models.ForeignKey(AcademicYear)
    event_type    = models.CharField(max_length = 50, choices = EVENT_TYPE)
    title         = models.CharField(max_length = 50, blank = True, null = True)
    description   = models.TextField(blank = True, null = True)
    start_date    = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    end_date      = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)

    def current_academic_year():
        academic_calendar = AcademicCalendar.objects.filter(event_type='ACADEMIC_YEAR').filter(start_date__lte=timezone.now()).filter(end_date__gte=timezone.now()).first()
        if academic_calendar:
            return academic_calendar.academic_year
        else:
            return None

    def find_academic_calendar_by_event_type(academic_year_id, session_number):
        event_type_criteria = "EXAM_SCORES_SUBMISSION_SESS_"+str(session_number)
        return AcademicCalendar.objects.get(academic_year=academic_year_id, event_type=event_type_criteria)

    def __str__(self):
        return u"%s %s" % (self.academic_year, self.title)


class Offer(models.Model):
    external_id = models.CharField(max_length = 100,blank = True, null = True)
    acronym     = models.CharField(max_length = 15)
    title       = models.CharField(max_length = 255)

    def save(self, *args, **kwargs):
        self.acronym = self.acronym.upper()
        super(Offer, self).save(*args, **kwargs)

    @property
    def structure(self):
        return Structure.objects.filter(id=self.id).structure

    def __str__(self):
        return self.acronym


class OfferYear(models.Model):
    external_id   = models.CharField(max_length = 100,blank = True, null = True)
    offer         = models.ForeignKey(Offer)
    academic_year = models.ForeignKey(AcademicYear)
    acronym       = models.CharField(max_length = 15)
    title         = models.CharField(max_length = 255)
    structure     = models.ForeignKey(Structure)

    def __str__(self):
        return u"%s - %s" % (self.academic_year, self.offer.acronym)

    # This function should not be here.
    def is_programme_manager(self,user):
        person = Person.objects.get(user=user)
        if user:
            programme_manager = ProgrammeManager.objects.filter(person=person.id, faculty=self.structure)
            if programme_manager:
                return True
        return False


class OfferEnrollment(models.Model):
    external_id     = models.CharField(max_length = 100,blank = True, null = True)
    date_enrollment = models.DateField()
    offer_year      = models.ForeignKey(OfferYear)
    student         = models.ForeignKey(Student)

    def __str__(self):
        return u"%s - %s" % (self.student, self.offer_year)


class OfferYearCalendar(models.Model):
    external_id       = models.CharField(max_length = 100,blank = True, null = True)
    academic_calendar = models.ForeignKey(AcademicCalendar)
    offer_year        = models.ForeignKey(OfferYear)
    event_type        = models.CharField(max_length = 50, choices = EVENT_TYPE)
    start_date        = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    end_date          = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)

    def current_session_exam():
        return OfferYearCalendar.objects.filter(event_type__startswith='EXAM_SCORES_SUBMISSION_SESS_'
                                       ).filter(start_date__lte=timezone.now()
                                       ).filter(end_date__gte=timezone.now()).first()

    def __str__(self):
        return u"%s - %s" % (self.academic_calendar, self.offer_year)


class LearningUnit(models.Model):
    external_id = models.CharField(max_length = 100,blank = True, null = True)
    acronym     = models.CharField(max_length = 15)
    title       = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    start_year  = models.IntegerField()
    end_year    = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return u"%s - %s" % (self.acronym, self.title)


class Attribution(models.Model):
    FUNCTION_CHOICES = (
        ('COORDINATOR','Coordinator'),
        ('PROFESSOR','Professor'))

    external_id   = models.CharField(max_length = 100,blank = True, null = True)
    start_date    = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    end_date      = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    function      = models.CharField(max_length = 15, blank = True, null = True,choices = FUNCTION_CHOICES, default = 'UNKNOWN')
    learning_unit = models.ForeignKey(LearningUnit)
    tutor         = models.ForeignKey(Tutor)

    def __str__(self):
        return u"%s - %s" % (self.tutor.person, self.function)


class LearningUnitYear(models.Model):
    external_id    = models.CharField(max_length = 100,blank = True, null = True)
    acronym        = models.CharField(max_length = 15)
    title          = models.CharField(max_length = 255)
    credits        = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True)
    decimal_scores = models.BooleanField(default = False)
    academic_year  = models.ForeignKey(AcademicYear)
    learning_unit  = models.ForeignKey(LearningUnit)

    def __str__(self):
        return u"%s - %s" % (self.academic_year,self.learning_unit)

    def find_offer_enrollments(learning_unit_year_id):
        learning_unit_enrollment_list= LearningUnitEnrollment.objects.filter(learning_unit_year=learning_unit_year_id)
        offer_list = []
        for lue in learning_unit_enrollment_list:
            offer_list.append(lue.offer_enrollment)
        return offer_list


class LearningUnitEnrollment(models.Model):
    external_id        = models.CharField(max_length = 100,blank = True, null = True)
    date_enrollment    = models.DateField()
    learning_unit_year = models.ForeignKey(LearningUnitYear)
    offer_enrollment   = models.ForeignKey(OfferEnrollment)

    @property
    def student(self):
        return self.offer_enrollment.student

    @property
    def offer(self):
        return self.offer_enrollment.offer_year

    def __str__(self):
        return u"%s - %s" % (self.learning_unit_year, self.offer_enrollment.student)


class SessionExam(models.Model):
    SESSION_STATUS = (
        ('IDLE', _('Idle')),
        ('OPEN', _('Open')),
        ('CLOSED', _('Closed')))

    external_id         = models.CharField(max_length = 100,blank = True, null = True)
    number_session      = models.IntegerField()
    status              = models.CharField(max_length = 10,choices = SESSION_STATUS)
    learning_unit_year  = models.ForeignKey(LearningUnitYear)
    offer_year_calendar = models.ForeignKey(OfferYearCalendar)

    def current_session_exam():
        offer_calendar = OfferYearCalendar.current_session_exam()
        session_exam = SessionExam.objects.filter(offer_year_calendar=offer_calendar).first()
        return session_exam

    def find_session(id):
        return SessionExam.objects.get(pk=id)

    def find_sessions_by_tutor(tutor, academic_year):
        learning_units = Attribution.objects.filter(tutor=tutor).values('learning_unit')
        return SessionExam.objects.filter(status='OPEN'
                                 ).filter(learning_unit_year__academic_year=academic_year
                                 ).filter(learning_unit_year__learning_unit__in=learning_units)

    def find_sessions_by_faculty(faculty, academic_year):
        return SessionExam.objects.filter(status='OPEN'
                                 ).filter(offer_year_calendar__offer_year__academic_year=academic_year
                                 ).filter(offer_year_calendar__offer_year__structure=faculty)

    @property
    def offer(self):
        for rec_exam_enrollment in ExamEnrollment.find_exam_enrollments(self):
            return rec_exam_enrollment.learning_unit_enrollment.offer
        return None

    @property
    def progress(self):
        enrollments = list(ExamEnrollment.find_exam_enrollments(self.id))

        if enrollments:
            progress = 0
            for e in enrollments:
                if e.score_final is not None or e.justification_final is not None:
                    progress = progress +1
            return str(progress) + "/"+ str(len(enrollments))
        else:
            return "0/0"

    def __str__(self):
        return u"%s - %d" % (self.learning_unit_year, self.number_session)


class ExamEnrollment(models.Model):
    JUSTIFICATION_TYPES = (
        ('ABSENT',_('Absent')),
        ('CHEATING',_('Cheating')),
        ('ILL',_('Ill')),
        ('JUSTIFIED_ABSENCE',_('Justified absence')),
        ('SCORE_MISSING',_('Score missing')))

    ENCODING_STATUS = (
        ('SAVED',_('Saved')),
        ('SUBMITTED',_('Submitted')))

    external_id              = models.CharField(max_length = 100,blank = True, null = True)
    score_draft              = models.DecimalField(max_digits = 4, decimal_places = 2, blank = True, null = True, validators=[MaxValueValidator(20), MinValueValidator(0)])
    score_reencoded          = models.DecimalField(max_digits = 4, decimal_places = 2, blank = True, null = True, validators=[MaxValueValidator(20), MinValueValidator(0)])
    score_final              = models.DecimalField(max_digits = 4, decimal_places = 2, blank = True, null = True, validators=[MaxValueValidator(20), MinValueValidator(0)])
    justification_draft      = models.CharField(max_length = 20, blank = True, null = True,choices = JUSTIFICATION_TYPES)
    justification_reencoded  = models.CharField(max_length = 20, blank = True, null = True,choices = JUSTIFICATION_TYPES)
    justification_final      = models.CharField(max_length = 20, blank = True, null = True,choices = JUSTIFICATION_TYPES)
    encoding_status          = models.CharField(max_length = 9, blank = True, null = True,choices = ENCODING_STATUS)
    session_exam             = models.ForeignKey(SessionExam)
    learning_unit_enrollment = models.ForeignKey(LearningUnitEnrollment)

    def calculate_progress(enrollments):
        if enrollments:
            progress = len([e for e in enrollments if e.score_draft is not None or e.justification_draft is not None]) / len(enrollments)
        else:
            progress = 0
        return progress * 100

    def find_exam_enrollments(session_exam):
        enrollments = ExamEnrollment.objects.filter(session_exam=session_exam)\
                                            .order_by('learning_unit_enrollment__offer_enrollment__offer_year__acronym',
                                                      'learning_unit_enrollment__offer_enrollment__student__person__last_name',
                                                      'learning_unit_enrollment__offer_enrollment__student__person__first_name')
        return enrollments

    def find_draft_exam_enrollments(session_exam):
        """ Return the enrollments of a session but not the ones already submitted. """
        enrollments = ExamEnrollment.objects.filter(session_exam=session_exam)\
                                            .filter(score_final__isnull=True)\
                                            .filter(justification_final__isnull=True)
        return enrollments

    def count_encoded_scores(enrollments):
        """ Count the scores that were already encoded but not submitted yet. """
        counter = 0
        for enrollment in enrollments:
            if (enrollment.score_draft or enrollment.justification_draft) \
                    and not enrollment.score_final \
                    and not enrollment.justification_final:
                counter += 1

        return counter

    def find_exam_enrollments_to_validate(session_exam):
        enrollments = ExamEnrollment.objects.filter(session_exam=session_exam)\
                                            .filter(~models.Q(score_draft=models.F('score_reencoded')) |
                                                    ~models.Q(justification_draft=models.F('justification_reencoded')))\
                                            .filter(score_final__isnull=True)\
                                            .filter(justification_final__isnull=True)
        return enrollments

    def student(self):
        return self.learning_unit_enrollment.student

    def justification_label(self):
        if self.justification_draft == "ABSENT":
            return _('Absent')
        if self.justification_draft == "ILL":
            return _('Ill')
        if self.justification_draft == "CHEATING":
            return _('Cheating')
        if self.justification_draft == "JUSTIFIED_ABSENCE":
            return _('Justified absence')
        if self.justification_draft == "SCORE_MISSING":
            return _('Score missing')
        return None

    def justification_label_authorized(isFac):
        if isFac:
            return '%s, %s, %s, %s, %s' % (_('Absent'), _('Ill'), _('Cheating'), _('Justified absence'), _('Score missing'))
        else:
            return '%s, %s, %s' % (_('Absent'), _('Ill'), _('Cheating'))

    def __str__(self):
        return u"%s - %s" % (self.session_exam, self.learning_unit_enrollment)