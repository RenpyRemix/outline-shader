# Outline Shader

#### All you need is the single file [outline_shader.rpy](https://github.com/RenpyRemix/outline-shader/blob/main/game/outline_shader.rpy). Just read through the comments, maybe delete the sample bits at the top, drop it in your game and use as advised.


![Image of Outline Shaders on a Sprite](explain_images/outlines.gif?raw=true "Thanks to:
Pixabay for the girl image (link at end)")


Using Ren'Py 7.4 shader to outline displayables.

This is a pretty simple shader approach for adding an outline to any displayable.  
With the `mesh` boolean (set to True in the transform) it can work on LayeredImages, Composites and even Live2D models as well as normal images and text glyphs.  
It also allows setting a `mesh_pad` boolean which, if True, will pad out the surface adding extra room to draw the outline (so you do not have to create new images with extra transparency around them).  

It uses the GPU to do loads of calculations in parallel, one for each non opaque pixel and works out the distance to the nearest opaque pixel. Once it has that distance it can calculate the colour to draw the pixel by using a variety of settings.  
With all these being in parralel it only takes a fraction of the time that an approach like this would require if done on the CPU. This makes it pretty acceptable to use during run-time as it should not add lag spikes, especially if mostly used for smaller images such as buttons.  

The end of the rpy file has the base transform as well as a couple of example transforms that then use the base one inside them.  
You could use them when showing images (as in the example label) using the `at` keyword to dictate a transform or use the `At()` wrapper function when defining or declaring an image.
```py
        imagebutton:
            idle "images/button.png"
            hover At("images/button.png", coloured_outline)
            action NullAction()
```
Alternatively, you could even write transforms especially for the buttons and include event triggers within them such as `on hover:` that then used the shader.
    
The notes in the rpy file should pretty much cover the basics of how the system is used.

### Navigation:

[Shaders Overview](https://github.com/RenpyRemix/outline-shader/blob/main/shader_overview.md)  
(this briefly covers how shaders work internally as well as some hints for writing shader code in Ren'Py)

[This Outline Shader](https://github.com/RenpyRemix/outline-shader/blob/main/outline_overview.md)  
(this goes into more depth to explain this shader in particular)


[![Support me on Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=19978585)


Sprite used in example image: https://pixabay.com/vectors/girl-face-startled-portrait-312497/

### Please note:

The way that some parts of this approach work might not be suitable for complete beginners. As such it will likely require some knowledge of Ren'Py in order to extend it to your particular needs. 

Though I have tried to explain it as simply as possible, I will not be available to help extend it unless under a paid contract.
Basically, if you want it to do more, you are expected to know enough Ren'Py to handle that yourself (or consider paying someone)
