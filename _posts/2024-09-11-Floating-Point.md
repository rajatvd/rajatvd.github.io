---
layout: post
title: Floating Point Numbers
watch: true
excerpt: Understanding floating point numbers
image:
    path: images/floating_point/gifs/RoundOff.gif
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

## Absolute vs Relative Error

The error we just discussed is called the **absolute error**. It is the absolute difference between the real number and the approximation.

Another way to quantify the error is by the **relative error**. It is just the absolute error normalized by the magnitude of the number:

$$\text{relative error}(x) = \frac{\text{error}(x)}{\vert x \vert}.$$

Many applications are more interested in the relative error than the absolute error, because the relative error is **scale-invariant**. 
For example, if we are measuring the length of a rod, we are more interested in the error as a percentage of the length of the rod, instead of the error in some absolute units.


-----Animation of relative error being scale-invariant-----


### The log approximation

An elegant method of approximately converting absolute error to relative error is through the **logarithm**.

First, let's assume that our errors are very small, and go so far as to use the notation of infinitesimals from caclulus. 
Specifically, we can say that 

$$\text{error}(x) = dx$$

where $dx$ is an infinitesimal error in $x$.

The relative error is then

$$\text{relative error}(x) = \frac{dx}{x}.$$

The neat trick that allows us to relate the two errors elegantly is to observe that the relative error is actually the absolute error of the logarithm of the number:

$$\text{error}(\log x) = d(\log x) = \frac{dx}{x} = \text{relative error}(x)$$

where we used the fact that the derivative of $\log x$ is $1/x$.

So now, if we want a storage scheme that has a fixed relative error, we can simply **store the logarithm of the number using fixed point.**
This is exactly what floating point numbers do!

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
