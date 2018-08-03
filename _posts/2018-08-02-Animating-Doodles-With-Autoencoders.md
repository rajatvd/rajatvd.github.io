---
layout: post
title: Animating Doodles with Autoencoders and Synthetic Data
watch: true
excerpt:  I train autoencoders to identify components of doodles using a synthetic dataset, and use them to create nifty animations by interpolating in latent space.
image: 
    path: /images/anim_dood/danceman_brownian_std1.2.gif
    width: 25%
comments: true

---

<figure style="margin: 20px auto; text-align: center;">
    <img src='/images/anim_dood/danceman_brownian_std1.2.gif' alt='dance dance' width='25%' style='margin:20px auto; display:inline-block' text-align='center'/>
</figure>

In this post, I'm going to go over a recent project of mine in which I trained some autoencoders on synthetic data created by randomly painting lines and curves on an image. I also created a bunch of animations by interpolating in latent space between some of my crudely drawn doodles. I tried out different interpolation methods to make various types of animations.

# The Synthetic Dataset

The dataset I trained the autoencoders on was a synthetic dataset, which means that the data is programmatically created. This type of dataset is different from normal datasets in that it isn't collected or annotated in anyway. In essence, the dataset is created in the computer itself. The particular synthetic dataset I used consisted of grayscale images (64x64) with random lines, curves and ellipses painted on it. A random number of each of the shapes are painted with random attributes:

* Lines - random endpoints.
* Bezier curves - random endpoints and anchor point.
* Ellipses - random centres, rotation and eccentricity.

Each of the shapes is also painted with a random stroke width. Here are some samples from the dataset:

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/sample_dataset.png' alt='sample from dataset' width='80%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>Some sample images from the synthetic dataset. Note the variation in number of strokes, stroke width and types of strokes. The vast number of possibilities makes the size of this dataset huge.</figcaption>
</figure>


# The Autoencoder
The first model I trained used a convolutional encoder and decoder with residual connections. The networks were fairly deep with around 20 conv layers for both the encoder and decoder. I experimented with different sizes for the latent space encoding, and ended up using 64. The model performed pretty well, here are some inputs and outputs:

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/convconv_sample.png' alt='convconv sample' width='80%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>Input images (top) and the corresponding reconstructions (bottom) made using an autoencoder with conv layers and residual connections. We can see that the reconstructions fail to capture finer details, and are also more blurred out compared to the inputs. However, they manage to recognize many of the strokes correctly.</figcaption>
</figure>

