import os
import cv2
import imgaug as ia
import imgaug.augmenters as iaa

# 定义增强器
seq = iaa.Sequential([
    iaa.Fliplr(0.5),
    # 进行水平翻转
    iaa.PiecewiseAffine(scale=(0.01, 0.05)),
    # 对图像进行弯曲变形，产生类似于地图等曲面的效果
    iaa.PerspectiveTransform(scale=(0.01, 0.15)),
    # 对图像进行透视变换，可以用于纠正图片的透视畸变问题；
    iaa.Sometimes(
        0.6,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    # 以0.5的概率进行高斯模糊，模糊程度sigma在0-0.5之间。
    iaa.LinearContrast((0.75, 1.5)),
    # 调整图像对比度，对比度范围在0.75-1.5之间
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
    # 以0.5的概率对图像添加高斯噪声，噪声均值为0，标准差在0-0.05255之间。
    iaa.Multiply((0.6, 1.4), per_channel=0.4),
    # 以0.2的概率对图像进行亮度调整，亮度范围在0.8-1.2之间。
    iaa.CoarseDropout(p=0.05, size_percent=0.02),
    # 随机选择一个区域并用固定的值填充该区域。可以通过设置size_percent参数来控制删除区域的大小，通过p参数来控制每个像素被替换的概率。
    iaa.Dropout(p=0.02),
    # 将输入图像中的像素值随机设置为0，即dropout，这种操作可以通过p参数控制dropout的概率，还可以通过per_channel参数控制是否对每个通道单独处理。
    iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
        # translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
        rotate=(-180, 180),
        shear=(-8, 8)
    )
    # 对图像进行仿射变换，包括缩放、平移、旋转和错切。其中，x和y的缩放比例在0.8-1.2之间，旋转角度在-180到180之间，错切程度在-8到8之间。
], random_order=True)  # apply augmenters in random order

# 定义输入和输出文件夹路径
input_dir = "D:/gzs/pyc demo/first/train/rice"
output_dir = "D:/gzs/pyc demo/first/up date 3/rice 4"

# 对每个图片进行增强并保存
for file_name in os.listdir(input_dir):
    # 读取原始图片
    img_path = os.path.join(input_dir, file_name)
    img = cv2.imread(img_path)

    # 进行增强
    augmented_img = seq(image=img)

    # 保存增强后的图片
    output_path = os.path.join(output_dir, file_name)
    cv2.imwrite(output_path, augmented_img)
