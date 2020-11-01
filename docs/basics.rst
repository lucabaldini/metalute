Basic Concepts
==============

Octaves and Tones
-----------------

An octave is the interval between one musical pitch and another with double its
frequency. The distance between two frequencies in octaves can be readily
calculated as

..  math::
  \text{octaves}(\nu_1, \nu_2) = \log_2\left( \frac{\nu_2}{\nu_1} \right).

In an\ twelve-tone equal tempered scale each octave is divided in 12 semitones,
and the distance in semitones reads

..  math::
  \text{semitones}(\nu_1, \nu_2) = 12 \log_2\left( \frac{\nu_2}{\nu_1} \right).

Additionally, intervals smaller than a semitone are expressed in cents (a cent
being the hundredth part of a semitone)

..  math::
  \text{cents}(\nu_1, \nu_2) = 1200 \log_2\left( \frac{\nu_2}{\nu_1} \right).


Pitch Notation
--------------

Notes are customarily specified in the so-called
`scientific pitch notation <https://en.wikipedia.org/wiki/Scientific_pitch_notation>`_,
where a pitch is identified by combining a musical note name (with accidental
if needed) and a number identifying the pitch's octave. C4, e.g., is the C of
the fourth octave.

A progressive note number corresponds to each tone identifier, with number 0
assigned to C0. The standard frequency reference is set to 440 Hz (exact) for A4
(corresponding to note number 69), and the frequency for a generic note can
be readily expressed as

.. math::
  \text{freq}(n) = 440. \times 2^{\frac{(n-69)}{12}}.

Note n, here, can be either an integer or a floating-point (i.e., with cents)
note number.

The standard guitar range for a 24-fret freatboard is E2 to E6.


The Vibrating String
--------------------

Vibrating strings are the basis of string instruments such as the guitar.
Although entire books exist on this very subject, a single formula, expressing
the frequency of the sound emitted as a function of the length of the string,
its tension and the linear mass density

.. math::
  \nu = \frac{1}{2\ell} \sqrt{\frac{\tau}{\mu}}

is sufficient for our purposes.

More commonly, we'd like to express the tension of the string as a function of
the other parameters:

.. math::
  \tau = 4 \ell^2 \nu^2 \mu.

Now, the linear density of a homogeneous string with a circular cross section
with diameter d can be written as

.. math::
  \mu = \varrho \pi \frac{d^2}{4}

and, therefore, the tension reads

.. math::
  \tau = \pi \varrho (\ell d \nu)^2.

It goes without saying that the homogeneous-string approximation breaks down
badly for wounded strings, but since most strings (coating aside) are made
of stainless steel (or, at least, the core is) one can fold the density of the
still into the equation to get useful effective formulas for quick calculations

.. math::
  \tau~\text{[N]} = 1.591 \times 10^{-5} (\ell~\text{[mm]} d~\text{[in]} \nu~\text{[Hz]})^2
