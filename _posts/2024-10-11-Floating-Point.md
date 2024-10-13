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

Some approximation is necessary since real numbers are continuous and infinite, while computers have finite memory.

A simple solution is **rounding** -- just round off the real number after some decimal places and store the remaining digits.

<video width="100%" controls="controls" loop="loop" autoplay muted>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/RoundOff.mp4" type="video/mp4">
</video>

The rounded numbers form a discrete set, and we can store a finite range of them using a fixed number of digits (or bits).

Let's quantify the error introduced by this rounding. If $x$ is the real number and $\text{round}(x)$ is the rounded number, then the error is given by:

$${\text{error}(x) = \vert x - \text{round}(x)\vert}.$$

This error is called **round-off error**.

An interesting property of this method is that the maximum round-off error is independent of the **magnitude** of the number being stored.
In the above example, we know that the error is at most $0.05$ for any number $x$.

This is because the decimal point is **fixed**.

In fact, this error depends only on which decimal place we round off at. For example, if we round off at the 2nd decimal place instead of the first, then the error is always at most $0.005$. In general,  

$$\text{error}(x) \leq 0.5 \cdot 10^{-d}$$

where $d$ is the decimal place we round off at.

## Absolute vs Relative Error

The error we just discussed is called the **absolute error**. It is the absolute difference between the real number and the approximation.

Another way to quantify the error is by the **relative error**. It is just the absolute error normalized by the magnitude of the number:

$$\text{relative error}(x) = \frac{\text{error}(x)}{\vert x \vert}.$$

Many applications are more interested in the relative error than the absolute error, because the relative error is **scale-invariant**. 

For example, if we are measuring lengths, having a constant absolute error of **1 cm** might be acceptable for measuing the height of a person, but would be completely overkill for measuring the distance between two cities, and would also be absolutely useless for measuring the distance between two components on a microchip.

Instead, a system which always introduces a constant relative error of **1%** can be used for all these applications consistently.


<video width="100%" controls="controls" loop="loop" autoplay muted>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/AbsVsRelError.mp4" type="video/mp4">
</video>

## The log approximation

An elegant method of approximately converting absolute error to relative error is through the **logarithm**.

First, let's assume that our errors are very small, and go so far as to use the notation of infinitesimals from caclulus. 
Specifically, we can say that 

$$\text{error}(x) = dx$$

where $dx$ is an infinitesimal error in $x$. The relative error is then

$$\text{relative error}(x) = \frac{dx}{x}.$$

The neat trick is to observe that the relative error is actually the absolute error of the logarithm of the number:

