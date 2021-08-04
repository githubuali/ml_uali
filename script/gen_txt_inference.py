import os

def gen_text (path_img):
    """
        Genera un archivo .txt con los path de cada imagen a inferir
        
        path_img: path de las imagenes a descargar.
    """
    
    try:
        image_files = []
        os.chdir(path_img)
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".JPG"):
                image_files.append(path_img + filename)
        with open("images.txt", "w") as outfile:
            for image in image_files:
                outfile.write(image)
                outfile.write("\n")
            outfile.close()
            
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            os.system.exit(0)
        except SystemExit:
            os._exit(0)
            
if __name__ == "__main__":

    prefix = '28072021_OE_'
    
    download_path = '/home/maximiliano/ml_uali/inference/eventos/' +  prefix + '/'
    
    gen_text (download_path)
