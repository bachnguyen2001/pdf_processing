import os
import subprocess
import time

import img2pdf
from pdf2image import convert_from_path


def pdf_converter(pdf_input_path, pdf_output_path):
    # convert all pdf to editable pdf
    subprocess.run(["ocrmypdf", pdf_input_path, pdf_output_path])


def pdf_to_text_converter(input_path, output_path):
    # convert all pdf to txt
    subprocess.run(["pdftotext", "-layout", input_path, output_path])


def pdf_to_image_converter(input_path, save_path):
    images = convert_from_path(input_path)
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(f"{save_path}/page" + str(i) + ".jpg", "JPEG")


def compress_image_to_pdf(image_path, output_path):
    list_of_images = sorted(os.listdir(image_path))
    image_files_path = list()
    for image in list_of_images:
        image_file_path = os.path.join(image_path, image)
        image_files_path.append(image_file_path)
    pdf_data = img2pdf.convert(image_files_path)
    # Write the PDF content to a file
    with open(output_path, "wb") as file:
        file.write(pdf_data)


def delete_all_images_in_folder(folder_path):
    try:
        images = os.listdir(folder_path)
        for image in images:
            image_path = os.path.join(folder_path, image)
            os.remove(image_path)
        print("all file deleted")
    except OSError:
        print("Error occurred while deleting files.")


# create directory needed for processing if not exist
def create_directory():
    paths = ["./pdf_images", "./image_pdf", "./editable_pdf", "./text_converted"]
    for path in paths:
        os.makedirs(path, exist_ok=True)


def main():
    path = "./raw_pdf"
    dir_list = os.listdir(path)
    print("There are %s files needed to process" % len(dir_list))
    create_directory()

    for pdf in dir_list:
        print(f"Proccess file {pdf}: started")
        raw_pdf_path = path + "/" + pdf
        image_path = "./pdf_images"
        image_pdf_file_path = "./image_pdf" + "/" + pdf
        editable_pdf_file_path = "./editable_pdf" + "/" + pdf
        txt_file_output_path = (
            "./text_converted" + "/" + pdf.replace("pdf", "txt").replace("PDF", "txt")
        )
        # convert pdf to image
        pdf_to_image_converter(raw_pdf_path, image_path)
        # save page images to a pdf file
        compress_image_to_pdf(image_path, image_pdf_file_path)
        # delete all image from folder
        delete_all_images_in_folder(image_path)
        # convert scanned pdf to editable pdf
        pdf_converter(image_pdf_file_path, editable_pdf_file_path)
        # convert pdf to txt
        pdf_to_text_converter(editable_pdf_file_path, txt_file_output_path)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Process done in %s seconds " % (time.time() - start_time))
