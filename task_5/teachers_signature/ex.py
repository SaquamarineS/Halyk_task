from PIL import Image

def split_image(image_path, output_directory):
    img = Image.open(image_path)
    width, height = img.size
    cropped_images = []

    sub_width = 150
    sub_height = 100

    for j in range(0, height, sub_height):
        for i in range(0, width, sub_width):
            box = (i, j, i + sub_width, j + sub_height)
            cropped_img = img.crop(box)
            cropped_images.append(cropped_img)
            cropped_img.save(f"{output_directory}/img_{len(cropped_images)+8}.jpg")

    return cropped_images

# Пример использования функции
image_path = r'task_5/teachers_signature/img_3.png'
output_directory = r'task_5/teachers_signature'
split_images = split_image(image_path, output_directory)