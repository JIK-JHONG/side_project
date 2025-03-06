QT_Image_Analysis_Blur 景深模擬小工具（計算）
-

**透過影像計算來弄出類似景深效果的功能。**

# V 1.1  Relased on 2025.03.06

Rename Elements in UI and Widget.


# V 1.0  Relased on 2025.03.04

此為 practise 項目改的，所以命名有點亂，但功能有趣，就先放到 side_project，之後再進行調整。

演算法部分，採用相對單純的遮罩計算。

**主要概念為「辨別主體」 - 「分離主體、背景」 - 「結合」。**



**演算法概念**

# 找出主體（原本圖片）
1. Gray
2. Gaussian - blur
3. Open or Close 運算
4. Binary


Note : 原本有使用 Canny，但他是用於找邊緣，對於計算景深，並沒有太大幫助（儘管設定成填充模式FILLED，效果有限）；故捨去。


此時的圖像為 Binary 的 Mask，為了讓邊緣平滑過渡，可以進行 Gaussian 作為平滑化的依據。

# 分離主體與背景：背景處理（原本圖片）
1. Gaussian - blur

# 合併計算：
1. 處理過的背景 + 分離的主體 進行圖片合併（判斷 mask > 0 ）


# 模糊使用介面

![介面](https://github.com/JIK-JHONG/side_project/blob/main/QT_Image_Analysis_Blur/demo_blur.jpeg)


# 過程檢視介面（可以看 Mask ），白色為主體，黑色為背景。

![介面](https://github.com/JIK-JHONG/side_project/blob/main/QT_Image_Analysis_Blur/demo_binary.jpeg)


# 浮水印：
1. 覆蓋率 = 遮罩(Mask)像素 / 整體像素 * 100%
2. 遮罩(Mask)像素
3. 整體像素