$$
\large{
\color{#33AA33}
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


# Floating Point Numbers

Computing logarithms is a non-trivial operation in practice, and ideally we would like to avoid having to compute them just to store numbers.

Instead, we can use a simple approximation of the logarithm based on **scientific notation**.

We can rewrite a real number $x$ using scientific notation in base 2 as

$$x = \pm \ (1 + m) \cdot 2^e$$

where $m$, the **mantissa**, is a real number between $0$ and $1$, and $e$, the **exponent** is an integer.

Now, we can use a linear approximation (technically not Taylor since we are in base 2) of the logarithm to get

$$\log_2 x =  \log_2 (1 + m) + e \approx m + e.$$

We can store the sum $m + e$ using fixed point, with the binary point placed right between the bits of $m$ and $e$ -- and this is essentially the floating point system!

The exact choice of how many bits to use for $m$ and $e$ is determined by the **IEEE 754 standard** for floating point numbers. We won't get into all the nitty gritty details of the IEEE standard (like how to deal with 0 and inf) -- this [video by Jan Misali](https://www.youtube.com/watch?v=dQhj5RGtag0) does a splendid job of that. 

Instead here's a brief illustration of the standard on a simple example.

<video width="100%" controls="controls" loop="loop" autoplay muted>
  <source src="{{site.baseurl}}/images/floating_point/mp4s/IEEE.mp4" type="video/mp4">
</video>

You can interactively play with floating point numbers on this great website by Bartosz Ciechanowski -- [float.exposed](https://float.exposed/).

An important bit of nomenclature -- the value of the constant relative error in floating point is called the **machine precision**. 

* For 32-bit floats with 23-bit mantissas, the machine precision is $2^{-24} \approx 10^{-7}$. 
* For 64-bit floats with 52-bit mantissas, the machine precision is $2^{-53} \approx 10^{-16}$.

The main takeaway I'd like to emphasize is:

Floating point is fixed point in log space.
{: style="font-size: 180%; text-align: center;"}


This intuition is very powerful and illuminating. In fact, it is the basis for a famous algorithm to compute inverse square roots -- the **fast inverse square root** algorithm.

### An aside: The Fast Inverse Square Root


The inverse square root function $y = \frac{1}{\sqrt{x}}$ is non-trivial to compute and shows up a lot in applications involving computer graphics, like video games. 

The core idea in the fast inverse square root algorithm is to realize that computing $\log y$ is much simpler -- in fact it is just $-\frac{1}{2} \log x$. 

Since the bit representation of $x$ stored as a floating point number approximates $\log x$, we can use this to approximately compute $\log y$ by simply multiplying the bits of $x$ by $-1/2$ instead of working with the floating point number itself. The resulting bits then represent $y$ when treated as a floating point number.

A detailed and illuminating exposition can be found in this [video by Nemean](https://www.youtube.com/watch?v=p8u_k2LIZyo).


# Propagation of Relative Error

Finally, let's investigate how errors propagate when we compute with floating point numbers. Again, we're interested specifically in the relative error. 

A natural quantity to consider is the **relative conditioning** (denoted by $\kappa_f$) of an operation $f$.

$$
\large{
\color{#33AA33}
\begin{align*}
\kappa_f  &= \frac{\text{relative error in output}}{\text{relative error in input}}\\
&= \left\vert \frac{d (\log f(x))}{d (\log x)} \right\vert. \\
\end{align*}
}
$$

In the computer, all algorithms are ultimately a composition of the fundamental arithmetic operations -- addition, subtraction, multiplication and division. So, the relative error of the output of an algorithm is obtained by accumulating the relative errors of the fundamental operations that make up the algorithm.

Let's consider the relative conditioning of the fundamental operations. We'll assume that the input is a single positive number $x$, and we perform the operation with a positive constant $c$.

* **Addition**: $f(x) = x + c$. 

$$\kappa_f = \frac{d (\log (x + c))}{d (\log x)} = \frac{|x|}{|x + c|}.$$

* **Subtraction**: $f(x) = x - c$.

$$\kappa_f = \frac{d (\log (x - c))}{d (\log x)} = \frac{|x|}{\color{red}|x - c|}.$$

* **Multiplication**: $f(x) = x \cdot c$.

$$\kappa_f = \frac{d (\log (x \cdot c))}{d (\log x)} = 1.$$

* **Division**: $f(x) = x / c$.

$$\kappa_f = \frac{d (\log (x / c))}{d (\log x)} = 1.$$

The conditioning of addition, multiplication and division is bounded for all positive $x$. These operations are **well-conditioned**.

However, the conditioning of subtraction can blow up to infinity when $x$ is close to $c$. 

$$\color{red}\kappa_{\text{subtraction}} = \frac{|x|}{|x - c|} \rightarrow \infty \quad \text{as} \quad x \rightarrow c.$$

**Subtraction is ill-conditioned**.

Note that these conclusions apply even if we consider errors in $c$, though the math gets slightly more involved.


## Catastrophic Cancellation

Another perspective to see the ill-conditioning of subtraction is to look at the bits of the result when we subtract two nearly equal floating point numbers.

A large portion of the most significant bits of the two operands are equal, and they _catastrophically cancel_ to 0, leading to much fewer significant bits in the result -- which corresponds to a blow up of the relative error.


<figure style="display:flex; justify-content:space-around">
<img src="{{site.baseurl}}/images/floating_point/CatastrophicCancellation.svg" alt="Catastrophic Cancellation" style="width: 70%; max-width:700px;">
</figure>

The source of numerical instability in algorithms is almost always due to this ill-conditioning of subtraction. Even the extremely simple task of computing the identity function can suffer if done using (an obviously unnecessary, but illustrative) intermediate subtraction.

Consider two approaches to compute the identity function $f(x) = x$:

1. **Intermediate subtraction**: $f_1(x) = (x + 5) - 5$.
2. **Intermediate multiplication**: $f_2(x) = (x \cdot 5) \ / \ 5$.

For $\vert x \vert \ll 1$, the first approach involves subtracting two nearly equal numbers, namely $x + 5$ and $5$. This results in a blow up of the relative error in the output. Such instability does not occur in the second approach, which involves well-conditioned multiplication and division operations.


<figure class="floating-point-plots-fig">
  <img src="{{site.baseurl}}/images/floating_point/32bit.svg" alt="Identity Function" class="floating-point-plots-img">
  <img src="{{site.baseurl}}/images/floating_point/64bit.svg" alt="Identity Function" class="floating-point-plots-img">
</figure>

The two floating point formats have different precisions, but the qualitative behavior is the same. For $\vert x\vert>1$, both approaches have a relative error around the machine precision. For $\vert x\vert \ll 1$, the relative error in the output of the intermediate subtraction approach blows up, while the intermediate multiplication approach remains stable. 

You can find the code to generate the above plots in this simple [colab notebook](https://colab.research.google.com/drive/1oDTwyg3FTyDlofxk5Pfm1Z2aHXrMzB6m?usp=sharing).

Catastrophic cancellation shows up in more practical scenarios as well -- like [computing variances](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Online_algorithm), solving [quadratic equations](https://people.csail.mit.edu/bkph/articles/Quadratics.pdf), [finite difference schemes](https://en.wikipedia.org/wiki/Numerical_differentiation#/media/File:AbsoluteErrorNumericalDifferentiationExample.png), [Gram-Schmidt orthogonalization](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process#:~:text=.-,Numerical%20stability,-%5Bedit%5D) and many more.

# Final Takeaways

* Round off in a fixed point system results in **constant absolute error**.
* Floating point is fixed point in log space.
* Round off in floating point results in **constant relative error**.
* **Catastrophic cancellation** -- numerical instability due to blow up of relative error when subtracting two nearly equal floating point numbers.


# Useful Links

* Jan Misali's video on [how floating point works](https://www.youtube.com/watch?v=dQhj5RGtag0).
* Nemean's video on the [Fast Inverse Square Root](https://www.youtube.com/watch?v=p8u_k2LIZyo).
* Interative website by Bartosz Ciechanowski to play with floating point numbers -- [float.exposed](https://float.exposed/).
* [Colab notebook](https://colab.research.google.com/drive/1oDTwyg3FTyDlofxk5Pfm1Z2aHXrMzB6m?usp=sharing) to generate the relative error plots. 
* [Code](https://github.com/rajatvd/floating-point) to generate the animations in this post using **`manim`**.

