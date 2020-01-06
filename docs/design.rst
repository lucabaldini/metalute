Design principles
=================

The scale length and the string spacing are two of the figures that it makes
sense start the design of a guitar from.
The scale length determines the length and the detailed layout of the freatboard
(and therefore the design of the neck), while the string spacing determines
the placement of the bridge on the guitar body as well as the design of the
headstock and the pickup choice.


Scale length
------------

The scale length or scale of a string instrument is the maximum vibrating length
of the strings that produce sound, and determines the range of tones that a
string can produce at a given tension. It's also called string length.

(Operationally, the scale length is measured by doubling the distance between
the nut and the 12th fret.)

The scale length of an electric guitar affects both its playability and its tone.
Regarding playability, a shorter scale length allows more compact fingering and
favors shorter fingers and hand-span. A longer scale allows more expanded finger
and favors longer fingers and hand-span. With regard to tone, a longer scale
favors "brightness" or cleaner overtones and more separated harmonics versus a
shorter scale scale length), which favors "warmth" or more muddy overtones.

Practical scale lengths range from 19.4 in (492 mm) to 30 in (762 mm), with
the "standard" Fender Stratocaster sitting at 25.5 in (648 mm).

.. list-table:: `Sample scale lenghts <https://en.wikipedia.org/wiki/Scale_length_(string_instruments)#Electric_guitar>`_
   :widths: 50 50
   :align: center
   :header-rows: 1

   * - Model
     - Scale length
   * - Red special
     - 610 mm
   * - Fender Jaguar/Mustang
     - 610 mm
   * - Gibson Les Paul and SG
     - 628 mm
   * - Paul Red Smith
     - 635 mm
   * - Fender Stratocaster
     - 648 mm
   * - Ibanez
     - 648 mm


String spread
-------------

The string spacing is a concept somewhat more subtle than a plain number, as
the distance between adjacent strings changes along the string itself. One
convenient way of describing the string spacing pattern is to provide the string
spread (i.e., the distance between the center of the low-E string and that of
the high-E one, assuming a 6-string configuration with the standard tuning) at
the nut and at the bridge.

The string spread at the nut is typically 33 to 38 mm, while the string spread
at the bridge ranges from 51 to 57 mm. Traditionally, Fender designs tend to
be somewhat larger than Gibson's.
`Floyd Rose <https://floydrose.com/products/original-locking-nut?variant=30510945234>`_
nuts for 6-string guitars are available in 10 different flavors, with a string
spread ranging from 33.25 mm to 36.45 mm. The string spread for the original
Floyd Rose bridge is 53.50 mm.

Once the scale length is decided, the choice of the nut and bridge specs
fixes pretty much the entire geometry of the strings, i.e.,

.. math::
 s(x) = s_{nut} + x \frac{(s_{bridge} - s_{nut})}{L},
 :label: eq_string_spread

where :math:`s(x)` is the string spread at a generic distance :math:`s(x)` from
the nut, and :math:`L` is the scale length. This, in turn, is relevant for both
the design of the freatboard, and for the choice of the pickups. Incidentally,
`Di Marzio <https://d2emr0qhzqfj88.cloudfront.net/String_Spacing_Template.pdf>`_
offers pickups in two different sizes:

* standard spacing, at 48.64 mm E-to-E;
* F spacing, at 51.05 mm E-to-E.
