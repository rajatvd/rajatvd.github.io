---
layout: post
title: Visualizing Tensor Operations with Factor Graphs
watch: true
excerpt: The factor graph is a beautiful tool for visualizating complex matrix operations and understanding tensor networks, as well as proving seemingly complicated properties through simple visual proofs.
image:
    path: images/factor_graphs/mp4s/TraceCyclic.mp4
    width: 90%
comments: true

---

<blockquote>
From [Grothendieck], I have also learned not to take glory in the difficulty of a proof: difficulty means we have not understood. The idea is to be able to <b>paint a landscape</b> in which the proof is obvious.


<p>&mdash; Pierre Deligne</p>
</blockquote>



Trying to understand operations involving multidimensional arrays can get quite tricky as we go into dimensions beyond 2 or 3. However, certain properties of matrices themselves may seem surprising the first time you encounter them. One example of this is the _cyclic property_ of the trace operation.

$$\text{tr}(ABC) = \text{tr}(CAB) = \text{tr}(BCA)$$

I recently came across a wonderful tool to visualize these so-called tensor operations -- **factor graphs** -- that makes results such as the cyclic trace visually obvious. While I initially encountered factor graphs in the context of graphical models and message passing, I soon realized that they capture a more general and simpler concept. In this post, I'll mainly cover a high-level view of factor graphs without getting into the nitty-gritty details of graphical models or algorithms like message passing, which will be topics of discussion for future posts in this series.

Before we delve into factor graphs, let's run through a quick introduction to einstein summation notation.

# Einstein Notation
Numerous flavors of einstein notation exist, especially in physics, but the one which we'll deal with is very simple and easy to grasp without needing any physics background.

In the definition of matrix multiplication,

$$(A B)_{ij} = \sum_k A_{ik} B_{kj}$$

the summation symbol is actually redundant. We can just drop it and infer that the index $k$ must be summed over, because it does not appear on the left hand side.

$$(A B)_{ij} = A_{ik} B_{kj}$$

Why do this? Well, let's look at an example which has general _tensors_ (think numpy arrays with more than just 2 dimensions):

$$D_{kl} =  \sum_{j} \Big( \sum_{i} (A_{ijk} B_{ji}) C_{lj} \Big) \label{eq:normal}$$

And say that the tensors have the following shapes:

* $A \in \mathbb{R}^{10 \times 20 \times 100}$
* $B \in \mathbb{R}^{20 \times 10}$
* $C \in \mathbb{R}^{50 \times 20}$
* So $D$ would be in $\mathbb{R}^{100 \times 50}$

This is a pretty complex interaction of sums and products, and it gets quite cumbersome to constantly write summation symbols. Again, we don't need to write these summation symbols because we can imply which indices need to be summed over by looking at which indices appear only on the right side. In einstein notation, it's much cleaner:

$$D_{kl} =  A_{ijk} B_{ji} C_{lj}$$

