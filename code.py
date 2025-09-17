# # Birthday Pixel
# Scenes: strike -> candle (singing) -> wish -> blowout + smoke -> confetti -> icing 


import time, math, random
import board, neopixel

PIX = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.35, auto_write=False)

#helpers
def clamp8(x): return max(0, min(255, int(x)))
def scale(rgb, k): return (clamp8(rgb[0]*k), clamp8(rgb[1]*k), clamp8(rgb[2]*k))

def hsv_to_rgb(h, s, v):
    i = int(h*6); f = h*6 - i; i %= 6
    p = v*(1-s); q = v*(1-f*s); t = v*(1-(1-f)*s)
    if i==0: r,g,b=v,t,p
    elif i==1: r,g,b=q,v,p
    elif i==2: r,g,b=p,v,t
    elif i==3: r,g,b=p,q,v
    elif i==4: r,g,b=t,p,v
    else:      r,g,b=v,p,q
    return (clamp8(r*255), clamp8(g*255), clamp8(b*255))

def ease_in_out(t):  # 0..1 -> 0..1
    return 0.5 - 0.5*math.cos(math.pi*t)

def blending_rgb(a, b, u):
    return (clamp8(a[0]+(b[0]-a[0])*u),
            clamp8(a[1]+(b[1]-a[1])*u),
            clamp8(a[2]+(b[2]-a[2])*u))

def fade_to(c0, c1, dur, steps=60):
    for i in range(steps+1):
        PIX[0] = blending_rgb(c0, c1, ease_in_out(i/steps))
        PIX.show(); time.sleep(dur/steps)

#colors
DARK      = (0,0,0)
SPARK     = (255,255,200)          # match spark
FLAME_TOP = (255, 120, 30)   # bright orange flame
FLAME_CORE = (100, 80, 255)
SMOKE     = (110,140,160)          # cool gray-blue
GOLD      = (255,230,120)

# scenes
def scene_match_strike():
    # a pause, scratch (dark), spark, settle to flame with blue core flash
    PIX[0]=DARK; PIX.show(); time.sleep(0.25)
    PIX[0]=SPARK; PIX.show(); time.sleep(0.12)
    fade_to(SPARK, FLAME_TOP, 0.6)
    fade_to(FLAME_TOP, FLAME_CORE, 0.20)
    fade_to(FLAME_CORE, FLAME_TOP, 0.35)

def scene_singing_candle(seconds=9, jitter=0.2):
    #flicker while everyone sings
    t_end = time.monotonic() + seconds
    while time.monotonic() < t_end:
        k = 0.85 - random.random()*jitter  # 0.65..0.85
        PIX[0] = scale(FLAME_TOP, k)
        PIX.show(); time.sleep(1/28)

def scene_make_a_wish(seconds=4, cycles=2):
    # heartbeat pulse in pink to feel like “make a wish”
    base = (255,90,150)
    steps = 60
    per = seconds/(cycles*2*steps)
    for _ in range(cycles):
        for i in range(steps):   # up
            u = ease_in_out(i/steps)
            PIX[0] = scale(base, 0.55 + 0.45*u)
            PIX.show(); time.sleep(per)
        for i in range(steps):   # down
            u = ease_in_out(i/steps)
            PIX[0] = scale(base, 1.0 - 0.45*u)
            PIX.show(); time.sleep(per)
    # back to candle color before blow
    fade_to(PIX[0], FLAME_TOP, 0.5)

def scene_blowout_and_smoke():
    #breath-out to smoke and near-dark
    fade_to(FLAME_TOP, scale(FLAME_TOP, 1.05), 0.25)
    fade_to(scale(FLAME_TOP,1.05), scale(SMOKE,0.10), 1.7)
    # two wisps of smoke
    for k in (0.12, 0.07, 0.04):
        PIX[0] = scale(SMOKE, k); PIX.show(); time.sleep(0.25)
        PIX[0] = scale(SMOKE, k*0.4); PIX.show(); time.sleep(0.25)
    PIX[0]=DARK; PIX.show()

def scene_confetti_burst(seconds=3):
    # rapid bright shifts pops like confetti
    t_end = time.monotonic() + seconds
    while time.monotonic() < t_end:
        h = random.random()
        PIX[0] = hsv_to_rgb(h, 0.9, 1.0)
        PIX.show(); time.sleep(0.06)
        PIX[0] = DARK; PIX.show(); time.sleep(0.02)
    # gold sparkle tail
    for _ in range(10):
        PIX[0] = scale(GOLD, 1.0 if _%2==0 else 0.4); PIX.show(); time.sleep(0.08)

def scene_icing_finale(seconds=6):
    # soft pastel (icing colors: mint, sky, lavender, peach)
    pastels = [(170,255,230),(170,210,255),(210,170,255),(255,200,180)]
    steps = 80
    per = seconds/(len(pastels)*steps)
    c = pastels[0]
    for nxt in pastels[1:]+pastels[:1]:
        for i in range(steps):
            PIX[0] = blending_rgb(c, nxt, ease_in_out(i/steps))
            PIX.show(); time.sleep(per)
        c = nxt
    # fade to dark end
    fade_to(PIX[0], DARK, 0.8)

#timing
scene_match_strike()        # ~1.6 s
scene_singing_candle(9)     # 9 s
scene_make_a_wish(4,2)      # ~4 s
scene_blowout_and_smoke()   # ~3 s
scene_confetti_burst(3)     # 3 s
scene_icing_finale(6)       # ~6.8 s
