# 综合感知
我认为，bm3d相较于先前的“局部性”算法（空间域、变换域滤波）的最大的优势就是其“非局部性”，不像传统算法那样将图片分割成一个个独立的个体，而是通过将相似的图片局部分为一组：相似的结构多次出现了，算法就知道了这个结构不是噪声，而是必要的纹理、边缘……（代价就是每次计算所用到的信息也多，过程也更复杂）；再者就是它分两个阶段进行处理，第一阶段用硬阈值进行预处理，然后最精彩的第二阶段采用维纳滤波的处理方法软化了硬阈值的“硬”，根据总样本方差（噪声大小的数学表达）的大小对能量进行不同程度的收缩，可以有效控制伪影，避免振铃效应等
# 步骤一：初步估计
## a）块估计
### 分块：
将大小为$H×W$的输入的图片按照$N×N$的块进行分割，取一个步长$N_{step}$，通过滑动窗口在图像上提取出一系列中心位置不同的子块。可以重叠$(N_{step}<N)$，也可以不重叠$(N_{step}=N)$。在最理想（不考虑效率）的算法中我们取$N_{step}=1$，即遍历所有的子块。
### 分组：（寻找相似的patch）
#### 计算patch之间的距离
理所当然的，我们采用L2范数，分别计算所有块的“块距离”（也就是各个块相同相对位置的像素值的差的平方和）：
$$
d(\mathbf{Z}_{x_R}, \mathbf{Z}_x) = \frac{1}{N_1^2} \sum_{i=1}^{N_1} \sum_{j=1}^{N_1} \left( \mathbf{Z}_{x_R}(i, j) - \mathbf{Z}_x(i, j) \right)^2
$$
其中，${Z}_{x_R}$是当前处理的patch，$x_R$是patch中心位置的坐标，${Z}_{x}$是将要去遍历的patch，双层求和达到遍历的效果

但是还存在一个问题，在这个方程里面我们使用的是噪声块（因为我们只有噪声块），噪声的方差不尽相同，会影响不含噪声的patch的方差（即相似性），有的块可能是相似的，但是噪声在两个块产生的方差不同，导致其距离超过阈值被判定为不相似块。
所以我们想到先对块进行粗略的预滤波处理，粗略地去除噪声，然后再进行相似性评估。粗略预滤波我们采用硬阈值处理，得到公式：
$$ d(Z_{x_R},Z_x)=\frac{\left||\Upsilon'!\big(T_{2D}(Z_{x_R})\big)-\Upsilon'!\big(T_{2D}(Z_x)\big)\right||2^2}{N_1^2}, $$ 
公式对两个patch进行2D线性变换，然后硬阈值处理后的系数求均方差。
让人在意的是改良后的公式对线性变换后的系数进行操作，而不像原始公式一样通过对像素值进行MSE操作，通过查阅资料得知，根据Parseval 定理
$ ||A-B||2^2=||T_{2D}(A)-T_{2D}(B)||_2^2, $ 
若不进行阈值操作（只是简单的滤波，没有坐标系地转换），那么像素域的MSE与系数域的MSE完全等价，也就是二者求出的距离完全等价，只是改良后的公式因为少了一大部分地噪声的影响而使所分的组更加相似罢了。
#### 块匹配
根据距离d，设置阈值$\tau^{\text{ht}}_{\text{match}}$，若$d<τ$，则将这两个块分为一组，得到了某一个组地中心位置坐标地集合：
$$
S^{\text{ht}}_{x_R}
= \left\{\, x \in X :\; d\!\left(Z_{x_R}, Z_x\right) \le \tau^{\text{ht}}_{\text{match}} \,\right\}
$$
然后我们对以上分好的组（由2D块堆叠而产生的体）做3D线性变换，并进行硬阈值处理。
$$
\widehat{\mathbf{Y}}^{\mathrm{ht}}_{S^{\mathrm{ht}}_{x_R}}
= \left(T^{\mathrm{ht}}_{3\mathrm{D}}\right)^{-1}
\!\left(
\Upsilon\!\left(
T^{\mathrm{ht}}_{3\mathrm{D}}\!\left(\mathbf{Z}_{S^{\mathrm{ht}}_{x_R}}\right)
\right)
\right)
$$
（线性变换部分在仓库中有文件）
对线性变换后的矩阵中某些低于设定阈值的值直接置零，然后进行线性变换的逆变换，就得到了经过硬阈值处理的patch中心位置的集合。
## b）聚合
由于在理想状态下我们的小窗滑动的步长为1，在得到硬阈值处理后的新patch重新拼成原图时必定有重叠部分（在某一点处有多个经过处理的像素值），所以我们通过聚合实现全局估计。分两个部分进行
#### 聚合权重的确定
文章采用权重与相应块的总方差成反比的权重分配，即总方差越大，噪声越大，占比越小。
需要注意一点的是聚合中的操作都是针对同一位置处的不同块的像素值的处理。
${\widehat\\{Y}}^{\mathrm{ht}}_{S^{\mathrm{ht}}_{x_R}}$的总样本方差为：
$$\sigma^2 N^{x_R}_{\mathrm{har}}$$
对于保留下来的每个系数的总方差仍然是$\sigma^2$（硬阈值完全地保留了非零地系数，所以其方差和噪声方差相同），零系数不再引入噪声，然后与非零系数的个数$N^{x_R}_{\mathrm{har}}$相乘得到这个样本的总方差。
文章里给出公式：
$$w_{x_R}^{\mathrm{ht}} = 
\begin{cases}
    \dfrac{1}{\sigma^2 N_{\mathrm{har}}^{x_R}}, & \text{if } N_{\mathrm{har}}^{x_R} \geq 1 \\
    1, & \text{otherwise}