But we did lose some information in this representation compared to equation $\ref{eq:normal}$ -- the order in which to compute the sums. Now, the order actually doesn't affect the final result (a la Fubini's theorem), but it turns out that some orderings can be computed more efficiently than others (more on this later). Also, you can easily play around with this in python using [`numpy.einsum`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.einsum.html). This [blog post](http://ajcr.net/Basic-guide-to-einsum/) provides a more detailed introduction to einsum with a bunch of nice examples.



# Factor Graphs

A general sum-product expression with multiple tensors of different sizes is called a _tensor network_. Apart from sounding fancy, the name is also justified, because any valid einstein sum you write can actually be mapped to a graph of tensors. (By valid, I mean that the size of the dimensions of different tensors with same indices must be equal).

We can build the graph pretty easily. Let's go back to the example and see what's going on (you can pause the visualizations if they seem too fast at first.)

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/IntroFG.mp4" type="video/mp4">
</video>


* The graph has two types of nodes - **factors** and **variables**.
  - We'll represent factors by squares, and variables by circles.
* Factors correspond to **Tensors** $(A, B, C)$
* Variables correspond to **Indices** $(i, j, k)$
* Edges occur only between squares and circles.
  - The rule for edges is simple -- **every factor is connected to each of its indices**. In the example above, $A_{ijk}$ means that $A$ is connected to $i,j$ and $k$.
  - The thickness of the edge corresponds to the size of the axis (or length of the array component) in the factor.
* This makes the graph a _bipartite graph_ between squares and circles.
* Indices that appear only on the right side of the equation ($i$ and $j$) are implicitly summed over. We'll represent this by darkening the corresponding variable node in the graph.

The last part of the animation above presents a **key intuition**:

Every factor graph has a fully _contracted_ state -- the right hand side of the einstein summation (the 2-d tensor D in the example). We can get this state by combining all the factors in the graph to one single factor, and then summing out each of the grayed variables. What's left is just a single factor connected to only the unsummed variables -- this is the contracted state. The green cloud transforming into the factor $D$ in the example demonstrates precisely this contraction.

Before we move on to exploring the power of this curious tool, a small aside on its origins:

### Why the name?

Well, for one, they are called factor graphs because the right hand side looks like a _factorization_ of the tensor on the left. This can be made more concrete in the context of probability distributions of discrete random variables. Tensors can represent **joint distributions** over different random variables if they are positive and sum to 1 (hence why the indices correspond to variables). In this setting, a factor graph is a factorization of a big joint over many variables into smaller joints over independent sets of variables.

Apart from appearing in probabilistic graphical models, factor graphs also show up in physics under the names _tensor network_ and _matrix product states_. However, I won't delve into the details of these applications in this particular post.

An important point to notice is that the factorization actually requires much lesser memory than the whole joint (compare storing a 10x10x10-tensor with three 10-dimensional vectors).


# Numpy Operations Visualized

Why is this representation useful? Well, it allows us to transform complicated factorizations into a more visual representation which is much easier to play around with. The numerous tensor operations in numpy can be neatly fit into this framework. A few self-explanatory examples are shown below:

## Matrix-Vector Multiplication

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/MatVec.mp4" type="video/mp4">
</video>

## Matrix-Matrix Multiplication

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/MatMul.mp4" type="video/mp4">
</video>

## Element-wise Product

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/Hadamard.mp4" type="video/mp4">
</video>

## Outer Product

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/OuterProduct.mp4" type="video/mp4">
</video>

## Trace

<video width="100%" controls="controls" loop autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/Trace.mp4" type="video/mp4">
</video>

Notice that a factor without any edges is a 0-d tensor, which is just a single number (as we would expect the trace to be).

<!-- ## Reshape -->


# Visual Proof

We can go beyond just understanding numpy operations and make short work of mathematical theorems using concise visual proofs. Here is a neat proof of the trace identity I mentioned in the beginning:

## Trace is Cyclic

<video width="100%" controls="controls" loop autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/TraceCyclic.mp4" type="video/mp4">
</video>

<!-- ## The Kron Property

Before we can prove this [property](), we need to look at how reshaping works in this framework.

## Reshape

<video width="100%" controls="controls" loop autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/Reshape.mp4" type="video/mp4">
</video>

Splitting one dimension into two dimensions is pretty straightforward, although the visualization does not offer too much insight per se. However, combining two dimensions into one can be done in a slightly different way:

<video width="100%" controls="controls" loop autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/ReshapeCombine.mp4" type="video/mp4">
</video>

This might look weird at first, and you might be wondering why I didn't just merge the indices $i$ and $j$ together. While that might be an accurate respresentation of how reshape works, it doesn't offer as much utility as this one. This view allows us to interpret this reshape as indexing the new, combined axis using the original two indices. It is basically a map from $(i, j)$ to the new axis index $k$, given by either $k = i + nj$ or $k = mi + j$ depending on if we performed column-major or row-major reshaping. -->

<!-- # Matrix factorizations
So far the operations we looked at just combined factors and variables to emulate mathematical operations. We can also split up factors into multiple factors through matrix factorizations.  -->

# Computational Cost of Tensor Contraction

So far we've been happily squishing those green clouds of the factor graph into one big factor without addressing how this transformation is actually computed. The process of combining a bunch of factors into one single factor and summing out the gray variables involves two basic computable operations:

* **Sum**: Remove a gray node which has only one edge
* **Product**: Combine two factors into one

It's easy to see that these operations preserve the final contracted state of the network, so if we can keep applying them until we end up with a single factor connected to only unsummed variables, we've contracted the network.

## Sum

The first operation, sum, is pretty self-explanatory. It's basically the `numpy.sum` operation applied on the corresponding axis. This involves summing tensors of size equal to the product of sizes of all other axes, and the number of these tensors is the size of the axis being summed. So the total number of additions is just the product of all the edge sizes. This can be gleaned from the visual representation as well:

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/SumVar.mp4" type="video/mp4">
</video>


## Product

The product operation is, in essence, a generalization of the outer product of two vectors to general tensors. In einstein notation, combining two factors amounts to treating two factors as one by multiplying their entries to get a bigger factor:

$$A_{ij} B_{kl} -> (AB)_{ijkl}$$

The product takes each element in one factor and multiplies it with a _whole_ copy of the other factor. So the size of the final result is the product of the total sizes of the individual factors, which is much larger. Each element of the final product is just the result of multiplying two numbers, so the total number of multiplications is the total number of entries in the final product. This is easy to visualize again:

<video width="100%" controls="controls" loop="loop" autoplay>
  <source src="{{site.baseurl}}/images/factor_graphs/mp4s-720p/CombineFactors.mp4" type="video/mp4">
</video>

Also, if two of the factors shared a variable, the two edges would be combined into a single one -- effectively performing a _diag_ operation akin to what happened in the trace animation.


When contracting a network, summing out variables and combining factors in different orders leads to different computational costs. It turns out that finding the optimal ordering for contracting a general factor graph to minimize the cost is actually NP-Hard. As a fun exercise, try to interpret the process of [_matrix chain multiplication_](https://en.wikipedia.org/wiki/Matrix_chain_multiplication) and understand how the total computational cost of finding a chain matrix product is affected by the multiplication order using the factor graph picture. This particular case has a neat dynamic programming algorithm that can obtain the optimal ordering in quadratic time.


Hopefully, I've now convinced you of the utility of factor graphs as a powerful visualization tool. We can go much further than just proving some nifty identities with them, and understand complex ideas like efficient methods for inference in probabilistic graphical models. Keep an eye out for upcoming posts in which I plan to discuss inference algorithms like the **sum-product** algorithm, **belief propagation** and **message passing** on trees using this visualization framework.

---

#### Some details

I lied a bit when I said that the factor graph is an exact representation of the einstein sum. The keen-eyed amongst you would have caught that we lose information about which axis of the tensor corresponds to which edge in the graph. However, this is easily remedied by just including an axis label for the edges coming out of each factor. But this makes the visualization unnecessarily cluttered and ugly, so I decided against including them.

Also, we can extend this visualization to networks that involve more than just summing variable nodes. Graying out a variable node effectively reduces the corresponding axis to a single number, so we can replace summation with any operation that performs such a reduction. For example, instead of summing, we could take the max across all elements in that axis, or simply index a particular position on the axis as well. This will become relevant when talking about _MAP estimation_ and _max-product belief propagation_. We can even extend this interpretation to the continuous domain and replace the summation with an integral, where now the factors are not discrete matrices but multivariable functions on a continuous domain.

---

I made the animations in this post using [manim](https://github.com/3b1b/manim), a math animation tool created by the amazing [3blue1brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw). I built a small library, [manimnx](https://github.com/rajatvd/manim-nx), on top of manim to help interface it with the graph package [networkx](https://networkx.github.io). You can find the code for the animations in this post [here](https://github.com/rajatvd/FactorGraphs).

I'd also like to thank my brother Anjan for the numerous back and forth discussions we had while I was creating this post.
