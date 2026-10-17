"""Generate Apple-style product illustration SVGs into images/."""
import os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def grad(gid, c1, c2, x2="1", y2="1"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


def shape(p, path, fill, extra=""):
    """A filled shape plus a soft glossy highlight."""
    return (f'<path d="{path}" fill="url(#{p}{fill})" {extra}/>'
            f'<path d="{path}" fill="url(#{p}hl)"/>')


def defs(p, main, dark):
    return (grad(f"{p}m", main, dark) +
            '<linearGradient id="%shl" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#fff" stop-opacity=".35"/>'
            '<stop offset=".45" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>' % p)


STITCH = 'fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="3" stroke-dasharray="8 7"'
LINE = 'fill="none" stroke="#000" stroke-opacity=".18" stroke-width="4" stroke-linecap="round"'


def shirt(p):
    body = "M250 300 L330 255 Q400 290 470 255 L550 300 L645 400 L592 455 L550 415 L550 770 Q400 785 250 770 L250 415 L208 455 L155 400 Z"
    return (shape(p, body, "m") +
            '<path d="M330 255 L400 335 L470 255 L448 244 L400 300 L352 244 Z" fill="#fff" fill-opacity=".85"/>'
            f'<path d="M400 335 V770" {LINE}/>' +
            "".join(f'<circle cx="412" cy="{y}" r="6" fill="#fff" fill-opacity=".9"/>' for y in (380, 460, 540, 620, 700)) +
            f'<path d="M290 360 h70 v70 q-35 10 -70 0 Z" {STITCH}/>')


def tee(p, dx=0, dy=0):
    body = "M262 300 L342 262 Q400 312 458 262 L538 300 L620 385 L570 435 L540 405 L540 770 Q400 782 260 770 L260 405 L230 435 L180 385 Z"
    return (f'<g transform="translate({dx} {dy})">' + shape(p, body, "m") +
            '<path d="M342 262 Q400 312 458 262" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="10"/></g>')


def tees(p):
    # three stacked tees in different colours
    out = ""
    for i, (c1, c2) in enumerate([("#cfd8e3", "#9aa9bd"), ("#2b2d33", "#121317"), ("#f4f1ea", "#d9d3c4")]):
        q = f"{p}t{i}"
        out += f"<defs>{defs(q, c1, c2)}</defs>" + tee(q, (i - 1) * 70, (i - 1) * -40 + 20)
    return out


def dress(p):
    body = "M340 225 L372 215 Q400 262 428 215 L460 225 L472 300 Q484 382 452 425 L565 830 Q400 875 235 830 L348 425 Q316 382 328 300 Z"
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" fill-opacity=".55"/>'
                   for x, y, r in [(370, 300, 9), (430, 340, 7), (390, 480, 11), (330, 600, 9), (450, 560, 10),
                                   (300, 760, 10), (400, 690, 8), (500, 760, 11), (460, 450, 6), (350, 400, 6)])
    return (shape(p, body, "m") +
            f'<clipPath id="{p}c"><path d="{body}"/></clipPath><g clip-path="url(#{p}c)">{dots}</g>'
            f'<path d="M328 300 Q400 420 470 300" {LINE}/>'
            f'<path d="M348 425 Q400 445 452 425" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="10"/>')


def sneaker(p):
    upper = "M165 640 Q170 525 255 505 L375 470 Q425 428 475 450 L525 520 Q610 535 648 580 Q668 605 655 640 Z"
    return (shape(p, upper, "m") +
            '<path d="M150 640 H668 Q680 640 676 664 L670 690 Q400 712 158 690 Q144 672 150 640 Z" fill="#fafafa"/>'
            '<path d="M150 668 Q400 690 676 668" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="4"/>'
            '<path d="M230 600 Q380 560 560 600 Q420 590 260 625 Z" fill="#fff" fill-opacity=".9"/>'
            + "".join(f'<path d="M{x} {y} l40 -14" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
                      for x, y in [(390, 500), (420, 520), (450, 540)]) +
            '<path d="M470 452 Q500 470 520 520" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="5"/>')


def tote(p):
    body = "M232 430 H568 L608 790 Q400 812 192 790 Z"
    return ('<path d="M300 440 Q300 255 400 255 Q500 255 500 440" fill="none" stroke="#5a3b26" stroke-width="22" stroke-linecap="round"/>'
            + shape(p, body, "m") +
            '<path d="M232 430 H568 L574 480 H226 Z" fill="#000" fill-opacity=".12"/>'
            f'<path d="M248 500 H552" {STITCH}/>'
            '<rect x="372" y="455" width="56" height="34" rx="8" fill="#e9c98a"/>')


