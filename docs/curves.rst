Drawing Complex Curves
======================

Challenges:

* capture the intent of a curve;
* make the curve smooth-looking, i.e., avoid discontinuities in the higher-order
  derivatives;
* handle multi-valued functions (i.e., the independent coordinate is not
  monotonically increasing along the lines).

Bonus desirable features:

* allow scaling easily;
* allow fixed-size borders (e.g., for carved designs);

Possible approaces:

* map the curve derivative as a function of the independent coordinate
  (how we handle x going backwards? and vertical lines?);
* map the angle wrt horizontal as a function of the independent coordinate
  (this is nice as we avoid infinities for vertical lines, and we can handle
  x going in both directions);
* map the *derivative* of the angle wrt horizontal as a function of the
  independent variable (I have a sense this might help with connections and
  smoothness, but we loose the immediate connection with the actual curve
  appearance).

We should keep in mind that the specification (i.e., the way we input the curve)
and the internal representation can be completely different (e.g., the latter
will almost certainly be implemented along the curve, while the former is easier
in x).
