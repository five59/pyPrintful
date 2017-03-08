Quick Start
===========

Installation
------------

To install this package, just type:

::

  pip3 install pyPrintful


This will load the package as well as any additional requirements to your
development environment.

Basic Usage
-----------

Simply add the requisite import to your script and make the requisite call to
the API wrapper:

  >>> from pyPrintful import *
  >>> import json

  >>> my_key = "XXXXXXXXXXXX:XXXXXXXXXXXXXXX"

  >>> p = pyPrintful(key=my_key)
  >>> data = p.get_store_info()

  >>> print( json.dumps( data, indent=4 ) )

(Note that I'm importing the 'json' package here so that the output is pretty,
but it's not required).

Check out the module documentation for additional methods. You can call the
named methods ( such as get_store_info() ), or if you need to go lower, you
also have access to:

- do_get()
- do_post()
- do_delete()
- do_put()
