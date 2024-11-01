import re
import sys

def read_svg(fname):
    with open(fname, "r") as f:
        data = f.read()

    m = re.search(r"d=\"m (.*)\"", data)
    xs = []
    ys = []
    pen = (0, 0)
    if m:
        tokens = m.group(1).split()
        mode = "m"
        hoffset = 0
        voffset = 0
        ci = 0
        for token in tokens:
            if token in ["m", "h", "v", "l", "c"]:
                mode = token
                continue
            else:
                if mode in ["m", "l"] or (mode == "c" and ci == 2):
                    cs = token.split(",")
                    x = float(cs[0]) + hoffset
                    y = float(cs[1]) + voffset
                    pen = (pen[0] + x, pen[1] + y)
                    xs.append(pen[0])
                    ys.append(pen[1])
                    print(pen)
                elif mode == "h":
                    pen = (pen[0] + float(token), pen[1])
                elif mode == "v":
                    pen = (pen[0], pen[1] + float(token))
                if mode == "c":
                    ci = (ci + 1) % 3
    return (xs, ys)

def get_osc_points(fname):
    (xs, ys) = read_svg(fname)

    # Normalize xs and ys
    min_x = min(xs)
    min_y = min(ys)
    xs = [x - min_x for x in xs]
    ys = [y - min_y for y in ys]
    max_x = max(xs)
    max_y = max(ys)
    xs = [x / max_x for x in xs]
    ys = [y / max_y for y in ys]
    # Invert
    ys = [1 - y for y in ys]

    return (xs, ys)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    (xs, ys) = read_svg(sys.argv[1])
    plt.plot(xs, ys)
    plt.savefig("plot.png")
