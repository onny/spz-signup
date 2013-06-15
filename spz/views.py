# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

from flask import redirect, url_for, flash

from spz import app
from spz.decorators import templated
from spz.headers import upheaders
from spz.forms import SignupForm


@app.route('/', methods=['GET', 'POST'])
@upheaders
@templated('signup.html')
def index():
    form = SignupForm()

    if form.validate_on_submit():
        # applicant = Applicant(first_name = form.first_name.data, ..)
        flash(u'Erfolgreich eingetragen', 'success')
        return redirect(url_for('index'))

    return dict(form=form)


# vim: set tabstop=4 shiftwidth=4 expandtab:
