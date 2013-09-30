# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

import socket  # To check for SMTP connectivity error only
import os

from flask import request, redirect, render_template, url_for, flash
from flask.ext.mail import Message
from werkzeug import secure_filename


from spz import app, models, mail, db
from spz.decorators import templated, auth_required
from spz.headers import upheaders
from spz.forms import SignupForm, NotificationForm


@upheaders
@templated('signup.html')
def index():
    form = SignupForm()

    if form.validate_on_submit():
        erg = BerErg(form)
        flash(u'Ihre Angaben waren plausibel', 'success')
        return render_template('confirm.html', erg=erg)

    return dict(form=form)


#hier werde die Teilnahmebedingunen geprüft
def BerErg(form):
    who = form.first_name.data + ' ' + form.last_name.data
    mat = form.tag.data
    mail = form.mail.data
    kurs_id = form.course.data

    kurs = models.Course.query.get(kurs_id)
    lang = models.Language.query.get(kurs.language_id)
    k = '%s %s (%s %s)' % (lang.name, kurs.level, kurs.language_id, kurs.id)

    erg = dict(a=who, b=mat, c=mail, d=k)
    return erg


@upheaders
@templated('licenses.html')
def licenses():
    return None


@upheaders
@templated('internal/overview.html')
def internal():
    return None


@upheaders
@auth_required
@templated('internal/statistics.html')
def statistics():
    return None


@upheaders
@auth_required
@templated('internal/datainput.html')
def datainput():
    return None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@upheaders
@auth_required
@templated('internal/datainput/matrikelnummer.html')
def matrikelnummer():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            lst = {models.Registration(line) for line in fp}
            gel = models.Registration.query.delete()
            db.session.add_all(lst)
            db.session.commit()
            anz = models.Registration.query.count()
            flash(u'Dateiname war OK %s Zeilne gelöscht %s Zeilen gelesen' % (gel, anz), 'success')
#            print '\nFile %s uploaded: %s records\n' % (fp.filename, anz)


            return redirect(url_for('matrikelnummer', filename=fp.filename))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        msg = '\n%s: Wrong file name \n\n' % (fp.filename)
        print msg
        return redirect(url_for('matrikelnummer'))
    return None


@upheaders
@auth_required
@templated('internal/datainput/zulassungen.html')
def zulassungen():
    return None


@upheaders
@auth_required
@templated('internal/notifications.html')
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        try:
            # TODO(daniel): extract recipients from courses; sender from config
            msg = Message(subject=form.mail_subject.data, body=form.mail_body.data, recipients=None, sender=None, cc=None, bcc=None)
            mail.send(msg)
            flash(u'Mail erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash(u'Mail wurde nicht verschickt: {0}'.format(e), 'danger')

    return dict(form=form)


@upheaders
@auth_required
@templated('internal/lists.html')
def lists():
    return dict(languages=models.Language.query.all())


@upheaders
@auth_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


@upheaders
@auth_required
@templated('internal/language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@upheaders
@auth_required
@templated('internal/applicant.html')
def applicant(id):
    return dict(applicant=models.Applicant.query.get_or_404(id))


# vim: set tabstop=4 shiftwidth=4 expandtab:
