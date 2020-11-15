## 基于opencv计算颗粒

## 如何使用 `python Count.py img/1.jpg`

### 思路：
1. 采用距离变换，腐蚀，膨胀等形态学操作对粘连颗粒进行分割
2. 采用轮廓检测对颗粒统计个数

### 环境：
python 3.8
opencv-python
numpy

### 图片
必须是统一深色作为颗粒背景，这样能形成比较好的对比度，方便区分
若使用白色作为背景，应当再第一次二值化的时候cv2.THRESH_BINARY参数改为cv2.THRESH_BINARY——INV
### 代码
* 使用cv2.imread()读取图片，格式可以是.jpg,.png等,读取通道顺序为BGR
* 灰度图处理
* 二值化处理，阈值选择120（具体还需调试）
* 对图片使用（5，5）（具体使用什么样的核还需调试计算）进行腐蚀操作，初步进行粘连分割
* 使用距离变换，每个计算非零像点到最近零像素点的距离，讲值保存再对应相速点的位置，对图片进一步特征提取
* 再进一步使用（5，5）开运算对图片粘连处分割
* 最后采用轮廓检测，统计颗粒轮廓个数

### 使用方法
```python
#实例化
app = Count()
#读取图片
img = cv2.imread(img_path)
#运行
number, result_img = app.run(img)
cv2.imwrite(filename,result)
cv2.imshow('result',result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
