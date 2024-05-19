---
layout: post
title: Floating Point Numbers
watch: true
excerpt: Understanding floating point number
image:
    path: /images/neural_ode/cover.png
    width: 90%
comments: true
---

We begin with a simple question:

How do we store real numbers in a computer?

An immediate issue is that there are infinite real numbers, even in a finite range like -1 to 1, while computers have finite memory.

A simple solution is **rounding** -- just round off the real number at some specific decimal place and store the remaining digits.

TODO: choose right values for example to look nice
For example, if we round off after the 2nd decimal place, then 0.4239... becomes 0.42.

<Insert visualization of round off with fixed decimal point and caption>

Clearly, this isn't a perfect way to store real numbers since we lose information. Different real numbers get mapped to the same rounded number in the computer.

The error introduced by this rounding off is called **round-off error**.

err(x) = |x - round(x)|

An interesting property of this method is that the error is constant -- it doesn't depend on the value of the number being stored. This is because the decimal point is **fixed**.

In fact, this error depends only on which decimal place we round off at. For example, if we round off at the 2nd decimal place, then the error is always at most 0.005.

In general, the err(x) < 0.5 \* 10^(-d), where d is the decimal place we round off at.

<Insert visualization of constant round-off error, but varying relative error and caption>

This is great for large numbers, but not so great for small numbers. This non-uniformity in the error is not ideal for most applications.

We usually care more about the **relative error** -- the error as a fraction of the number being stored.

relative_err(x) = |x - round(x)| / |x|

How can we make the relative error uniform over all numbers?

Choose the decimal place to round at based on the size of the number.

Choose d such that 0.5 \* 10^(-d) / |x| is roughly constant.

An easy way to think about this is using **scientific notation**.

<Basic visualization of scientific notation>

The **mantissa** or **significand** captures the digits of the number, and the **exponent** captures the magnitude of the number.

Now, deciding which decimal place to round off based on the magnitude is equivalent to choosing a fixed number of bits to keep for the mantissa.


----------------- NOTES ----------------

# Storing numbers in a computer

A simple attempt: store like integers, with an implicit decimal point.

Round off errors -- introduce interval to visualize error.

Leads to constant rounding errors -- animate the value increasing but error staying fixed.

-   Great for large numbers, bad for small numbers -- the resolution is not uniform.

# Relative vs Absolute error

A better idea: use some bits to store the digits, and some to store the position of the decimal point.

constant **relative error**

Leads to constant relative errors -- animate the value increasing and error growing accordingly.

Understanding relative errors using logarithms.

Constant error in log number line.

# Perspectives on the ill-conditionness of subtraction

-   Algebraic -- logarithm
-   Catastrophic cancellation of significant digits
-   Interval arithmetic

# Example of two ways to compute the same function

## Quadratic formula
