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
from io import StringIO
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Tutor, AcademicCalendar, SessionExam, ExamEnrollment
from . import pdf_utils
from . import export_utils
from core.forms import ScoreFileForm
from core.models import *


def page_not_found(request):
    return render(request,'page_not_found.html')


def access_denied(request):
    return render(request,'acces_denied.html')


def home(request):
    return render(request, "home.html")


@login_required
def studies(request):
    return render(request, "studies.html", {'section': 'studies'})


@login_required
def assessments(request):
    return render(request, "assessments.html", {'section': 'assessments'})


@login_required
def scores_encoding(request):
    academic_year = AcademicCalendar.current_academic_year()

    tutor = Tutor.find_by_user(request.user)
    # In case the user is a tutor.
    sessions = None
    faculty = None
    if tutor:
        sessions = SessionExam.find_sessions_by_tutor(tutor, academic_year)
    # In case the user is not a tutor we check whether it is member of a faculty.
    elif request.user.groups.filter(name='FAC').exists():
        faculty = ProgrammeManager.find_faculty_by_user(request.user)
        if faculty:
            sessions = SessionExam.find_sessions_by_faculty(faculty, academic_year)

    # Calculate the progress of all courses of the tutor.
    all_enrollments = []

    if sessions:
        for session in sessions:
            enrollments = list(ExamEnrollment.find_exam_enrollments(session))
            if enrollments:
                all_enrollments = all_enrollments + enrollments

    progress = ExamEnrollment.calculate_progress(all_enrollments)

    return render(request, "scores_encoding.html",
                  {'section':       'scores_encoding',
                   'tutor':         tutor,
                   'faculty':       faculty,
                   'academic_year': academic_year,
                   'session':       sessions.first(),
                   'sessions':      sessions,
                   'progress':      "{0:.0f}".format(progress)})


@login_required
def online_encoding(request, session_id):
    tutor = None
    faculty = ProgrammeManager.find_faculty_by_user(request.user)
    if not faculty:
        tutor = Tutor.find_by_user(request.user)

    academic_year = AcademicCalendar.current_academic_year()
    session = SessionExam.find_session(session_id)
    enrollments = ExamEnrollment.find_exam_enrollments(session.id)
    progress = ExamEnrollment.calculate_progress(enrollments)
    num_encoded_scores = ExamEnrollment.count_encoded_scores(enrollments)

    return render(request, "online_encoding.html",
                  {'section': 'scores_encoding',
                   'tutor': tutor,
                   'faculty': faculty,
                   'academic_year': academic_year,
                   'session': session,
                   'progress': "{0:.0f}".format(progress),
                   'enrollments': enrollments,
                   'num_encoded_scores': num_encoded_scores})


@login_required
def online_encoding_form(request, session_id):
    session = SessionExam.find_session(session_id)
    enrollments = ExamEnrollment.find_exam_enrollments(session)
    if request.method == 'GET':
        tutor = Tutor.find_by_user(request.user)
        academic_year = AcademicCalendar.current_academic_year()
        return render(request, "online_encoding_form.html",
                      {'section':       'scores_encoding',
                       'tutor':         tutor,
                       'academic_year': academic_year,
                       'session':       session,
                       'enrollments':   enrollments,
                       'justifications':ExamEnrollment.JUSTIFICATION_TYPES})
    elif request.method == 'POST':
        for enrollment in enrollments:
            score = request.POST.get('score_' + str(enrollment.id), None)
            if score:
                if enrollment.learning_unit_enrollment.learning_unit_year.decimal_scores:
                    enrollment.score_draft = float(score)
                else:
                    enrollment.score_draft = int(float(score))
            else:
                enrollment.score_draft = enrollment.score_final

            enrollment.justification_draft = request.POST.get('justification_' + str(enrollment.id), None)
            enrollment.save()
        return online_encoding(request, session_id)


@login_required
def online_double_encoding_form(request, session_id):
    session = SessionExam.find_session(session_id)
    enrollments = ExamEnrollment.find_exam_enrollments(session.id)
    if request.method == 'GET':
        tutor = Tutor.find_by_user(request.user)
        academic_year = AcademicCalendar.current_academic_year()
        return render(request, "online_double_encoding_form.html",
                      {'section':       'scores_encoding',
                       'tutor':         tutor,
                       'academic_year': academic_year,
                       'session':       session,
                       'enrollments':   enrollments,
                       'justifications':ExamEnrollment.JUSTIFICATION_TYPES})
    elif request.method == 'POST':
        for enrollment in enrollments:
            score = request.POST.get('score_' + str(enrollment.id), None)
            if score:
                if enrollment.learning_unit_enrollment.learning_unit_year.decimal_scores:
                    enrollment.score_reencoded = float(score)
                else:
                    enrollment.score_reencoded = int(float(score))
            enrollment.justification_reencoded = request.POST.get('justification_' + str(enrollment.id), None)
            enrollment.save()
        return HttpResponseRedirect(reverse('online_double_encoding_validation', args=(session.id,)))


