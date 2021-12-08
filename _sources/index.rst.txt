Pygame Animated GIF Sprite
==========================

Simple usage
------------

To get started, install the package for your project

.. code-block:: console

   pip install pygame-animatedgif

To use the class in your project first import the corresponding class

.. literalinclude:: ../../example/example.py
   :lines: 1, 3

Now you can create instances of the animated sprites in the following way

.. literalinclude:: ../../example/example.py
   :dedent:
   :lines: 38

The first parameter given to the constructor are the x, y coordinates on
your `pygame` screen where the sprite should be placed. The second
parameter is a string giving the absolute or relative path to an animated
GIF file.

To automatically handle drawing of the sprite, it must be added to a
sprite group:

.. literalinclude:: ../../example/example.py
   :dedent:
   :lines: 47-48

And finally, in the main game loop you only need to take care of updating
drawing the sprite group once every frame.

.. literalinclude:: ../../example/example.py
   :dedent:
   :lines: 35-36, 55, 64-68

Complete API
------------
.. autoclass:: pygame_animatedgif.AnimatedGifSprite
   :members:
   :special-members: __init__

Acknowledgments
===============

 * RB[0] - `Original implementation <https://www.pygame.org/project/1039/1829>`_ of a Python class for animated GIFs
 * `Nick Sandau <https://github.com/nicksandau>`_ - Addition of several methods for a richer API in the `extended GIFImage class <https://github.com/nicksandau/GIFImage_ext>`_

Contents
========

:ref:`Keyword Index <genindex>`, :ref:`Search Page <search>`

.. toctree::
   :maxdepth: 2
   :caption: Contents:
