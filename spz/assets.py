# -*- coding: utf-8 -*-

"""Register assets for optimizations.

   We optimize and merge assets into bundles, in order to reduce the client's connections
   from number of assets down to number of bundles.

   Register static files for those asset bundles here.

   We support the two most common and mature filters only:
        - rjsmin (for *.js files)
        - cssmin (for *.css files)

   .. note::
      Paths are relative to the static directory.

   .. warning::
      Synchronize this listing with static directory changes.
"""

from flask.ext.assets import Bundle


all_js = Bundle('js/jquery-1.10.1.min.js',
                'js/mailcheck.1.0.2.min.js',
                'js/garlic-1.2.2.min.js',
                'js/parsley-1.1.16.min.js',
                filters='rjsmin', output='js/packed.js')


# vim: set tabstop=4 shiftwidth=4 expandtab: