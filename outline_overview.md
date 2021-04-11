# This Outline Shader in Depth

So, this will be a rather vague `in Depth` overview because:  
1. Those who are using GLSL can probably suss out what is happening there.
1. The main useful stuff is just the variables that are passed in to the transform.
1. I want to move on to new things rather than explain this. 

The Shader part of the code basically iterates outward from each transparent pixel to find the nearest threshold opaque one. It then uses the distance, along with the passed in variables, to calculate a colour and opacity to draw the pixel. The passed in values allow the outline to have an antialias effect, use different colours for set parts and have defined curve boundaries.

The parameters for the transform are briefly explained as a comment block in the code...

```py

## This is the base transform
## You could either use this directly and pass in parameters as wanted
## or make transforms (with set parameters) to then call this (like below)
#
## width: the width of the outline area
## threshold: the minimum alpha level to count as opaque when finding 
##            the nearest opaque pixel
## color: the primary colour of the outline
## far_color: secondary colour
##            if set, this is the colour furthest from the image
## low_color: secondary colour
##            if set, this is the colour through the inner/outer steps
## low_color_fade: whether to fade the primary colour into the low_color
## step_start: proportion of the width to begin a smooth up-step at
##             (if this plus (1.0 - step_end) is less than 0.0 then no inner
##             step will be shown)
## step_end: proportion of the width at which to begin a smooth step-down
##           which will appear as a form of anti-aliasing
## mesh_pad: whether to pad out the image to make extra room for the outline
transform outline(
        width=10.0, 
        threshold=0.95, 
        color="#FFF", 
        far_color=None,
        low_color=None,
        low_color_fade=True,
        step_start=-0.25, 
        step_end=0.75,
        mesh_pad=True):
    mesh True
    mesh_pad (False if not mesh_pad else (int(width),) * 4)
    shader "remix.smoothstep_outline"
    u_width float(width)
    u_threshold float(threshold)
    u_step_start float(step_start)
    u_step_end min(1.0, max(0.0, float(step_end)))
    u_color Color(color).rgba
    u_far_color (Color(far_color).rgba if far_color else Color(color).rgba)
    u_low_color (Color(low_color).rgba if low_color else Color(color).rgba)
    u_low_color_fade (1.0 if low_color_fade else 0.0)
    u_mesh_pad (1.0 if mesh_pad else 0.0)
```
Some of these are self-explanatory to some level. I will expand on the comment descriptions anyway.  

#### `width` - the width of the outline area  
As the name implies, this is the pixel width of the outline area.

#### `threshold` - the minimum alpha level to count as opaque when finding the nearest opaque pixel  
When calculating the distance to nearest opaque pixel the system uses this value to determine if a found pixel is suitable. This would allow outlines on images that themselves were lower alpha (by setting this value to match). It also makes the internal logic easier as it only looks for ones above a certain level rather than trying to calculate whether opacity 0.88 at 11px distance is better or worse than 0.96 at 12px...  
Just set it to something a bit below the alpha level of the main image is best.

#### `color` - the primary colour of the outline  
As the comment says, this is the outline colour.

#### `far_color` - secondary colour - if set, this is the colour furthest from the image
With this set (to something different than `color`) the outline will use a gradient between the two colours, with the `color` colour being closest to the image.

#### `low_color` - secondary colour - if set, this is the colour through the inner/outer steps
With this set (to something different than `color`) the outline will use a different colour for the inner and outer edges where the step-up/down anti-aliasing occurs.  

#### `low_color_fade` - whether to fade the primary colour into the low_color
This True/False boolean controls how immediate the transition is between `color` and `low_color`.  
If you end up using these `low_` settings you might do best to tweak the actual shader itself and create a level that suits you best (as the setting is a bit clunky being just `on/off`)

#### `step_end` - proportion of the width at which to begin a smooth step-down which will appear as a form of anti-aliasing
To add a form of edge anti-aliasing, this value controls the point when smooth Hermite interpolation is used to reduce the alpha level of the outer edge of the outline. Pixels at a distance greater than this (as a 0.0 to 1.0 proportion of width) are reduced in opacity by using a smooth `S` curve.  

#### `step_start` - proportion of the width to begin a smooth up-step at (if this plus (1.0 - step_end) is less than 0.0 then no inner step will be shown)
Taking the width of the `step_end` value (if step_end was 0.8 it would have a width of 0.2 as it runs from itself up to 1.0) this setting controls where to place a mirrored step-up at for the inner edge of the outline. This allows outlines to start a little away from the image edge if desired.

#### `mesh_pad` - whether to pad out the image to make extra room for the outline
Utility setting so you do not have to add transparent borders to images (to make room for the added outline).  
Note: Positional settings for the image will Not take the extra padding into account (if you set the left edge of the image at 20px and use a 15px outline the left edge of that outline would end up being at 5px)
 
### Navigation:

Back to the main page [Home](README.md)

[Shaders Overview](https://github.com/RenpyRemix/outline-shader/blob/main/shader_overview.md)  
(this briefly covers how shaders work internally as well as some hints for writing shader code in Ren'Py)
