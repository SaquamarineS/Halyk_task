import cv2
import fitz
from PIL import Image
from io import BytesIO
import numpy as np


class SignatureDetector:
    def __init__(self):
        pass

    def detect_from_jpeg(self, image_path):
        try:
            image = cv2.imread(image_path)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, threshold = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            signature_detected = False
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h

                if 2.0 <= aspect_ratio <= 4.0:
                    signature_detected = True
                    break

            return signature_detected
        except Exception as e:
            print(f"Error: {e}")
            return False

    def detect_from_pdf(self, pdf_path):
        try:
            pdf_document = fitz.open(pdf_path)
            signature_detected = False

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

                _, threshold = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h

                    if 2.0 <= aspect_ratio <= 4.0:
                        signature_detected = True
                        break

                if signature_detected:
                    break

            pdf_document.close()
            return signature_detected
        except Exception as e:
            print(f"Error: {e}")
            return False

    def detect_from_tiff(self, tiff_path):
        try:
            image = cv2.imread(tiff_path)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, threshold = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            signature_detected = False
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h

                if 2.0 <= aspect_ratio <= 4.0:
                    signature_detected = True
                    break

            return signature_detected
        except Exception as e:
            print(f"Error: {e}")
            return False
