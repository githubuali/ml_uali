import os
def gen_txt():
    # Generando valid.txt

    image_files = []
    for filename in os.listdir("darknet/data/valid"):
        if filename.endswith(".jpg"):
            image_files.append("data/valid/" + filename)
    with open("valid.txt", "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()

    # Generando train.txt

    image_files = []
    for filename in os.listdir("darknet/data/valid"):
        if filename.endswith(".jpg"):
            image_files.append("data/train/" + filename)
    with open("train.txt", "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()
