import cv2
import cairosvg


def read_image(file_path):
    # 支持的图片格式
    image_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif')
    
    if file_path.lower().endswith(image_formats):
        # 直接读取图像文件
        image = cv2.imread(file_path)
        return image
    elif file_path.lower().endswith('.svg'):
        # 将SVG转换为PNG后读取
        png_path = 'converted_image.png'
        cairosvg.svg2png(url=file_path, write_to=png_path)
        image = cv2.imread(png_path)
        return image
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
