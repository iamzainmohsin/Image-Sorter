import image_utils
proc = image_utils.ImageProcessor()
proc.load_image("/home/zainm/Desktop/MAIN FOLDER/folder 1/AHP_1258_AH_CABI_PAK_Parthenium_Insect.jpg")
proc.resize_image(0.5)
image = proc.get_image_copy()
print(image.shape)