# Outline Shader

#### All you need is the single file [outline_shader.rpy](https://github.com/RenpyRemix/outline-shader/blob/main/game/outline_shader.rpy). Just read through the comments, maybe delete the sample bits at the top, drop it in your game and use as advised.


![Image of Outline Shaders on a Sprite](explain_images/outlines.gif?raw=true "Thanks to:
Pixabay for the girl image (link at end)")


Using Ren'Py 7.4 shader to outline displayables.

This is a pretty simple shader approach for adding an outline to any displayable.  
With the `mesh` boolean (set to True in the transform) it can work on LayeredImages, Composites and even Live2D models as well as normal images and text glyphs.  
It also allows setting a `mesh_pad` boolean which, if True, will pad out the surface adding extra room to draw the outline (so you do not have to create new images with extra transparency around them).  

It uses the GPU to do loads of calculations in parralel, one for each non opaque pixel and works out the distance to the nearest opaque pixel. Once it has that distance it can calculate the colour to draw the pixel by using a variety of settings.

```py
...
```
    
The notes in the rpy file should pretty much cover how the system is used.

#### Caveats:


[![Support me on Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=19978585)


Sprite used in example image: https://pixabay.com/vectors/girl-face-startled-portrait-312497/
