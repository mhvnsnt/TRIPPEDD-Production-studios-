ns = {'__name__': 'paintmod'}
for f in ['/tmp/paint_trio.py', '/tmp/paint_bg.py', '/tmp/paint_chars.py', '/tmp/paint_trio_main_clean.py']:
    exec(open(f).read(), ns)
exec("""
img = paint_background()
img.alpha_composite(paint_bubbles())
img.alpha_composite(paint_ricky())
img.alpha_composite(paint_julian())
img = grain(img, 5)
img.convert("RGB").save('/tmp/trio_v1.png')
print('saved /tmp/trio_v1.png')
""", ns)
