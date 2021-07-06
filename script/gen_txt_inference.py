import os

# Generando images.txt
folder_name = "S-N-20210630"

image_files = []
os.chdir("..")
os.chdir(os.path.join("inference", "eventos",folder_name))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".JPG"):
        image_files.append("../eventos/" + folder_name + "/" + filename)
os.chdir("..")
with open("images.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")
