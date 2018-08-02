---
title: My projects
layout: page
permalink: /projects/
---

A list of some of the projects I have worked on previously:

## A Physics Simulation of gravitating particles in 2D

This is a simulation of 2D particles in a plane written in Java. The code can be found in the [repo](https://github.com/rajatvd/PhysicsSim). Click [here](https://rajatvd.github.io/PhysicsSim/PhysicsSim_v1.5.3.jar) to download the latest .jar executable. I also ported the Java app to a [web version](https://rajatvd.github.io/PhysicsSim/war/PhysicsSimWeb.html) with some small features omitted (like custom colors). Note that this port can be a bit buggy.

Some of the currently available features include: 

* Collision detection between spheres
* Gravitation between the particles
* Ability to change physical parameters like gravity strength and the restitution of collisions
* Ability to create particles of different masses and sizes
* Freezing of time

Instructions:

* To create a ball, press the left mouse button where you want to create it, and drag the mouse to define its velocity.
* Right click and drag to move the view, and use the mouse wheel to zoom in and out.
* Click the 'Lock Camera' button to be able to select a ball to lock the view onto.

### Some examples

* An ideal gas can be simulated by turning on the walls. Since the Kinetic theory of Gases models them as a collection of particles which only interact with each other through elastic collisions, Newton's Laws are sufficient to simulate ideal gases.

![ideal gas](/images/projects/idealGasPic.PNG)

* By turning off the walls, a simulation of many large bodies can be created. It is possible to make systems having planets with their own moons by careful placement of particles.

![three body](/images/projects/threeBody2.PNG)

By playing around with the parameters like gravity strength, restitution and using particles of different sizes and masses, you can create a lot of different interesting systems! For example, try to create a system which mimics the behaviour of particles in a crystal.

---

## Cryptanalysis of the Caesar and Vigenere ciphers

I analyse the Caesar and Vigenere ciphers, and explore methods of cracking them including frequency analysis and the [Kasiki examination](https://en.wikipedia.org/wiki/Kasiski_examination). The code was written in python using a jupyter notebook. You can find it in the repo [here](https://github.com/rajatvd/Cryptanalysis).

---