\end{cases}$$
分类是为了预防系数全部置零的patch，将其权重直接设置为1（其实什么数都可以，只要小于∞就行），防止出现∞的结果。
#### 加权平均聚合
公式如下：
\[
\widehat{y}^{\mathrm{basic}}(x) = 
\frac{
    \sum\limits_{x_R \in X} \sum\limits_{x_m \in S_{x_R}^{\mathrm{ht}}} 
    w_{x_R}^{\mathrm{ht}} \widehat{Y}_{x_m}^{\mathrm{ht, x_R}}(x)
}{
    \sum\limits_{x_R \in X} \sum\limits_{x_m \in S_{x_R}^{\mathrm{ht}}} 
    w_{x_R}^{\mathrm{ht}} \chi_{x_m}(x)
}
\]
其中$\widehat{Y}_{x_m}^{\mathrm{ht, x_R}}(x)$是硬阈值处理后的块的估计值，是一个二维矩阵，然后与我们上面得到的权重相乘，对这个矩阵中的每一个系数进行加权，然后两层求和：内层求和某个patch所在的组的所有patch；由于该像素点处重叠了多个组，外层求和就是遍历这所有的组。
最终我们就得到了一张经过粗略预滤波的图片。
# 步骤二：最终估计
我们进行初步估计的目的就是获得一张去除离谱噪声的图片，然后在最终估计中可以使分到一组的图片的相似性更强
## a）块估计
### 分组
采用比硬阈值处理更加精细的操作（wiener filtering），我们定义一个维纳收缩系数：
\[
\mathbf{W}_{S_{x_R}^{\mathrm{swie}}} =
\frac{
    \left| \mathcal{T}_{3D}^{\mathrm{wie}}\left( \widehat{\mathbf{Y}}^{\mathrm{basic}}_{S_{x_R}^{\mathrm{swie}}} \right) \right|^2
}{
    \left| \mathcal{T}_{3D}^{\mathrm{wie}}\left( \widehat{\mathbf{Y}}^{\mathrm{basic}}_{S_{x_R}^{\mathrm{swie}}} \right) \right|^2 + \sigma^2
}
\]
不清楚这个公式是怎么推导出来的，但是我们可以从先验的角度来理解其道理：令$t=$，则原式可以化为：
$$\mathbf{W}_{S_{x_R}^{\mathrm{swie}}} =\dfrac{1}{1+\dfrac{\sigma ^2}{t} } $$
如果$\dfrac{\sigma ^2}{t}$较小，即这个块的能量比噪声的占比大，相应地，$\mathbf{W}_{S_{x_R}^{\mathrm{swie}}}$的值也大，符合我们想要的结果。
用这个收缩系数进行维纳滤波处理，相比硬阈值的生硬处理，维纳滤波没有直接放弃那些可能成为图像细节的小信号，而是类似因材施教，给每一个信号都提供一个合适的加权，适当的扩大和收缩（相对而言）。
经过处理我们得到块的集合：$\widehat{\\{Y}}_{S_{x_R}^{\mathrm{swie}}}^{\mathrm{wie}}=\mathcal{T}_{3D}^{\mathrm{wie}^{-1}}
\left(
    \mathbf{W}_{S_{x_R}^{\mathrm{swie}}}
    \mathcal{T}_{3D}^{\mathrm{wie}}
    \left(
        \mathbf{Z}_{S_{x_R}^{\mathrm{swie}}}
    \right)
\right)$
然后用和上面相同的操作进行距离计算……
### 块匹配
操作同上
## b）聚合
#### 聚合权重的确定
权重分配方法相同，计算总方差：噪声方差乘以维纳收缩系数的平方然后求和（因为每个系数都乘以了维纳收缩系数），即：
$$w_{x_R}^{\mathrm{wie}} = \sigma^{-2} \left\| \mathbf{W}_{x_R}^{\mathrm{swie}} \right\|_2^{-2}$$
#### 加权平均聚合
和上面的处理方法相同，公式改为：
\[
\widehat{y}^{\mathrm{final}}(x) = 
\frac{
    \sum\limits_{x_R \in X} \sum\limits_{x_m \in S_{x_R}^{\mathrm{wie}}} 
    w_{x_R}^{\mathrm{wie}} \widehat{Y}_{x_m}^{\mathrm{wie, x_R}}(x)
}{
    \sum\limits_{x_R \in X} \sum\limits_{x_m \in S_{x_R}^{\mathrm{wie}}} 
    w_{x_R}^{\mathrm{wie}} \chi_{x_m}(x)
}
\]
我们就得到了最终处理的图像。


`后续快速高效方案见仓库`