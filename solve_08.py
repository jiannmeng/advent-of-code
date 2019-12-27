with open("input_08.csv", "r") as file:
    img_data = [int(x) for x in file.read()]

# Split the data into layers:
PIXELS_PER_LAYER = 25 * 6
NUM_LAYERS = len(img_data) // PIXELS_PER_LAYER
img_layers = [
    img_data[PIXELS_PER_LAYER * i : PIXELS_PER_LAYER * (i + 1)]
    for i in range(NUM_LAYERS)
]

zeroes = [layer.count(0) for layer in img_layers]
fewest_zeroes_layer = img_layers[zeroes.index(min(zeroes))]
part1 = fewest_zeroes_layer.count(1) * fewest_zeroes_layer.count(2)
print(part1)

image = []
for i in range(PIXELS_PER_LAYER):
    j = 0
    while True:
        color = img_layers[j][i]
        if color == 0:
            image.append(".")
            break
        elif color == 1:
            image.append("#")
            break
        elif color == 2:
            j += 1

image = [image[25 * i : 25 * (i + 1)] for i in range(25)]
image = ["".join(i) for i in image]
for i in image:
    print(i)
