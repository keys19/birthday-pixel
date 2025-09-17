# birthday-pixel
A CircuitPython light story told with a single on-board RGB NeoPixel!


The sequence lasts around 30 seconds to the familiar beats of a birthday:  
**match strike → candle flame while everyone sings → make-a-wish heartbeat → blowout + smoke → confetti burst → pastel “icing”.**

---

## Concept / Intention
I wished someone a happy birthday just before I began this assignment! The idea was to see if one pixel can convey that wish and emotion.  
The animation begins with a sharp yellow white spark as if a match is struck, then shifts to a warm orange flame that flickers while we would sing “Happy Birthday”.  
A soft pink pulse marks the moment of making a wish. The flame then swells and fades into smoky blue-gray, suggesting the candle being blown out.  
Finally, the pixel explodes into rapid rainbow flashes like confetti and lands on a sweep of pastel colors, echoing icing on a cake.

---

## Interesting Snippet
I used an easing helper to make fades feel natural. Instead of stepping linearly between two colors, the code eases in and out, like breathing. This makes swells, fades, and pulses feel more alive.

```python
def ease_in_out(t):               # 0..1 -> eased 0..1
    return 0.5 - 0.5*math.cos(math.pi*t)

def blending_rgb(a, b, u):           
    return (clamp8(a[0]+(b[0]-a[0])*u),
            clamp8(a[1]+(b[1]-a[1])*u),
            clamp8(a[2]+(b[2]-a[2])*u))

def fade_to(c0, c1, dur, steps=60):
    for i in range(steps+1):
        PIX[0] = lerp_rgb(c0, c1, ease_in_out(i/steps))
        PIX.show(); time.sleep(dur/steps)
```

## Reflection
While I’m satisfied with this first attempt at mapping familiar birthday moments to colors and timing i.e. the flame, the wish, the blowout, and the celebration, all with a single pixel, I’d like to push it further by experimenting with a wider palette and more carefully tuned timings to make the transitions feel even more natural. Looking ahead, I’d also love to sync the sequence with sound, so the light and audio work together. That would make the piece feel more complete and wholesome, like a true micro–birthday performance rather than just a visual sketch.

### Attribution
The code uses Adafruit’s NeoPixel CircuitPython API.
Requires neopixel.mpy and adafruit_pixelbuf.mpy in the lib/ folder on CIRCUITPY.
