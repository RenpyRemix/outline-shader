## To view example in your game add
##
##  call outline_example
##
## somewhere in your running label script



            ###########################################
            #                                         #
            #           To use in your game           #
            #                                         #
            #   Make sure the Python stuff and the    #
            #   transform are available (basically,   #
            #   just do not delete them)              #
            #   Then just do similar to the example   #
            #   usage below                           #
            #                                         #
            ###########################################

# You may need to allow gl2 to operate by setting the config
define config.gl2 = True

label outline_example:

    scene expression "#456"

    ### girl.png is https://pixabay.com/vectors/girl-face-startled-portrait-312497/

    show girl at outline():
        xcenter 0.38
        ycenter 0.4
    pause 1.0

    show girl as girl2 at coloured_outline():
        xcenter 0.5
        ycenter 0.4
    pause 1.0

    show girl as girl3 at animated_outline():
        xcenter 0.64
        ycenter 0.4
    pause

    hide girl
    hide girl2
    hide girl3

    return


init python:

    renpy.register_shader("remix.smoothstep_outline",
        variables="""
uniform vec2 u_model_size;
uniform float u_lod_bias;
uniform sampler2D tex0;
varying vec2 v_tex_coord;

uniform float u_threshold;
uniform float u_width;
uniform float u_step_start;
uniform float u_step_end;
uniform vec4 u_color;
uniform vec4 u_far_color;
uniform vec4 u_low_color;
uniform float u_low_color_fade;
uniform float u_mesh_pad;
        """,
        vertex_300="""
        """,
        fragment_functions="""
# line 74 "outline_shader.rpy "

// given a 0.0 to 1.0 distance, return alpha based on smoothstep values
float get_step_alpha(float d, float s, float e)
{
    return smoothstep(s, s + 1.0 - e, d) * (1.0 - smoothstep(e, 1.0, d));
}

bool find_opaque(float x, float y, vec2 pos, vec2 pxo, float lod, sampler2D tex0, float threshold) {
    // x,y
    if (texture2D(tex0, clamp(pos + pxo, 0.0, 1.0), lod).a >= threshold) {
        return true;
    }

    // -x, y (if x is not 0)
    if (x > 0.1) {
        if (texture2D(tex0, clamp(pos + vec2(-pxo.x, pxo.y), 0.0, 1.0), lod).a >= threshold) {
            return true;
        }
    }

    // x, -y (if y is not 0)
    if (y > 0.1) {
        if (texture2D(tex0, clamp(pos + vec2(pxo.x, -pxo.y), 0.0, 1.0), lod).a >= threshold) {
            return true;
        }

        // -x, -y (if both x and y not 0)
        if (x > 0.1) {
            if (texture2D(tex0, clamp(pos - pxo, 0.0, 1.0), lod).a >= threshold) {
                return true;
            }
        }
    }
    return false;
}

float opaque_distance(vec2 pos, float lod, sampler2D tex0, float threshold, 
                      float u_width, vec2 pixel_size, float max_dist) {
    float nearest = 0.0;
    for (float x = 1.0; x <= u_width; x += 1.0) {
        float x_dist = pow(x, 2);
        for (float y = 0.0; y <= x; y += 1.0) {
            float d = pow(y, 2) + x_dist;
            if (nearest > 0.1) max_dist = nearest;
            if (d > max_dist) break;

            vec2 pxo = vec2(x, y) * pixel_size;
            // best of the four pixels (-x, y), (x, y), (-x, -y), (x, -y)
            if (find_opaque(x, y, pos, pxo, lod, tex0, threshold)) {
                nearest = d;
            }

            if (x > y) {
                vec2 pyo = vec2(y, x) * pixel_size;
                // best of the four pixels (-y, x), (y, x), (-y, -x), (y, -x)
                if (find_opaque(y, x, pos, pyo, lod, tex0, threshold)) {
                    nearest = d;
                }
            }
        }
    }
    return nearest;
}
        """,
        fragment_300="""
# line 140 "outline_shader.rpy "

vec2 padded_size = u_model_size;
if (u_mesh_pad > 0.5) padded_size += vec2(u_width) * 2;

vec2 pos = v_tex_coord.xy;
vec2 pixel_size = (vec2(1.) / padded_size);

float max_dist = pow(u_width, 2);

// only want outlines where the image is part or fully transparent
if (gl_FragColor.a < 0.98) {
    // the square distance of nearest threshold alpha pixel
    float near = opaque_distance(pos, u_lod_bias, tex0, u_threshold, 
                                 u_width, pixel_size, max_dist);
    if (near > 0.1) {
        // Now we can do the sqrt
        float dist = sqrt(near) / u_width;
        float color_dist = (dist - u_step_start) / (u_step_end - u_step_start);
        vec4 color = mix(u_color, u_far_color, color_dist);
        float alpha = get_step_alpha(dist, u_step_start, u_step_end);
        if (u_low_color != u_color && alpha < 0.99) {
            color = (u_low_color_fade > 0.5) ? 
                mix(u_low_color, color, clamp(alpha * alpha, 0.0, 1.0)) : 
                u_low_color;
        }
        alpha *= u_color.a;
        // this pixel should be altered
        if (gl_FragColor.a > 0.05 && alpha > 0.05) {
            // some edge pixel that has some opacity
            gl_FragColor = vec4(
                mix(color.rgb, 
                    gl_FragColor.rgb, 
                    gl_FragColor.a / (gl_FragColor.a + alpha)), 
                1.0) * (1.0, 1.0, 1.0, max(alpha, gl_FragColor.a));
        } else {
            gl_FragColor = vec4(color * (1.0, 1.0, 1.0, alpha));
        }
    }
}
        """)

## This is the base transform
## You could either use this directly and pass in parameters as wanted
## or make transforms (with set parameters) to then call this (like below)
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

## This one just uses other colour values
transform coloured_outline():
    outline(
        width=25.0, 
        color="#0EC04D", 
        far_color="#074621",
        low_color="#FFF",
        low_color_fade=False,
        step_start=0.1, 
        step_end=0.7,
        mesh_pad=True)

## A little bit of animation on the width and step distances
transform animated_outline():
    outline(
        width=15.0, 
        color="#FFF",
        step_start=0.4, 
        step_end=0.8)
    linear 1.5 u_width 0.0 u_step_start -0.2
    linear 1.5 u_width 15.0 u_step_start 0.4
    repeat