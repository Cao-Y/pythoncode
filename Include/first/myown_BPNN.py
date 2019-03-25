# -*- encoding:utf-8-*-
'''
模拟BPNN神经网络算法，使用sklearn中iris数据集
'''
import math
import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data.astype(np.float32)
y = iris.target.astype(np.int32)

from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
pca = PCA(n_components= 2)
X = pca.fit_transform(X) # 主要特征:n=3
onthot = OneHotEncoder() # 将输出变为3维
y = np.array(onthot.fit_transform(y.reshape(y.shape[0],1)).todense(),dtype=np.int32)

def inv_label_tr(y_1d):
    y_pres = []
    for i in range(y_1d.shape[0]):
        for j in range(3):
            if y_1d[i][j] == 1:
                y_label = j
            y_pres.append(y_label)
    return np.array(y_pres)


# 分割训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=20)

import random
random.seed(0)

def rand(b, a):
    # 随机数函数
    return (b - a) * random.random() + a

def make_matrix(m, n, fill=0.0):
    # 矩阵生成函数
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat

def sigmoid(x):
    # 激活函数
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_derivative(x):
    # 激活函数求导
    return x * (1 - x)

class BNeualnetwork: # BP神经网络
    def __init__(self):
         self.input_n = 0 # 输入神经元个数
         self.hidden_n = 0 # 隐藏层数
         self.output_n = 0 # 输出层数
         self.input_cells = []
         self.hidden_cells = []
         self.output_cells = []
         self.input_weights = []
         self.hidden_weights = []
         self.output_weights = []
         self.input_correction = []
         self.output_correction = []

    def setup(self, ni, nh, no):
        '''
        初始化
        :param ni: 输入
        :param nh: 隐藏层
        :param no: 输出
        :return:
        '''
        self.input_n = ni
        self.hidden_n = nh
        self.output_n = no

        # 初始化神经元
        self.input_cells = [1.0] * self.input_n
        self.output_cells = [1.0] * self.output_n
        self.hidden_cells = [1.0] * self.hidden_n

        # 初始化连接值矩阵
        self.input_weights = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)

        # 初始化权重
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = rand(-2.0, 2.0)

        # 初始化偏置
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        # 激活输入层
        for i in range(self.input_n ):
            self.input_cells[i] = inputs[i]

        # 激活隐藏层
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total)

        # 激活输出层
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total)
        return self.output_cells[:]

    def backpropagation(self, case, label, learn, correct):
        # 反向传播

        self.predict(case)
        # 输出误差
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):


            # print(label)
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error

        # 隐藏层误差
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.input_n):
                error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error

        # 更新输出连接值
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # 更新输入连接值
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change

        # 求全局误差
        error = 0.0
        for o in range(len(label)):
            error += 0.5 *(label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit = 10000, learn=0.5, correct=0.1):
        # 训练神经网络
        for j in range(limit):
            error = 0.0
            for i in range(len(cases)):
                lable = labels[i]
                case = cases[i]
                # print(i)
                error += self.backpropagation(case, lable, learn, correct)
            errors.append(error)
    def fit(self, X_test):
        # 离散预测函数用于输出数据
        y_pre_1d = []
        for case in X_test:
            y_pred = self.predict(case)
            for i in range(len(y_pred)):
                if (y_pred[i] == max(y_pred)):
                    y_pred[i] = 1
                else:
                    y_pred[i] = 0
            y_pre_1d.append(y_pred)
        return inv_label_tr(np.array(y_pre_1d))

    def fit2(self, X_test):
        # 连续预测用于画图
        y_pre_1d = []
        for case in X_test:
            w = np.array([0, 1, 2])
            y_pred = self.predict(case)
            y_pre_1d.append(np.array(y_pred).dot(w.T))
        return np.array(y_pre_1d)

number = 1000
errors =[]
if __name__ == '__main__':
    nn = BNeualnetwork()
    nn.setup(2,5,3)
    nn.train(X_train, y_train, number, 0.05, 0.1) # 训练
    y_pre_1d = nn.fit(X_test) # 测试
    y_test_1d = inv_label_tr(y_test)
    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_pre_1d,y_test_1d)) # 打印精度

    from matplotlib import pyplot as plt
    import matplotlib as mpl
    # 画图
    mpl.rcParams['font.sans-serif'] = [u'Simhei']
    mpl.rcParams['axes.unicode_minus'] = False
    cm_light = mpl.colors.ListedColormap(['#FFA0A0', '#A0FFA0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['#AAAAFF', '#FFAAAA', '#AAFFAA'])

    x1_min, x1_max = X[:, 0].min(), X[:, 0].max()
    x2_min, x2_max = X[:, 1].min(), X[:, 1].max()
    x1, x2 = np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j] # 生成网格采样点

    grid_test = np.stack((x1.flat, x2.flat), axis=1) # 测试点
    grid_hat = nn.fit2(grid_test)
    grid_hat = grid_hat.reshape(x1.shape) # 使之与预测形状相同
    plt.pcolormesh(x1, x2, grid_hat, cmap=cm_light)
    # plt.scatter(X[: 0], X[: 1], c=y, edgecolors='k', s=50, cmap=cm_dark)
    plt.title(u'BNN二特征分类',fontsize=15)
    # plt.show()

    print(grid_hat.shape)

    plt.plot(range(number), errors, '-')
    plt.title('ERROR曲线/1000次')
    plt.show()