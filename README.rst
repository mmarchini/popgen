popgen
======

.. image:: https://magnum.travis-ci.com/mmarchini/popgen.svg?token=yf1zCW46NXpQ9nShXMSz
    :target: https://magnum.travis-ci.com/mmarchini/popgen

Algorithmic Composition of Popular Music
----------------------------------------

Package providing tools for algorithmic composition of popular music. This
implementation is heavily based on the framework presented by *Andres Elowsson* and
*Anders Friberg* on their paper:

Elowsson, Anders, and Anders Friberg. "Algorithmic composition of popular music."
*Royal Institute of Technology, Stockholm, Sweden* (2012).

Implementation
--------------

.. image:: flow.png

TODO
----

These are the features that will be implemented in the near future:

- Tempo
    - User-defined distribution with discrete and continuous random values
- Rhythm Pattern
    - Improved rules
        - Hihat and ride note length probabilities based on tempo
        - Improved rules for kicks distribution
        - Improved rules for snare
    - More isolation, allowing more customized rules
- Rhythm Dynamics
- Harmony
    - Implementation of other modes (at least Aeolian/Minor scale)
- Phrasing
- Melody
