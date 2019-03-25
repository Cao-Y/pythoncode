'''
    通过程序生成数字图片或者字母图片作为训练集，
    手写数字/字母识别
'''
import numpy as np
import warnings,time,os
from matplotlib import pyplot as plt
from PIL import Image,ImageFont,ImageDraw,ImageOps
from skimage import transform as tf
from skimage.measure import label, regionprops
import random,time
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import pickle


warnings.filterwarnings('ignore')
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # 字母列表，用来完成预测后，按值索引
numbers='1234567890' # 数字索引
shears =[0.1,0.2,0.3,0,-0.1,-0.2,-0.3] # 斜切值，用来生成不同类型的图像

def create_captcha(text , shear =0.2 ,size=(20, 20)):
    '''
    生成模式为L的黑白图像，生成写有text的文字，斜切值为0.2
    :param text:  str
    :param shear: 图片斜切率
    :param size:  图片大小
    :return:
    '''
    im = Image.new('L', size, color='black')
    draw = ImageDraw.Draw(im)
    draw.text(xy=(1, 1), text=text, fill= 1, font=ImageFont.truetype(r'Coval-Black.otf', 16))
    image = np.array(im)

    # 斜切效果
    image = tf.warp(image, tf.AffineTransform(shear=shear))

    # 保存训练图片
    t = time.time()
    name = str(text)+str(shear)+str(t)+'.png'
    if not os.path.exists('Image'):
        os.mkdir('Image')

    im = Image.fromarray(np.uint8(image))
    im.save(os.path.join('Image',name))

    return image / image.max() # 图像做归一化处理，避免单值范围过大


def segement_image(image):
    '''
    分割图像，按照单个字母分割图像
    :param image: image
    :return: list
    '''
    label_image = label(image > 0)
    subimages = []
    for region in   regionprops(label_image):
        start_x, start_y ,end_x, end_y = region.bbox
        subimages.append(image[start_x:end_x, start_y:end_y])

    if len(subimages) == 0:
        return [image, ]
    return subimages


# 使用Pybrain库，其中创建数据集SupervisedDataSet
# 创建训练集
training = SupervisedDataSet(400,len(numbers))
for i in range(1000):  # 随机生成1000个图片用于训练
    random.seed(time.time())
    # 从字母/数字索引中随机抽取一个值，冲斜切值随机抽取
    # segement为特样本，y为样本标记
    letter = random.choice(numbers)
    shear = random.choice(shears)
    image = create_captcha(letter, shear)
    segement = tf.resize(segement_image(image)[0], (20, 20))
    y = np.zeros(len(numbers))
    index = numbers.index(letter)
    y[index] = 1
    training.addSample(segement.flatten(),y) # 加入到数据结构中

# 测试集
testing = SupervisedDataSet(400,len(numbers))
print('测试数字：')
for i in range(10):
    random.seed(time.time() )
    letter = random.choice(numbers)
    print(letter,end='')
    shear = random.choice(shears)
    image = create_captcha(letter, shear)
    segement = tf.resize(segement_image(image)[0], (20, 20))
    y = np.zeros(len(numbers))
    index = numbers.index(letter)
    y[index] = 1
    testing.addSample(segement.flatten(),y)
print('\n')

# 创建一个 输入层为400个神经元，隐藏测为100个，输出层为10个的神经网络结构，使用BP神经网络算法（反向传播）
net = buildNetwork(400,5,len(numbers), bias =True)
trainer = BackpropTrainer(net, training, learningrate=0.01 ,weightdecay=0.01)
# 设置训练步数
trainer.trainEpochs(epochs=50)

# 保存模型
pickle.dump(trainer, open('number——tow_predictor.model','wb'),0)

# 测试
predictions = trainer.testOnClassData(dataset=testing)
print("预测数字：")
for v in predictions:
    print(numbers[v],end='')
print()

# 读取图片，，经过反相处理，重定尺寸处理，模式转换为L
image = Image.open('1.png')
plt.imshow(image)
image = ImageOps.invert(image)
image = image.resize((15,20))

image = np.array(image.convert('L'))
image = image / image.max() # 归一
image = segement_image(image)[0] # 分割

# 加入到数据集 400 * 1
testing = SupervisedDataSet(400,1)
testing.addSample(tf.resize(image, (20, 20)).flatten(), 1)

# 加载模型
trainer = pickle.load(open('number——tow_predictor.model', 'rb'))
# 预测
pre = trainer.testOnClassData(dataset=testing)
print('图片所显示数字为：',numbers[pre[0]])
plt.show()