def jacket(p, lapels=False):
    body = "M258 285 L338 250 Q400 280 462 250 L542 285 L622 365 L652 705 L592 715 L562 425 L562 755 Q400 770 238 755 L238 425 L208 715 L148 705 L178 365 Z"
    out = shape(p, body, "m")
    if lapels:
        out += ('<path d="M338 250 L400 470 L462 250 Z" fill="#f4f4f4"/>'
                '<path d="M338 250 L400 470 L360 300 L320 330 Z" fill="#000" fill-opacity=".25"/>'
                '<path d="M462 250 L400 470 L440 300 L480 330 Z" fill="#000" fill-opacity=".25"/>'
                '<path d="M388 262 L400 300 L412 262 Z" fill="#7a1f2b"/><path d="M394 300 L382 440 L400 465 L418 440 L406 300 Z" fill="#7a1f2b"/>'
                + "".join(f'<circle cx="400" cy="{y}" r="8" fill="#000" fill-opacity=".45"/>' for y in (540, 610)) +
                f'<path d="M290 600 h60" {LINE}/><path d="M450 600 h60" {LINE}/>')
    else:
        out += ('<path d="M338 250 L400 330 L462 250 L490 275 L400 365 L310 275 Z" fill="#000" fill-opacity=".18"/>'
                f'<path d="M400 365 V755" {LINE}/>'
                f'<path d="M280 410 h80 v70 h-80 Z" {STITCH}/><path d="M440 410 h80 v70 h-80 Z" {STITCH}/>'
                f'<path d="M238 700 H562" {STITCH}/>'
                + "".join(f'<circle cx="412" cy="{y}" r="7" fill="#d9b26b"/>' for y in (420, 500, 580, 660)))
    return out


def coord(p):
    top = "M300 245 L500 245 L522 425 Q400 440 278 425 Z"
    pants = "M290 455 H510 L545 860 H432 L400 575 L368 860 H255 Z"
    ribs = "".join(f'<path d="M{x} 250 V860" stroke="#000" stroke-opacity=".08" stroke-width="5"/>' for x in range(270, 540, 18))
    return (f'<path d="M318 245 L340 180 M482 245 L460 180" stroke="url(#{p}m)" stroke-width="12" stroke-linecap="round"/>'
            + shape(p, top, "m") + shape(p, pants, "m") +
            f'<clipPath id="{p}c"><path d="{top}"/><path d="{pants}"/></clipPath><g clip-path="url(#{p}c)">{ribs}</g>'
            '<rect x="290" y="455" width="220" height="26" fill="#000" fill-opacity=".14"/>')


def watch(p):
    return ('<rect x="338" y="170" width="124" height="660" rx="34" fill="#6b4a33"/>'
            '<rect x="338" y="170" width="124" height="660" rx="34" fill="url(#%shl)"/>' % p +
            "".join(f'<circle cx="400" cy="{y}" r="7" fill="#000" fill-opacity=".35"/>' for y in (720, 760, 800)) +
            '<rect x="545" y="478" width="30" height="44" rx="8" fill="#c9ccd2"/>' +
            shape(p, "M400 345 A155 155 0 1 1 399.9 345 Z", "m") +
            '<circle cx="400" cy="500" r="128" fill="#101215"/>'
            '<circle cx="350" cy="500" r="30" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="3"/>'
            '<circle cx="450" cy="500" r="30" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="3"/>'
            + "".join(f'<rect x="397" y="382" width="6" height="22" rx="3" fill="#fff" transform="rotate({a} 400 500)"/>' for a in range(0, 360, 30)) +
            '<path d="M400 500 L400 410" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
            '<path d="M400 500 L470 540" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
            '<path d="M400 520 L400 395" stroke="#ff7a45" stroke-width="3" stroke-linecap="round"/>'
            '<circle cx="400" cy="500" r="9" fill="#ff7a45"/>'
            '<path d="M290 410 A140 140 0 0 1 440 365" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="10" stroke-linecap="round"/>')


def mules(p):
    upper = "M175 600 Q185 455 335 448 Q432 458 445 600 Z"
    sole = "M160 600 H600 Q632 600 630 628 H572 V735 H498 V640 H196 Q160 640 160 600 Z"
    return (shape(p, sole, "m") + '<path d="M160 600 H630" stroke="#000" stroke-opacity=".15" stroke-width="6"/>'
            + f'<path d="{upper}" fill="#f2e6dc"/><path d="{upper}" fill="url(#{p}hl)"/>'
            f'<path d="M215 560 Q300 530 400 560" {LINE}/>'
            '<path d="M498 640 H572 V735 H498 Z" fill="#000" fill-opacity=".2"/>')


