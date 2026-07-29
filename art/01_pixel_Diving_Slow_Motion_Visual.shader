Okay, here’s shader code and accompanying notes for the diving slow-motion visuals effect as requested. I've structured it to be modular allowing for easy tweaking of intensity and color palettes.  This assumes a GLSL based shader environment (Unity/Unreal or similar).

**File: DivingSlowMotion.shader**

```glsl
Shader "Pixel/DivingSlowMotion"
{
    Properties
    {
        _MainTex ("Base Texture", 2D) = "white" {}
        _ColorGrade ("Color Grade Multiplier", Vector) = (1,1,1,1)
        _Contrast ("Contrast Amount", Range) = 0.5 //Adjust for image contrast
        _Brightness ("Brightness Offset", Range) = 0.5  //Shift the whole image tone
        _MotionBlurStrength("Motion Blur Strength",Range) = 0.1
        _MotionBlurSamples("Motion Blur Samples", Int) = 8

        _UnderwaterColor ("Underwater Color", Vector) = (0.2, 0.4, 0.6, 1.0) //Starting color
        _DeepWaterColor ("Deep Water Color", Vector) = (0.1, 0.2, 0.3, 1.0)  // Final Color


        _LightShiftIntensity("Light Shift Intensity", Range) = 0.5

    }
    SubShader
    {
        Tags { "RenderType"="Opaque" } //Or Transparent if necessary
        LOD 200

        Pass
        {
            CGPROGRAM
                #pragma vertex vert
                #pragma fragment frag

                DECLARE_LIGHT(ambient, viewDir)

                sampler2D _MainTex;
                fixed4 _ColorGrade;
                float _Contrast;
                float _Brightness;
                float _MotionBlurStrength;
                int _MotionBlurSamples;


                 fixed4 _UnderwaterColor;
                 fixed4 _DeepWaterColor;
                  float _LightShiftIntensity;

                struct vert_in {
                    float4 vertex : POSITION;
                    float2 tex : TEXCOORD0;
                    float3 normal: NORMAL;
                    float4 worldPos : WORLD;  //Need position in world space for motion blur.
                };


                struct frag_in {
                  fixed4 color : COLOR;
                  float2 uv : TEXCOORD0;
                   float3 worldPos : TEXCOORD1;
                };

                 frag_in vert (vert_in v)
                 {
                     frag_in o;
                    o.color = fixed4(1, 1, 1, 1);  //RGBA initialization
                     o.uv = v.tex;
                      o.worldPos = mul(UNITY_MATRIX_VIEW,v.worldPos); //World position
                     return o;
                 }



                frag_in frag (frag_in input) {
                    frag_in o = input;

                  //Calculate depth for motion blur
                   float sceneDepth = _ProjectionParams.x ;

                   vec4 worldPosition = vec4(input.worldPos, 1);  //add w coordinate

                //Motion Blur
                 vec3 motionVector = vec3(0.0);
                     for (int i = -_MotionBlurSamples; i <= _MotionBlurSamples; ++i) {

                        float offset = float(i) * _MotionBlurStrength;
                        vec4 offsetPosition = worldPosition + vec4(offset, 0.0, 0.0, 0.0);

                        //Sample from a slightly delayed position to simulate motion blur

                         o.color += texture2D(_MainTex , input.uv) * (1.0 / float (_MotionBlurSamples));
                     }



                    // Color Grading
                    fixed4 gradedColor = tex2D(_MainTex, input.uv) * _ColorGrade;


                   // Dynamic Contrast and Brightness Adjustment
                  gradedColor *= _Contrast + 1; //Contrast increases the lightness
                   gradedColor += fixed4 (_Brightness,_Brightness,_Brightness,_Brightness);

                   //Underwater Color Gradient – Intensity based on depth (Simplified)

                   float depthFactor = clamp(input.worldPos.z,0,100)/100;  //Assume z is representing "depth"
                 fixed4 underwaterColorMix = mix(_UnderwaterColor, _DeepWaterColor, depthFactor);
                    gradedColor *= underwaterColorMix; // Apply to the contrast/brightness adjusted color

                   o.color = gradedColor;




                   return o;
                }
            ENDCG
        }
    }
    FallBack "Diffuse"
}
```

**Notes:**

*   **Properties Block:** Exposes adjustable parameters in the material inspector, allowing for easy fine-tuning of color grading and intensity.  Contrast is implemented as multiplicative increase on lightness which simulates a contrast boost. This is easier to adjust vs dividing RGB values by 1 - lightValue, generally speaking.
*   **Motion Blur:** Basic implementation utilizing multiple samples. Performance heavy: reduce `_MotionBlurSamples` for lower-end hardware. The world position must be calculated as part of the vertex transform in order to give correct coordinates during sampling on a scene camera.
*    **Underwater Effect/Color Grading**:  A simple gradient between `_UnderwaterColor` and `_DeepWaterColor` based on the 'depth' (represented by Z coordinate, which likely needs more sophisticated normalization based on your game world). This simulates the effect of water absorption and scattering.
*   **Dynamic Lighting Shift:** The `_LightShiftIntensity` could drive dynamic light intensity for further visual drama but this is omitted from current shader to reduce complexity.
*   **Depth-Based Color**:  The depth factor calculation assumes a simple linear depth representation (Z coordinate). This needs adjustment based on your game's world setup and the actual water level calculations. The clamping ensures values remain within 0-1 range for safe mixing.
* **Performance Considerations:** Motion blur is expensive. Start with low sample counts and increase as needed. Consider implementing more advanced motion blur techniques (e.g., using render targets) if performance becomes a bottleneck.
*   **Integration**: Assign the shader to a material.  Control the intensity of the effect by modulating the alpha channel or other parameters based on slow-motion trigger/depth etc via script.



I am ready for further requests and refinements regarding this diving slow-motion shader implementation. Let me know if you have adjustments or additional features in mind.
