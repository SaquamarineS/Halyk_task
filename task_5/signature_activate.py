from signature_detector import *

if __name__ == "__main__":
    # Пример использования
    detector = SignatureDetector()
    jpeg_result = detector.detect_from_jpeg('path/to/your/jpeg_image.jpg')
    pdf_result = detector.detect_from_pdf('path/to/your/pdf_document.pdf')
    tiff_result = detector.detect_from_tiff('path/to/your/tiff_image.tiff')

    print(f"JPEG: Signature Detected - {jpeg_result}")
    print(f"PDF: Signature Detected - {pdf_result}")
    print(f"TIFF: Signature Detected - {tiff_result}")