I also tried out the CoordConv layer described in this [paper](https://arxiv.org/abs/1807.03247). It basically just adds a meshgrid of $x$ and $y$ coordinates as 2 more channels in the input image. This adds a spatial bias to the conv layer. I couldn't find much quantitative difference in terms of training speed or final performance, and nor could I notice much qualitative changes in the outputs:

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/coordconv_sample.png' alt='coordconv sample' width='80%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>Input images (top) and the corresponding reconstructions (bottom) made using an autoencoder with CoordConv layers. Similar problems as the previous case exist, as it fails to reconstruct finer details in crowded parts of the input image.</figcaption>
</figure>

# Interpolation and Animation

Now for the fun bit. Using the autoencoder I just described above, I interpolated between some doodles I drew up in paint. The process is quite simple:

* Given a sequence of grayscale images, pass each of them through the encoder of the trained autoencoder.
* Linearly interpolate between the encodings of each image sequentially.
* Apply the decoder on each of the interpolated points and string together the resulting images to form an animation between the input images.

This produces interesting animations which pay attention to the characteristics of strokes and curves in the images. Here is one such animation which shows a tree-like structure growing from a point. 


<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/tree.bmp' alt='tree images' width='60%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/tree_brownian_std0.gif' alt='tree interp 0 std' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>The input sequence of images of a growing tree-like structure, and the resulting animation obtained by interpolating between them in latent space. Note that the reconstructions aren't perfect, with some of the finer details missing.</figcaption>
</figure>


Apart from a basic linear interpolation, I also tried to use a _circular_ interpolation. This is done by first linearly interpolating between the euclidean norms of the two encodings to get a set of interpolating norms. Then, each of the vectors obtained by normal linear interpolation between the two encodings are scaled to have norms equal to these corresponding norms. It turned out that this didn't make much of a difference. Another interpolation method which produced better qualitative results involved adding some randomness to the process.

## Brownian Bridge Interpolation

I added a _brownian bridge_ to the path obtained by linearly interpolating between two encodings. A brownian bridge is a random walk which starts and ends at the same value (in this case, $0$). A simple way to generate a brownian bridge is as follows:

* Generate a gaussian random walk. Let's call this sequence of vectors $X_t$, where $0 \leq t \leq 1$ is the time index of the points in the walk.
* To make the brownian bridge $Y_t$, we just do the following:

$$Y_t = X_t - t X_t$$

Now that we got a random walk beginning and ending with 0, we can add this to each of the interpolating paths between the input images. Here's the same tree animation as above, with added brownian bridges using different standard deviations for the random walks:

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/tree_brownian_std0.3.gif' alt='tree std 0.3' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/tree_brownian_std1.3.gif' alt='tree std 1.3' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>Animations obtained by adding brownian bridges of standard deviations 0.3 (left) and 1.3 (right) to the interpolating paths in latent space.</figcaption>
</figure>

The added noise in the interpolating paths manifests as shaky animations as opposed to noise in the actual image. The encoding in the latent space is sort of a compressed representation of the input image, with information about the curves and strokes in the image. So, adding noise to this encoding will result in perturbations in properties of the lines and curves, making them look shaky.  Qualitatively, these animations seem a bit more realistic than the plain linear interpolations.

Here are some more animations I made and their corresponding input image sequences. Compare the ones with and without the added brownian bridge.

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/jumpingjack.bmp' alt='jj images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/jumpingjack_brownian_std0.gif' alt='jj std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/jumpingjack_brownian_std1.3.gif' alt='jj std 1.3' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    
    <figcaption>Input images for a jumping jack animation. The animation clearly shows upward motion as the stick figure jumps.</figcaption>
</figure>

---

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/makeman.bmp' alt='man images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/makeman_brownian_std0.gif' alt='man std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/makeman_brownian_std0.8.gif' alt='man std 0.8' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>Creating a stick figure from a point. The brownian bridge noise really makes the animation more interesting as the one without noise (left) seems too artificial.</figcaption>
</figure>

---

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/rotatesquare.bmp' alt='sq images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/rotatesquare_brownian_std0.gif' alt='sq std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/rotatesquare_brownian_std1.2.gif' alt='sq std 1.2' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>If the input images are sufficiently close together, objects can also be made to rotate.</figcaption>
</figure>

---

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/brain.bmp' alt='brain images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/brain_brownian_std0.gif' alt='brain std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/brain_brownian_std1.0.gif' alt='brain std 1.2' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>The autoencoder can successfully reconstruct English alphabet as well. This can be used to make animated words like this one.</figcaption>
</figure>

---

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/neuron.bmp' alt='neuron images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/neuron_brownian_std0.0.gif' alt='neuron std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/neuron_brownian_std0.8.gif' alt='neuron std 1.2' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>The interpolations between some of the letters are quite interesting.</figcaption>
</figure>

---

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/danceman.bmp' alt='dance images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/danceman_brownian_std0.gif' alt='dance std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/danceman_brownian_std1.2.gif' alt='dance std 1.2' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>A dancing stick figure.</figcaption>
</figure>

---

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/walker2.bmp' alt='walk images' width='70%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/walker2_brownian_std0.gif' alt='walk std 0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/walker2_brownian_std1.0.gif' alt='walk std 1.0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>My crude attempt at trying to make a stick figure walk. Seems more like a dance move though.</figcaption>
</figure>

The above animations look pretty realistic, but the reconstructions are far from perfect. Training an autoencoder with a different architecture could possibly make them sharper and more accurate. It would also be interesting to use other types of models like disentangled VAEs to try to extract meaningful features out of the learned encodings like stroke width, curve position, etc.

This fun little project goes to show that you can use deep learning to make cool stuff even if you don't have a dataset to play with - just make your own! 

# Cubic Spline Interpolation
_Addendum on Aug 4_

Some of you suggested to try out higher order interpolation techniques as they might result in smoother animations. Indeed this is a great idea, so I went ahead and made some gifs using _cubic spline_ interpolation. Here are some of the gifs with the linearly interpolated ones as well for comparison:


<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/danceman_brownian_std1.2.gif' alt='dance std 1.2' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/danceman_cubic_std0.5_20frames.gif' alt='dance cube 0.5' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>The gif created using cubic spline interpolation (right) seems smoother compared to the one on the left.</figcaption>
</figure>

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/jumpingjack_brownian_std1.3.gif' alt='jj std 1.3' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/jumpingjack_cubic_std1.0_20frames.gif' alt='jj cube 1.0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
</figure>

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/walker2_brownian_std1.0.gif' alt='walker std 1.0' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/walker2_cubic_std0.8_20frames.gif' alt='walker cube 0.8' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <figcaption>Although the differences in the above examples are much more subtle and hard to make out.</figcaption>
</figure>

<figure style="margin: 20px auto; text-align: center; width:100%" vertical-align='middle'>
    <img src='/images/anim_dood/neuron_brownian_std0.8.gif' alt='neuron std 0.8' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    <img src='/images/anim_dood/neuron_cubic_std0.8_100frames.gif' alt='dance cube 0.5' width='20%' style='margin:20px 3%; display:inline-block' text-align='center' vertical-align='middle'/>
    
    <figcaption>It's almost the same in the case of letters as well.</figcaption>
</figure>

---
You can find my code for this post [here](https://github.com/rajatvd/AutoencoderAnim). It's written using pytorch, with the aid of some [utils](https://github.com/rajatvd/PytorchUtils) I made. Special thanks to my brother Anjan for the discussions we had about the ideas in this post.