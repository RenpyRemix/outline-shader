# Outline Shader - Shaders Overview

If you have not encountered shaders in Ren'Py yet, there is documentation [Here](https://www.renpy.org/doc/html/model.html).  
This new features allows creation of GLSL code that is passed to the GPU to act upon a displayable. The main way of using them is to declare a shader by name within a normal transform. 

Creating your own shader is done through the `renpy.register_shader()` function which basically has parameters that can be used to pass in blocks of text...

```py
init python:

    renpy.register_shader("remix.smoothstep_outline",
        variables="""
// this section is to set up variable names 
        """,
        ## not using vertex code on this one
        vertex_300="""
        """,
        fragment_functions="""
# line 74 "outline_shader.rpy "

// this section can set up functions to use in the fragment section(s)
        """,
        fragment_300="""
# line 140 "outline_shader.rpy "

// the main fragment shader section (the _300 part is generally what you would use to indicate main)
        """)
```
Just blocks of text... variables, then vertex stuff, then fragment stuff... All just text, written in GLSL (which is similar to C, not Python)  

### Useful Little Trick  
Did you spot the 
```py

        fragment_functions="""
# line 74 "outline_shader.rpy "
```
bit?  
Adding a line like that is really helpful for debugging as it can allow any reported error to also indicate the filename and line. Obviously you do have to write the actual line number there... Then if an error occurs 10 lines further down it would say `Error (outline_shader.rpy 84)` or somesuch, pointing you to where you need look.


## The Process (a simplified example)
#### (Note: this does not reflect the approach used for the Outline Shader)

In order to maintain some structure here, I will detail the standard process in a chronological order (that does not reflect the outline shader file).  

So, let's start with a displayable shown with a transform:
```py
label x:
    show eileen at outline
    pause
```
All very straight-forward, so next our simplified transform:  
```py
transform outline(width=3.0, color="#FFF"):
    mesh True
    shader "remix.simple_shadow_example"
    u_width float(width)
    u_color Color(color).rgba
```
As you can see, it is very similar to normal transforms. We give it a name and pass in a couple of parameters by name with default values.  
The differences start once we are inside...  
Firstly we have `mesh True` which at a basic level flattens the displayable so our shader can work on it as a whole rather than running once per part of it.  
Then we tell it the shader to use with `shader "remix.simple_shadow_example"`. Convention in shader naming is to use prefix dot name.  
The next two lines both declare a variable to use inside the shader. Here we use the `u_` prefix to denote a `uniform` value. The values of each are coerced to a format usable inside a shader, float for the width (though it could easily be int) and a four part float for colour using the `Color().rgba` property.

Those variables with the `u_` prefix are now passed into the shader defined as shown at the top...
```py
init python:

    renpy.register_shader("remix.simple_shadow_example",
        variables="""
uniform float u_width;
uniform vec4 u_color;
```
That names the shader and scopes the two uniforms for use inside other parts...  

There are also quite a few inbuilt variales that can be accessed within shaders. These cover things such as the current position, textures and texture sizes and others. These are detailed in the Ren'Py documentation.  

... in that section we also declare the inbuilt variables we want to use...
```py
uniform vec2 u_model_size;
uniform sampler2D tex0;
varying vec2 v_tex_coord;
        """,
```

Within the vertex or fragment sections we would now have access to those variables...
```py
        fragment_300="""
vec2 pixel_size = (vec2(1.) / u_model_size);
vec2 offset_pos = v_tex_coord.xy - (vec2(u_width) * pixel_size);

if (gl_FragColor.a < 0.98) {
    if (texture2D(tex0, offset_pos).a >= 0.02) {
        gl_FragColor = u_color;
    }
}
        """)
```
(not really an example you would want to use in a game)

Almost everything within a shader is based upon a float value between 0.0 and 1.0.  
This includes colours (0.2, 0.6, 0.8, 1.0) rgba values rather than say "#3399CCFF" and positions (0.5, 0.5) rather than pixel (100, 100).  

Our horrible little example script there wants to add a dropshadow of size `u_width` drawn in colour `u_color`.  
As we passed in the width as a pixel value we first want to determine what each pixel is as a float of the full image size. So we just divide 1.0 by how many pixels wide and divide 1.0 by how tall the image is.  
Now we can multiply those by the passed in width to get an offset (say (0.014, 0.018)) and minus that from the position of the current pixel.  

The fragment shader here is effectively running once for each pixel in the image, just is it doing loads of those similar calculations at the same time in parallel.  
Therefore, when we use `v_tex_coord` we are getting the position of just the pixel we are working on. Our line calculating offset_pos is taking that position and moving `width` pixels left and `width` pixels upwards, calculated as two floats relative to the texture.

The conditional block after that is then doing:
```py
if the current pixel is not opaque:
    test the alpha level of the pixel up-and-left from current pixel
    if that offset pixel is opaque:
        recolour the current pixel to be the colour we set
```
Very basic, rather simple and not at all like the approach used in the Outline Shader.

There are a huge number of resources online for learning about GLSL.  
This page is just to give a few pointers about how they are done within Ren'Py.
    

### Navigation:

Back to the main page [Home](README.md)

[This Outline Shader](https://github.com/RenpyRemix/outline-shader/blob/main/outline_overview.md)  
(this goes into more depth to explain this shader in particular)
