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


String Gauges
-------------

String gauges are identified as a series of (typically 6) numbers, expressing
the thickness of each string (in inches). A light, .009"--.046" gauge, for
instance, features a 0.009 in thick high E and a 0.046 in thick low E, as
illustrated in the following table.

.. list-table:: Typical string gauge
   :widths: 50 50
   :align: center
   :header-rows: 1

   * - String
     - Thickness
   * - High E (E4)
     - 0.009 in (0.229 mm)
   * - B (B3)
     - 0.011 in (0.279 mm)
   * - G (G3)
     - 0.016 in (0.406 mm)
   * - D (D3)
     - 0.026 in (0.660 mm)
   * - A (A2)
     - 0.036 in (0.914 mm)
   * - Low E (E2)
     - 0.046 in (1.168 mm)