def sunglasses(p):
    left = "M200 470 Q198 420 285 418 L372 424 Q394 432 388 474 Q376 590 296 594 Q212 592 200 470 Z"
    right = "M600 470 Q602 420 515 418 L428 424 Q406 432 412 474 Q424 590 504 594 Q588 592 600 470 Z"
    frame = 'fill="none" stroke="#c8a24a" stroke-width="9"'
    return (shape(p, left, "m") + shape(p, right, "m") +
            f'<path d="{left}" {frame}/><path d="{right}" {frame}/>'
            f'<path d="M372 430 Q400 415 428 430" {frame}/><path d="M290 418 Q400 395 510 418" {frame}/>'
            '<path d="M200 455 L130 440 M600 455 L670 440" stroke="#c8a24a" stroke-width="9" stroke-linecap="round"/>'
            '<path d="M230 460 Q260 440 310 445" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="10" stroke-linecap="round"/>'
            '<path d="M440 460 Q470 440 520 445" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="10" stroke-linecap="round"/>')


def skirt(p):
    body = "M300 335 H500 L612 790 Q400 815 188 790 Z"
    pleats = "".join(f'<path d="M{300 + i * 25} 340 L{188 + i * 53} 795" stroke="#000" stroke-opacity=".14" stroke-width="5"/>' for i in range(1, 8))
    return (shape(p, body, "m") +
            f'<clipPath id="{p}c"><path d="{body}"/></clipPath><g clip-path="url(#{p}c)">{pleats}</g>'
            '<rect x="294" y="300" width="212" height="44" rx="10" fill="#000" fill-opacity=".25"/>'
            '<rect x="294" y="300" width="212" height="44" rx="10" fill="url(#%sm)" fill-opacity=".8"/>' % p)


# name: (drawer, product main, product dark, bg top, bg bottom)
ITEMS = {
    "linen-shirt": (shirt, "#e9dcc6", "#c2ab86", "#f7f2ea", "#e8dfd0"),
    "wrap-dress": (dress, "#ff7a94", "#d93a63", "#fff0f3", "#ffd9e1"),
    "running-sneakers": (sneaker, "#3d7bff", "#1c3fbf", "#eef3ff", "#d6e2ff"),
    "leather-tote": (tote, "#b07a4f", "#7a4b2a", "#faf3ec", "#efdfcf"),
    "denim-jacket": (lambda p: jacket(p), "#5b86c4", "#2f4f86", "#eef3fa", "#d5e1f1"),
    "knit-coord": (coord, "#c9b8a6", "#9d8670", "#f6f1ec", "#e6dcd1"),
    "chronograph-watch": (watch, "#e4e6ea", "#9fa4ad", "#f4f4f6", "#e1e2e6"),
    "crew-tees": (tees, "#999", "#666", "#f3f4f6", "#e2e5ea"),
    "block-mules": (mules, "#8a5a3c", "#5a3622", "#fbf1ea", "#f0dccd"),
    "aviator-sunglasses": (sunglasses, "#3a4a3f", "#121a15", "#f1f5f2", "#d9e4dc"),
    "wool-blazer": (lambda p: jacket(p, lapels=True), "#3b3f4a", "#1b1d23", "#f2f2f4", "#dcdde2"),
    "satin-skirt": (skirt, "#c8a7e8", "#8d62c2", "#f7f1fd", "#e7dbf6"),
}


def card_svg(name, draw, main, dark, b1, b2):
    p = "a"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" role="img" aria-label="{name.replace("-", " ")}">'
            f'<defs>{grad("bg", b1, b2, "0", "1")}{defs(p, main, dark)}'
            '<radialGradient id="sh"><stop offset="0" stop-color="#000" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
            '<rect width="800" height="1000" fill="url(#bg)"/>'
            '<ellipse cx="400" cy="880" rx="270" ry="34" fill="url(#sh)"/>'
            f'{draw(p)}</svg>')


for name, (draw, main, dark, b1, b2) in ITEMS.items():
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(card_svg(name, draw, main, dark, b1, b2))

# Wide editorial scene for the scroll-zoom section
scene = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Autumn collection">'
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1c14"/><stop offset=".55" stop-color="#7a3e1d"/><stop offset="1" stop-color="#d9823b"/></linearGradient>'
         '<radialGradient id="glow" cx=".7" cy=".3" r=".6"><stop offset="0" stop-color="#ffd59a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd59a" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="sh"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
         '<rect width="1600" height="1000" fill="url(#bg)"/><rect width="1600" height="1000" fill="url(#glow)"/>']
for i, (key, tx, ty, s) in enumerate([("denim-jacket", 120, 40, .95), ("wool-blazer", 560, -20, 1.0), ("leather-tote", 980, 180, .8),
                                       ("running-sneakers", 1060, 470, .75), ("aviator-sunglasses", 360, 520, .55)]):
    draw, main, dark, *_ = ITEMS[key]
    p = f"s{i}"
    scene.append(f'<g transform="translate({tx} {ty}) scale({s})"><defs>{defs(p, main, dark)}</defs>'
                 f'<ellipse cx="400" cy="880" rx="260" ry="30" fill="url(#sh)"/>{draw(p)}</g>')
scene.append('</svg>')
with open(f"{OUT}/autumn-scene.svg", "w") as f:
    f.write("".join(scene))

print("wrote", len(ITEMS) + 1, "files")
