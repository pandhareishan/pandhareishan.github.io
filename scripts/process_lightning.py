from PIL import Image, ImageSequence
from pathlib import Path

src = Path('/Users/ishanpandharework/Downloads/Github Portfolio/images/Lightning.gif')
out = Path('/Users/ishanpandharework/Downloads/Github Portfolio/images/lightning-horizontal.gif')

im = Image.open(src)
frames = []
frame_durations = []

bbox_union = None
for frame in ImageSequence.Iterator(im):
    rgba = frame.convert('RGBA')
    mask_data = []
    for r, g, b, a in rgba.getdata():
        if a == 0 or max(r, g, b) <= 20:
            mask_data.append(0)
        else:
            mask_data.append(255)
    mask = Image.new('L', rgba.size)
    mask.putdata(mask_data)
    bbox = mask.getbbox()
    if bbox:
        if bbox_union is None:
            bbox_union = list(bbox)
        else:
            bbox_union[0] = min(bbox_union[0], bbox[0])
            bbox_union[1] = min(bbox_union[1], bbox[1])
            bbox_union[2] = max(bbox_union[2], bbox[2])
            bbox_union[3] = max(bbox_union[3], bbox[3])

if not bbox_union:
    raise SystemExit('No non-black pixels found')

pad = 12
bbox_union = (
    max(0, bbox_union[0] - pad),
    max(0, bbox_union[1] - pad),
    min(im.size[0], bbox_union[2] + pad),
    min(im.size[1], bbox_union[3] + pad),
)

for frame in ImageSequence.Iterator(im):
    duration = frame.info.get('duration', 50)
    rgba = frame.convert('RGBA')
    data = []
    for r, g, b, a in rgba.getdata():
        if max(r, g, b) <= 20:
            data.append((0, 0, 0, 0))
        else:
            data.append((r, g, b, a))
    rgba.putdata(data)
    cropped = rgba.crop(bbox_union)
    rotated = cropped.rotate(90, expand=True)
    frames.append(rotated)
    frame_durations.append(duration)

frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=frame_durations,
    loop=0,
    disposal=2,
)

print(f'Saved {out}')
