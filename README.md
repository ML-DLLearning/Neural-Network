# The Essence
本仓库为个人对论文算法复现的初次尝试，其中也包含一些准备工作和附加材料。
## 文献
Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering
## 仓库结构
.
├── official_code/          # 官方代码的搬运  
├── NN_notebook/            # pytorch的笔记  
├── ReproductionProcess/    # 复现的过程（下一部分会详细介绍）  
├── 3D_linear_trans         # 3D线性变换的过程  
├── bm3d_AlgorithmAnalysis  # 对整个bm3d算法的总结和一点个人看法  
                            # 有两种文件版本  
├── LICENSE  
├── requirements.txt  
└── README.md  
## 复现过程（个人对复现的理解，可能较为粗浅）
### 结构
src/ 中我放了gpt生成的加载图片并加入噪声、进行评估还有将两个程序付诸行动的运行程序的模块。
results/ 中我放了demo和test的运行结果，包括具体的PSNR和原图、噪声图和去噪图片的对比结果。
scripts/ 中我放了gpt生成的全流程代码。
run_log 是运行主文件时的日志
### 过程
首先创建一个虚拟环境，再根据requirements.txt在这个环境中下载所有的软件包。
```python
# 创建 Python 虚拟环境并激活它
python -m venv .venv    # 创建虚拟环境，名称为 .venv
source .venv/bin/activate  # Linux/MacOS 激活虚拟环境
# Windows 用户使用以下命令激活虚拟环境
 .venv\\Scripts\\Activate.bat

# 安装 requirements.txt 中的所有依赖
pip install -r requirements.txt

# 确保所有依赖安装成功
pip list
```
然后运行demo文件夹中的所有文件，正常情况下是可以直接跑通的。
其他bm3d主程序和tests文件可以不用动
接下来如果想自己导入图片，可以将scripts目录下的文件导入到official_code中，也可以直接使用我整理好的runningcode
在复现过程中，我使用了三张图片，存放在test文件夹中整个复现的结果可以在results中查看
#### 推荐直接使用runningcode文件，直接运行main文件夹中的文件即可，自主输入图片的路径即可
