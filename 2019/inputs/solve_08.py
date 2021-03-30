def chunks(lst, n):
    """Yield successive n-sized chunks from `lst`.
    
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


with open("inputs/input_08.txt") as file:
    img_data = [int(x) for x in file.read()]

# Split the data into layers:
HEIGHT = 6
WIDTH = 25
PIXELS_PER_LAYER = HEIGHT * WIDTH
NUM_LAYERS = len(img_data) // PIXELS_PER_LAYER
img_layers = list(chunks(img_data, PIXELS_PER_LAYER))

# PART 1.
zeroes = [layer.count(0) for layer in img_layers]
fewest_zeroes_layer = img_layers[zeroes.index(min(zeroes))]
part1 = fewest_zeroes_layer.count(1) * fewest_zeroes_layer.count(2)

# PART 2.
image = []
for i in range(PIXELS_PER_LAYER):
    j = 0
    while True:
        color = img_layers[j][i]
        if color == 0:
            image.append(" ")
            break
        elif color == 1:
            image.append("#")
            break
        elif color == 2:
            j += 1

image = list(chunks(image, WIDTH))
part2 = ["".join(i) for i in image]

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2:")
    for line in part2:
        print(line)
