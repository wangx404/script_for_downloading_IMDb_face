# script_for_downloading_IMDb_face
A python script for downloading IMDb images (SenseTime clean datasets) with multi processings.

Before using this script to download images, you should download the csv file firstly. You can find the donwload link in here.  https://github.com/fwang91/IMDb-Face

Besides, the authors had published a paper about the IMDb datasets for face recognition. And I think that paper is pretty inspiring. I recommend you to read that if you are doing relative work. You can read that paer in here. https://arxiv.org/abs/1807.11649

To use this script, you should set some variables, such as root_dir and so on. The variables and their meanings are listed in the front of this script.

一个用于下载IMDb人脸数据集的多进程python脚本。

在使用此脚本下载数据集之前，你首先需要将存储图片信息的csv文件下载到你的电脑或者服务器上。你可以在这里找到相应的下载链接。
https://github.com/fwang91/IMDb-Face

作者就此数据集撰写了一篇论文，论文的名字是《The Devil of Face Recognition is in the Noise》。虽然是一篇预印本论文，但是我觉得这篇论文的内容仍然具有一些洞见。一个规模相对较小的，但是更干净的数据集（可以达到更大规模的脏数据集同样的效果）对于学术界探索人脸识别模型的极限有着很大的帮助。不管你是在工业界还是在学术界，如果你正在从事相关的工作，我推荐你看一下。你可以在这里找到这篇论文：https://arxiv.org/abs/1807.11649

在使用本脚本之前，你需要设置一些变量（主要是csv文件的位置、下载文件夹、缓存文件夹和进程数）。你可以在脚本的开头找到这些变量和它们的含义。

P.S.由于在中国大陆下载这些数据的速度非常缓慢，因此强烈建议你使用类似AWS的服务器进行下载。在完成下载后，通过类似bypy之类的扩展将数据传输到本地。
