# Outline Shader - System Overview

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

Did you spot the 
```py

        fragment_functions="""
# line 74 "outline_shader.rpy "
```
bit?  
Adding a line like that is really helpful for debugging as it can allow any reported error to also indicate the filename and line.


### Navigation:

Back to the main page [Home](README.md)
