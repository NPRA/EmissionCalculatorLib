EmissionCalculatorLib
=====================


This python library uses formulas and factors from EU to calculate the emission(s) from personal cars, busses to trailers of various sizes give a start and stop point (see 'examples/simple_planner.py').

You could also calculate the emission for a given vehicle.


Pull requests are more than welcome! Please visit the `project on GitHub <https://github.com/NPRA/EmissionCalculatorLib>`_.
Also checkout the `CHANGELOG.md <CHANGELOG.md>`_.


Quickstart
---------

Show the "make help" and run the test cases

.. highlight:: bash
    :linenothreshold: 5

    $ make help
    Use target: test, install, uninstall, upload or clean

.. highlight:: bash
    :linenothreshold: 5

    $ make test
    Use target: test, install, uninstall, upload or clean


Examples
--------

We have some examples (more to come) under the 'examples' directory. You can use them to view how a simple planning with some pre-defined emissions might look like.

If you see some improvements, bugs or something, then please file a Github issue so we can continue to improve.


Screencast(s)
-------------

To ease the learning curve a bit we've included a screecast to help you get started:

.. image:: https://asciinema.org/a/150349.png
    :width: 150px
    :target: https://asciinema.org/a/150349


Routing Service
---------------

We are using the Routing Service which serves NPRA's "vegkart": https://www.vegvesen.no/vegkart/vegkart/. The routing services is served from Triona (triona.se).


