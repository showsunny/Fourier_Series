import cv2
import cairosvg


def read_image(file_path):
    # 支持的图片格式
    image_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif')
    
    if file_path.lower().endswith(image_formats):
        # 直接读取图像文件
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError("图片路径错误或图片不存在。")
        return image
        
    elif file_path.lower().endswith('.svg'):
        # 将SVG转换为PNG后读取
        png_path = 'converted_image.png'
        cairosvg.svg2png(url=file_path, write_to=png_path)
        image = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError("图片路径错误或图片不存在。")
        return image
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
