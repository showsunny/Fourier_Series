<!-- <script type="text/javascript" async 
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
-->
# 傅里叶级数的讲解与可视化

## 📖 目录
1. [傅里叶级数的简介](#傅里叶级数的简介)
2. [如何将平面点转换为正余弦函数](#如何将平面点转换为正余弦函数)
3. [代码实现与可视化视频](#代码实现与可视化视频)
4. [运行指南](#运行指南)

---

## 🧠 傅里叶级数的简介
**傅里叶级数**是一种数学工具，用于将周期函数表示为正弦和余弦函数的无穷级数之和。它由法国数学家约瑟夫·傅里叶（Joseph Fourier）在19世纪初提出，广泛应用于信号处理、物理学、工程学等领域。

一个周期为T的复值函数f(t)若在实数域 $[0,T]$ 可积，则他可以用如下三角级数定义：

$$ f(t) = \sum_{n=- \infty}^{ \infty} c_n \cdot e^{j 2\pi\frac{n}{T} t} $$

只取部分和我们可以得到近似值(指数形式和正余弦形式)：

$$ z(t) = \sum_{k=-N}^{N} c_n e^{j2 \pi \frac{k}{T}t} $$

$$
z(t) = a_0 + \sum_{k=1}^{N} \left[ a_k \mathrm{cos}(2 \pi \frac{k}{T} t) + b_k \mathrm{sin}(2 \pi \frac{k}{T} t) \right]
$$

其中，系数 $a_k$ 和 $b_k$ 与复数系数 $c_k$ 的关系如下( $c_0$ 是 $f(t)$ 在 $t \in [0,T]$ 上的均值)：

$$ a_0 = c_0 $$

$$ a_k = c_k + c_{-k} $$

$$ b_k = i(c_k - c_{-k}) $$

$c_k$ 通过如下公式得到(在程序中由`np.fft`计算得到精确的近似值)：

$$ c_k = \frac{1}{2\pi} \int_0^{2\pi} f(t)e^{-j 2\pi\frac{k}{T}t} dt $$

**傅里叶变换连续形式(CFT)**

$${\displaystyle F(f) = \int_{-\infty}^{+\infty}f(t)e^{-j 2\pi f t} dt}$$

**傅里叶变换离散形式(DFT)**

$$ X_{k} = \sum_{n=0}^{N-1} x_n \cdot e^{-j 2\pi\frac{k}{N} n} $$

其中，

$$ \{ \mathrm{x_n} \} :=x_0, x_1, \dots, x_{N-1}, \{ \mathrm{X_n} \} :=X_0, X_1, \dots, X_{N-1} $$

## 🎨 如何将平面点转换为正余弦函数

**步骤**：
1. **采样边界点**：从闭合曲线上采样 $ N $ 个点，形成 $(x_i, y_i)$ 序列。
2. **生成复数点序列**：
   $\[ z_n = x_n + i y_n \]$
3. **进行DFT**：使用 `numpy.fft.fft()` 计算傅里叶系数。
4. **重建曲线**：
   - 使用前 k 个系数按时间 t 逐步绘制。
   - 每个系数对应一个**频率向量**，可以通过向量的旋转与叠加，动态可视化为**旋转向量的和**。

**直观理解**：
- 高频项表示边界的细节，低频项表示大致形状。
- 傅里叶变换将复杂的边界拆解为一组旋转的“钟摆”，最终合成为原始图形。

---

## 🎬 代码实现与可视化视频

我们使用 `manim` 库进行可视化演示，生成以下视频：

![DFT Visual](./video/pi_anime.gif)

**可视化内容**：
<!-- - 蓝色箭头：不同频率的旋转向量。- 红色曲线：这些向量端点的轨迹。 -->



**视频描述**：
<!-- - 左侧显示傅里叶分解过程。- 右侧展示原始形状和傅里叶重建的同步对比。 -->


---

## ⚙️ 运行指南

### 1️⃣ 环境配置
```bash
!sudo apt install libcairo2-dev \
    texlive texlive-latex-extra texlive-fonts-extra \
    texlive-latex-recommended texlive-science \
    tipa libpango1.0-dev
!pip install manim
```

### 2️⃣ 代码示例
以下是用于生成傅里叶变换可视化的 Python 脚本：

```python
import numpy as np
from manim import *

class FourierTransformVisualization(Scene):
    def construct(self):
        # 示例点（圆形）
        N = 100
        t = np.linspace(0, 2 * np.pi, N, endpoint=False)
        points = np.array([np.cos(t) + 1j * np.sin(t) for t in t])

        # 计算傅里叶系数
        coeffs = np.fft.fft(points) / N

        # 绘制向量和轨迹
        circles = VGroup()
        for k, c in enumerate(coeffs):
            circle = Circle(radius=abs(c)).set_stroke(color=BLUE, opacity=0.5)
            circles.add(circle)
        self.play(Create(circles))
```

### 3️⃣ 生成视频
```bash
manim -pql dft_visualization.py FourierTransformVisualization
```

运行后，项目目录下会生成 `media/videos` 文件夹，视频文件位于其中。

---

## 🧩 进阶探索
- 尝试不同形状（如心形、星形）的傅里叶描述子。
- 调整傅里叶系数数量，观察重建误差。
- 分析傅里叶变换在图像识别中的应用。

**Enjoy your Fourier Journey! 🚀**

