---
layout: post
title: Floating Point Numbers
watch: true
excerpt: Understanding floating point numbers
image:
    path: images/neural_ode/cover.png
    width: 90%
comments: true
---

How do we store real numbers in a computer?
{: style="font-size: 120%; text-align: center;"}

<!-- ### Prelude -- Fixed Point Numbers -->

Some approximation is clearly necessary since real numbers are continuous and infinite, while computers have finite memory.

A simple solution is **rounding** -- just round off the real number at some specific decimal place and store the remaining digits.

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/RoundOff.mp4" type="video/mp4">
</video>

The rounded numbers form a discrete set, and we can store a finite range of them using a fixed number of digits (or bits).

Let's quantify the error introduced by this rounding. If x is the real number and round(x) is the rounded number, then the error is given by:

$$\text{error}(x) = \vert x - \text{round}(x)\vert.$$

This error is called **round-off error**.

An interesting property of this method is that the error is independent of the **magnitude** of the number being stored.
In the above example, we know that the error is at most $0.05$ for any number $x$.

This is because the decimal point is **fixed**.

In fact, this error depends only on which decimal place we round off at. For example, if we round off at the 2nd decimal place instead of the first, then the error is always at most $0.005$.

In general,  

$$\text{error}(x) \leq 0.5 \cdot 10^{-d}$$

where $d$ is the decimal place we round off at.

-----Absolute vs relative error, and how log takes us from one to the other-----

-----Get constant error by using fixed point to store log of number-----

-----Animation of log making floating point numbers uniformly spaced-----

Floating point is fixed point in log space.
{: style="font-size: 180%; text-align: center;"}

-----Exact IEEE format for binary floating point numbers-----

## Propagation of Relative Error

* Errors propagation via interval arithmetic.

* Conditioning is just the derivative.
* Relative conditioning is just the derivative in log space.
* Of the fundamental arithmetic operations, only subtraction is ill-conditioned.
** Catastrophic cancellation perspective of ill-conditionness of subtraction.
* Example of two ways to compute the same function, one of which is ill-conditioned.

---- Animation of subtraction being ill-conditioned ----
