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
##             if this plus (1.0 - step_end) is less than 0.0 then no inner
##             step will be shown
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

 
### Navigation:

Back to the main page [Home](README.md)

[Shaders Overview](https://github.com/RenpyRemix/outline-shader/blob/main/shader_overview.md)  
(this briefly covers how shaders work internally as well as some hints for writing shader code in Ren'Py)
