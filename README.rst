=====================
EmissionCalculatorLib
=====================


This python library uses formulas and factors from EU to calculate the emission(s) from personal cars, busses to trailers of various sizes give a start and stop point (see 'examples/simple_planner.py').

You could also calculate the emission for a given vehicle


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


Routing Service
---------------

We are using the Routing Service which serves NPRA's "vegkart": https://www.vegvesen.no/vegkart/vegkart/. The routing services is served from Triona (triona.se).


