import numpy as np
import matplotlib.pyplot as plt
from manim import *
import cv2
import math
from utils import read_image,polygon_centriod



# 1. 读取图片
image = read_image('pi.png')

# 2. 边缘检测
image = cv2.GaussianBlur(image, (5,5), 0)
edges = cv2.Canny(image, 50, 150)

# 3. 查找轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
if len(contours) == 0:
    raise ValueError("未检测到轮廓，请调整Canny阈值或检查图片。")

# 4. 选取最大轮廓
contour = max(contours, key=cv2.contourArea)
contour_points = contour.squeeze()

# 5. 采样N个点
N = 512
if len(contour_points) > N:
    indices = np.linspace(0, len(contour_points)-1, N, dtype=int)
    sampled_points = contour_points[indices]
else:
    sampled_points = contour_points

# 6. 转换坐标系
h, w = image.shape
sampled_points = sampled_points - np.array([w/2, h/2])  # 平移坐标系至图像中心
sampled_points[:, 1] = -sampled_points[:, 1]  # y轴向上
sampled_points = sampled_points / (min(h,w)*10)     # 调整尺度


# 将边界点平移，使质心位于(0,0)  如果轮廓不在图片中心取消以下两行代码注释
# cx, cy = polygon_centroid(sampled_points)
# centered_points = sampled_points - np.array([cx, cy])


# 7. 转为复数形式
complex_points = sampled_points[:, 0] + 1j * sampled_points[:, 1]

# 8. 计算傅里叶变换
fourier_coeffs = np.fft.fft(complex_points)
frequencies = np.fft.fftfreq(N)
angular_frequencies = 2 * np.pi * frequencies

# 按振幅排序
sorted_indices = np.argsort(np.abs(fourier_coeffs))[::-1]
fourier_coeffs = fourier_coeffs[sorted_indices]
angular_frequencies = angular_frequencies[sorted_indices]


fourier_coeffs = fourier_coeffs[:60]    用 M 个圆来近似
angular_frequencies = angular_frequencies[:60]

# # 9. 打印傅里叶系数和对应的角速度
# print("傅里叶级数（系数及对应角速度）：")
# for i, (coeff, omega) in enumerate(zip(fourier_coeffs, angular_frequencies)):
#     print(f"频率索引: {i}, 角速度: {omega:.13f}, 系数: {coeff}")

# # 10. 可视化
# plt.figure(figsize=(6, 6))
# plt.imshow(edges, cmap='gray', extent=[-w/2, w/2, -h/2, h/2])
# plt.plot(sampled_points[:, 0]*(min(h,w)*10), sampled_points[:, 1]*(min(h,w)*10), 'r.')
# plt.title('Edge Points (60 samples) with Centered Coordinates')
# plt.axhline(0, color='gray', linestyle='--')
# plt.axvline(0, color='gray', linestyle='--')
# plt.show()

class Locus(Scene):
    def construct(self, scale=15, fourier_coeffs=fourier_coeffs, angular_frequencies=angular_frequencies):
        # 缩放后的平面
        plane = NumberPlane(
            x_range=[-8 * scale, 8 * scale, 1/8 * scale],
            y_range=[-5 * scale, 5 * scale, 1/8 * scale],
            x_length=16,
            y_length=10,
            axis_config={
                "color": WHITE,
                "stroke_width": 3,
            },
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 0.5,
                "stroke_opacity": 0.5,
            },
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": range(-7 * scale, 8 * scale, 1 * scale),
                "decimal_number_config": {"num_decimal_places": 0},
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": range(-7 * scale, 8 * scale, 1 * scale),
                "decimal_number_config": {"num_decimal_places": 0},
            }
        )

        # 加粗整数轴
        integer_axes = NumberPlane(
            x_range=[-8 * scale, 8 * scale, 1 * scale],
            y_range=[-5 * scale, 5 * scale, 1 * scale],
            x_length=16,
            y_length=10,
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 2,
                "stroke_opacity": 0.7,
            }
        )

        plane.axes.set_color(WHITE)

        self.add(plane, integer_axes)

        def trajectory(t):
            x, y = 0, 0
            for i in range(len(fourier_coeffs)):
                a_i = np.real(fourier_coeffs[i])  # 实部
                b_i = np.imag(fourier_coeffs[i])  # 虚部
                omega_i = angular_frequencies[i]
                x += (a_i * np.cos(omega_i * t)-b_i * np.sin(omega_i * t))
                y += (b_i * np.cos(omega_i * t)+a_i * np.sin(omega_i * t))
            return np.array([x/scale, y/scale, 0])
        T = 2 * PI / angular_frequencies[0]
        curve = ParametricFunction(trajectory, t_range=[0, T], color=WHITE)
        run_time = T / 40
        self.play(Create(curve), run_time=run_time,rate_func=linear)
        self.wait()
