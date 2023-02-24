import os                                      # Importing the os module for operating system functions
from dotenv import load_dotenv                # Importing the load_dotenv function from the dotenv module
from PIL import Image                          # Importing the Image module from the Pillow library
from multiprocessing import Pool              # Importing the Pool class from the multiprocessing module for parallel processing
from tqdm import tqdm                          # Importing the tqdm module for progress bars

load_dotenv('.env.path')                        # Loading environment variables from the .env.path file

def resize_image(file_path):
    megapixels = 20                              # Setting the maximum number of megapixels for the image to 20
    if file_path.lower().endswith('.png'):       # Checking if the file extension is '.png'
        with Image.open(file_path) as im:        # Opening the image file
            megapixels_in_pixels = megapixels * 1000000            # Converting megapixels to pixels
            ratio = (megapixels_in_pixels / (im.width * im.height)) ** 0.5     # Calculating the ratio of the new image size
            width = int(im.width * ratio)        # Calculating the new width of the image
            height = int(im.height * ratio)      # Calculating the new height of the image
            resized_im = im.resize((width, height))                         # Resizing the image
            output_path = os.path.join(os.environ['OUTPUT_DIR'], os.path.relpath(file_path, os.environ['INPUT_DIR']))    # Creating the output file path
            os.makedirs(os.path.dirname(output_path), exist_ok=True)         # Creating the output directory if it doesn't exist
            resized_im.save(output_path)                                    # Saving the resized image to the output file path

def process_file(file_path):
    resize_image(file_path)                     # Resizing the image
    return file_path                            

if __name__ == '__main__':
    input_dir = os.environ['INPUT_DIR']          # Getting the input directory from the environment variable
    output_dir = os.environ['OUTPUT_DIR']        # Getting the output directory from the environment variable
    pool = Pool(processes=6)                     # Creating a process pool with 6 worker processes
    file_paths = []                               # Initializing an empty list to store file paths
    for root, dirs, files in os.walk(input_dir):  # Walking through the input directory and its subdirectories
        for file in files:                       # Looping through the files in each directory
            file_path = os.path.join(root, file) # Creating the file path
            file_paths.append(file_path)         # Adding the file path to the list of file paths
    with tqdm(total=len(file_paths)) as pbar:     # Creating a progress bar with the total number of files to process
        for i, _ in enumerate(pool.imap_unordered(process_file, file_paths)):   # Using the process pool to resize images in parallel
            pbar.update()                        # Updating the progress bar for each processed file
    print("Done")                                # Printing "Done" when all files are processed
