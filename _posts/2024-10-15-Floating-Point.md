---
layout: post
title: Perspectives on Floating Point
watch: true
excerpt: An illuminating perspective on floating point numbers that I haven't seen emphasized before.
image:
    type: mp4
    path: images/floating_point/mp4s/LogFixedPoint.mp4
    width: 90%
comments: true
---

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: {
      equationNumbers: {
        autoNumber: "False"
      }
    }
  });
</script>

How do we store real numbers in a computer?
{: style="font-size: 120%; text-align: center;"}

<!-- ### Prelude -- Fixed Point Numbers -->

Some approximation is necessary since real numbers are continuous and infinite, while computers have finite memory.

A simple solution is **rounding** -- just round off the real number after some decimal places and store the remaining digits.

<video width="100%" controls="controls" loop="loop" autoplay muted>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/RoundOff.mp4" type="video/mp4">
</video>

The rounded numbers form a discrete set, and we can store a finite range of them using a fixed number of digits (or bits).

Let's quantify the error introduced by this rounding. If x is the real number and round(x) is the rounded number, then the error is given by:

$${\text{error}(x) = \vert x - \text{round}(x)\vert}.$$

This error is called **round-off error**.

An interesting property of this method is that the round-off error is independent of the **magnitude** of the number being stored.
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

For example, if we are measuring lengths, having a constant absolute error of **1cm** might be acceptable for measuing the height of a person, but would be completely overkill for measuring the distance between two cities, and would also be absolutely useless for measuring the distance between two components on a microchip.

Instead, a system which always introduces a constant relative error of **1%** can be used for all these applications consistently.


<video width="100%" controls="controls" loop="loop" autoplay muted>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/AbsVsRelError.mp4" type="video/mp4">
</video>

### The log approximation

An elegant method of approximately converting absolute error to relative error is through the **logarithm**.

First, let's assume that our errors are very small, and go so far as to use the notation of infinitesimals from caclulus. 
Specifically, we can say that 

$$\text{error}(x) = dx$$

where $dx$ is an infinitesimal error in $x$.

The relative error is then

$$\text{relative error}(x) = \frac{dx}{x}.$$

The neat trick is to observe that the relative error is actually the absolute error of the logarithm of the number:

$$
\large{
\color{#338833}
\begin{align*}
\text{error}(\log x) &= d(\log x) \\
&= \frac{dx}{x} \\
&= \text{relative error}(x)
\end{align*}
}
$$

where we used the fact that the derivative of $\log x$ is $1/x$.

So now, if we want a storage scheme that has a fixed relative error, we can simply **store the logarithm of the number using fixed point.**
This is essentially what floating point does!

<video width="100%" controls="controls" loop="loop" autoplay muted>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/LogFixedPoint.mp4" type="video/mp4">
</video>

Before moving forward, let's switch to binary numbers, since that's what computers actually use in practice.
The same ideas of the logarithm and fixed point apply to binary numbers as well, since we simply have a different base for the log.
In binary, the only digits -- rather bits -- are $0$ and $1$. For example, the decimal number $5.25$ would be represented as $101.01$ in binary.


## Floating Point Numbers

Computing logarithms is a non-trivial operation in practice, and ideally we would like to avoid having to compute them just to store numbers.

Instead, we can use a simple approximation to the logarithm based on **scientific notation**.

We can rewrite a real number $x$ as

$$x = \pm \ (1 + m) \cdot 2^e$$

where $m$ is a number between $0$ and $1$, and $e$ is an integer.

Now, we can use a linear approximation (technically not Taylor since we are in base 2a) of the logarithm to get

$$\log_2 x =  \log_2 (1 + m) + e \approx m + e.$$

Now, we can store the sum $m + e$ using fixed point, with the binary point placed right between the bits of $m$ and $e$.a

The exact choice of how many bits to use for $m$ and $e$ is determined by the **IEEE 754 standard** for floating point numbers. We won't get into all the nitty gritty details of the IEEE standard (like how to deal with 0 and inf) -- this [video by Jan Misali](https://www.youtube.com/watch?v=dQhj5RGtag0) does a splendid job of that. 

Instead here's a brief illustration of the standard on some simple examples.


The main takeaway I'd like to emphasize is:

Floating point is fixed point in log space.
{: style="font-size: 180%; text-align: center;"}


This intuition is very powerful and illuminating. In fact, it is the basis for a famous algorithm to compute inverse square roots -- the **fast inverse square root** algorithm.

### An aside: The Fast Inverse Square Root


The inverse square root function $y = \frac{1}{\sqrt{x}}$ is non-trivial to compute and shows up a lot in applications involving computer graphics, like video games. 

The core idea in the fast inverse square root algorithm is to realize that computing $\log y$ is much simpler -- in fact it is just $-\frac{1}{2} \log x$. 

Since the bit representation of $x$ stored as a floating point number approximates the $\log x$, we can use this to approximately compute $\log y$ by simply working with the bits of $x$ instead of the floating point number itself. The resulting bits then represent $y$ when treated as a floating point number.

A detailed and illuminating exposition can be found in this [video by Nemean](https://www.youtube.com/watch?v=p8u_k2LIZyo).


# Propagation of Relative Error



* Errors propagation via interval arithmetic.

* Conditioning is just the derivative.
* Relative conditioning is just the derivative in log space.
* Of the fundamental arithmetic operations, only subtraction is ill-conditioned.
** Catastrophic cancellation perspective of ill-conditionness of subtraction.
* Example of two ways to compute the same function, one of which is ill-conditioned.

---- Animation of subtraction being ill-conditioned ----