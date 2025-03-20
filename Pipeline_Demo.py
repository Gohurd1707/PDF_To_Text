import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def convert_pdf_to_images(pdf_folder):
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            base_name = os.path.splitext(pdf_file)[0]
            image_folder = os.path.join(pdf_folder, f"{base_name}_image")
            os.makedirs(image_folder, exist_ok=True)
            images = convert_from_path(pdf_path, poppler_path=r'C:\Users\84936\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin')
            for i, image in enumerate(images):
                image_name = f"{base_name}_{i + 1:02}.png"
                image_path = os.path.join(image_folder, image_name)
                image.save(image_path, "PNG")
                print(f"Saved image: {image_path}")

def convert_images_to_text(pdf_folder):
    pytesseract.pytesseract.tesseract_cmd = r'C:/Users/84936/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    viet_lang_path = r'C:/Users/84936/AppData/Local/Programs/Tesseract-OCR/tessdata'
    os.environ['TESSDATA_PREFIX'] =viet_lang_path
    for folder in os.listdir(pdf_folder):
        if folder.endswith("_image"):
            base_name = folder.replace("_image", "")
            image_folder = os.path.join(pdf_folder, folder)
            text_folder = os.path.join(pdf_folder, f"{base_name}_text")
            os.makedirs(text_folder, exist_ok=True)
            for image_file in os.listdir(image_folder):
                if not image_file.endswith(".png"):
                    continue
                
                image_path = os.path.join(image_folder, image_file)
                text_file = os.path.join(text_folder, f"{os.path.splitext(image_file)[0]}.txt") 

                try:
                    if not os.path.exists(image_path) or os.path.getsize(image_path) == 0:
                        print(f"[WARNING] File ảnh rỗng hoăc không tồn tại: {image_path}")
                        continue

                    with Image.open(image_path) as img:
                        img.verify()

                    img = Image.open(image_path)    
                    text = pytesseract.image_to_string(img, lang ='vie')

                    with open(text_file, "w", encoding="utf-8") as file:
                        file.write(text)
                    print(f"[INFO] Văn bản đã được lưu: {text_file}")

                except (UnicodeDecodeError, IOError) as e:
                    print(f"[ERROR] Không thể xử lý {image_path}: {e}")
                except Exception as e:
                    print(f"[ERROR] Lỗi không xác định với {image_path}: {e}")

def process_all_folders(root_folder):
    for sub_folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, sub_folder)
        if os.path.isdir(folder_path):
            convert_pdf_to_images(folder_path)
            convert_images_to_text(folder_path)

def main():
    root_folder = "D:/thống kê số lượt nợ thuế"
    process_all_folders(root_folder)

if __name__ == "__main__":
    main()