@login_required
def online_double_encoding_validation(request, session_id):
    session = SessionExam.find_session(session_id)
    if request.method == 'GET':
        tutor = Tutor.find_by_user(request.user)
        academic_year = AcademicCalendar.current_academic_year()
        enrollments = ExamEnrollment.find_exam_enrollments_to_validate(session)
        return render(request, "online_double_encoding_validation.html",
                      {'section': 'scores_encoding',
                       'tutor': tutor,
                       'academic_year': academic_year,
                       'session': session,
                       'enrollments': enrollments,
                       'justifications': ExamEnrollment.JUSTIFICATION_TYPES})
    elif request.method == 'POST':
        enrollments = ExamEnrollment.find_exam_enrollments(session)
        for enrollment in enrollments:
            score = request.POST.get('score_' + str(enrollment.id), None)
            if score:
                if enrollment.learning_unit_enrollment.learning_unit_year.decimal_scores:
                    enrollment.score_final = float(score)
                else:
                    enrollment.score_final = int(float(score))
            else:
                enrollment.score_final = enrollment.score_draft

            justification = request.POST.get('justification_' + str(enrollment.id), None)
            if justification:
                enrollment.justification_final = justification
            else:
                enrollment.justification_final = enrollment.justification_draft
        return online_encoding(request, session_id)


@login_required
def online_encoding_submission(request, session_id):
    session_exam = SessionExam.find_session(session_id)
    enrollments = ExamEnrollment.find_draft_exam_enrollments(session_exam)
    all_encoded = True
    for enrollment in enrollments:
        if enrollment.score_draft or enrollment.justification_draft:
            enrollment.score_final = enrollment.score_draft
            enrollment.justification_final = enrollment.justification_draft
            enrollment.save()
        else:
            all_encoded = False

    if all_encoded:
        session_exam.status = 'CLOSED'
        session_exam.save()

    return HttpResponseRedirect(reverse('online_encoding', args=(session_id,)))


@login_required
def notes_printing(request,session_exam_id,learning_unit_year_id):
    tutor = Tutor.find_by_user(request.user)
    academic_year = AcademicCalendar.current_academic_year()
    session_exam = SessionExam.find_session(session_exam_id)
    sessions = SessionExam.find_sessions_by_tutor(tutor, academic_year)
    return pdf_utils.print_notes(request,tutor,academic_year,session_exam,sessions,learning_unit_year_id)


@login_required
def upload_score_error(request):
    return render(request, "upload_score_error.html", {})


@login_required
def notes_printing(request, session_id, learning_unit_year_id):
    tutor = Tutor.find_by_user(request.user)
    academic_year = AcademicCalendar.current_academic_year()
    session_exam = SessionExam.current_session_exam()
    sessions = SessionExam.find_sessions_by_tutor(tutor, academic_year)
    return pdf_utils.print_notes(request,tutor,academic_year,session_exam,sessions,learning_unit_year_id)


@login_required
def notes_printing_all(request, session_id):
    return notes_printing(request,session_id,-1)


@login_required
def programme(request):
    return render(request, "programme.html", {'section': 'programme'})


@login_required
def export_xls(request, session_id, learning_unit_year_id, academic_year_id):
    return export_utils.export_xls(request, session_id, learning_unit_year_id, academic_year_id, request.user.groups.filter(name='FAC').exists())


def offers(request):
    validity = None
    faculty = None
    code = ""

    faculties = Structure.objects.all().order_by('acronym')
    validities = AcademicYear.objects.all().order_by('year')

    academic_year = AcademicCalendar.current_academic_year()
    if not(academic_year is None):
        validity = academic_year.id
    return render(request, "offers.html", {'faculties':     faculties,
                                           'validity':      validity,
                                           'faculty':       faculty,
                                           'code':          code,
                                           'validities':    validities,
                                           'offers':        [] ,
                                           'init':          "1"})

def offers_search(request):
    faculty = request.GET['faculty']
    validity = request.GET['validity']
    code = request.GET['code']

    faculties = Structure.objects.all().order_by('acronym')
    validities = AcademicYear.objects.all().order_by('year')

    if validity is None:
        academic_year = AcademicCalendar.current_academic_year()
        if not(academic_year is None):
            validity = academic_year.id

    query = OfferYear.objects.filter(academic_year=int(validity))

    if not(faculty is None) and faculty != "*" :
        query = query.filter(structure=int(faculty))

    if not(code is None) and len(code) > 0  :
        query = query.filter(acronym__startswith=code)

    return render(request, "offers.html", {'faculties':     faculties,
                                           'validity':      int(validity),
                                           'faculty':       int(faculty),
                                           'code':          code,
                                           'validities':    validities,
                                           'offers':        query ,
                                           'init':          "0"})