import torch
import json
import numpy as np
from torch.autograd import Variable
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from utils import english_tokenizer_load
from utils import chinese_tokenizer_load

import config
DEVICE = config.device


def subsequent_mask(size):
    """Mask out subsequent positions."""
    # 设定subsequent_mask矩阵的shape
    attn_shape = (1, size, size)

    # 生成一个右上角(不含主对角线)为全1，左下角(含主对角线)为全0的subsequent_mask矩阵
    subsequent_mask = np.triu(np.ones(attn_shape), k=1).astype('uint8')

    # 返回一个右上角(不含主对角线)为全False，左下角(含主对角线)为全True的subsequent_mask矩阵
    return torch.from_numpy(subsequent_mask) == 0


# 定义了一个 Batch 的内容
# 根据 collate_fn 的定义可知, 每个 Batch 实例输入的各个输入是
# src_text: 是一个 batch 里面的所有英文文本, a list of all the English text in a mini-batch
# trg_text: 是一个 batch 里面的所有中文文本, a list of all the Chinese text in a mini-batch
# src: 是一个 batch 里面所有英文文本所对应的经过 pad 后的 vocab index;
# batch 里 所有的句子都经过了填充, 彼此都是等长的;
class Batch:
    """Object for holding a batch of data with mask during training."""
    def __init__(self, src_text, trg_text, src, trg=None, pad=0):
        """
        src.shape = [B, Ts]
        trg.shape = [B, Tt]
        src_mask.shape = [B, 1, Ts]
        trg_mask.shape = [B, Tt, Tt]
        """
        self.src_text = src_text
        self.trg_text = trg_text
        src = src.to(DEVICE) # tensor - 是输入文本经过词汇表后得到的 vocab index 表示
        self.src = src  # src.shape = [B, T]

        # 对于当前输入的句子非空部分进行判断成bool序列
        # 并在seq length前面增加一维，形成维度为 1×seq length 的矩阵
        # self.src_mask 标记 self.src中哪些部分是有效内容, 哪些部分是填充的无效内容;
        # 因为 src 只输入到 encoder 中, attention 可以看到所有位置, 所以这里 src_mask 只需要识别 src 中那些不是 pad 的部分即可
        # 所以 self.src_mask.shape = [B, 1, T]
        self.src_mask = (src != pad).unsqueeze(-2) 

        # trg 也应该是文本的 vocab index 表示
        # 如果输出目标不为空，则需要对decoder要使用到的target句子进行mask
        # 如果输出目标为空, 那么应该是 inference 而非 train
        if trg is not None:
            trg = trg.to(DEVICE)

            # decoder要用到的target输入部分
            self.trg = trg[:, :-1] # 去掉最后一列(因为最后一列不需要作为输入传入)

            # decoder训练时 应预测输出 的target结果
            self.trg_y = trg[:, 1:]

            # 将target输入部分进行attention mask
            # 因为 trg 要输入到 decoder 中, attention 只能看到当前以及过去的位置
            # 所以这里 trg_mask 除了需要识别 trg 中那些不是 pad 的部分, 还要根据当前时刻的不同来生成 mask
            # 所以 self.trg_mask.shape = [B, T, T]
            self.trg_mask = self.make_std_mask(self.trg, pad)   

            # 将应输出的target结果中实际的词数进行统计
            self.ntokens = (self.trg_y != pad).data.sum()



    # Mask掩码操作 — 可以用于后续我们在 Decoder 中做预测以及 实现 masked attention用
    # @ 是函数修饰器, 其原理可以参考 http://c.biancheng.net/view/2270.html
    @staticmethod # 相当于此函数修饰符使得定义的 make_std_mask 不必接收参数 self;
    def make_std_mask(tgt, pad):    # 用于标记一个句子哪些部分是 valid, 哪些部分是 invalid(也即是填充的部分)
        """Create a mask to hide padding and future words."""

        # 由于此时数据还未经过 embedding层, 所以数据的形状为 tgt.shape = [B, T]; B表示batch size, T表示这个batch中所有句子的最大长度
        # tgt_mask.shape = [B, 1, T] - 主要是用来识别出输入的数据中那些不为 padding 的部分
        tgt_mask = (tgt != pad).unsqueeze(-2)   # 表示在原本torch的形状上增加一个轴 e.g. 原本形状为 (3,4) 那么 .unsqueeze(-2) 后形状为 (3,1,4) 元素排布发生变化但是元素不变;

        # 根据 subsequent_mask 的定义可知 Variable(subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data)).shape = [1, T, T]
        # 这里的与操作的目的是选择出
        tgt_mask = tgt_mask & Variable(subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data))
        # 输出的 tgt_mask.shape = [B, 1, T] & [1, T, T] (广播机制) = [B, T, T]; 其表示每个 sequence 的 word-by-word 地被隐蔽掉, 整个矩阵呈现一个
        return tgt_mask
        # 举个例子: 输入 tgt = [[[2,21,32,3,0]] shape = [1,5]
        # 那么 tgt_mask = [[[True, False, False, False, False], 表示 这一次 我只能看到 第一个 word
        #                   [True, True, False, False, False],  表示 这一次 我只能看到 前两个 word
        #                   [True, True, True, False, False],   表示 这一次 我只能看到 前三个 word
        #                   [True, True, True, True, False],    表示 这一次 我只能看到 前四个 word
        #                   [True, True, True, True, False],]]  表示 这一次 我仍然只能看到 前四个 word, 因为第五个是 填充(0), 所以对我来说没有意义
        # tgt_mask.shape = [1,5,5] 

# 定义数据集 Dataset 
class MTDataset(Dataset):
    def __init__(self, data_path):
        # 这里的 out_en_sent 和 out_cn_sent 都是一个列表, 列表里的每个元素都是一个字符串(句子),用以后续转化成 index
        self.out_en_sent, self.out_cn_sent = self.get_dataset(data_path, sort=True)
        # 把利用 setencepiece 构建 vocabulary 时生成的模型文件加载进来, 以便后续将文本字符串转化成数字index;        
        self.sp_eng = english_tokenizer_load()
        self.sp_chn = chinese_tokenizer_load()
        # PAD, BOS, EOS 分别记录了 填充、句子开始、句子结尾 的 token 在 vocab 中的 index
        self.PAD = self.sp_eng.pad_id()  # 0
        self.BOS = self.sp_eng.bos_id()  # 2
        self.EOS = self.sp_eng.eos_id()  # 3

    @staticmethod
    def len_argsort(seq):
        """传入一系列句子数据(分好词的列表形式)，按照句子长度排序后，返回排序后原来各句子在数据中的索引下标"""
        return sorted(range(len(seq)), key=lambda x: len(seq[x]))

    def get_dataset(self, data_path, sort=False):
        """把中文和英文按照同样的顺序排序, 以英文句子长度排序的(句子下标)顺序为基准"""
        dataset = json.load(open(data_path, 'r'))   # 加载 json 文件
        out_en_sent = []
        out_cn_sent = []
        for idx, _ in enumerate(dataset):
            out_en_sent.append(dataset[idx][0])
            out_cn_sent.append(dataset[idx][1])
        # 此处 out_en_sent 和 out_cn_sent 是一个列表, 且列表的每个元素都是英文或中文句子
        if sort:
            # 按照句子的从短到长排序后, 形成相应的索引表
            sorted_index = self.len_argsort(out_en_sent)
            out_en_sent = [out_en_sent[i] for i in sorted_index]
            out_cn_sent = [out_cn_sent[i] for i in sorted_index]
        return out_en_sent, out_cn_sent

    # 我们自定义的 Dataset 需要重写  __getitem__ 和 __len__ 以便 Dataloader 来加载我们的数据

    def __getitem__(self, idx):
        eng_text = self.out_en_sent[idx]
        chn_text = self.out_cn_sent[idx]
        return [eng_text, chn_text]

    def __len__(self):
        return len(self.out_en_sent)

    # collate: 整理(文件或书等);核对，校勘，对照(不同来源的信息)
    # 这个函数就是用来处理每一个 batch 里面的句子, 将这些 原本表示为文本 的句子转化为 对应到词汇表中一个一个index的表示方式
    # e.g. "I am bob" -> [self.BOS, indx of space, index of am, index of space, index of bob, self.EOS]=[2,1,x,1,x,3]
    # collate_fn 是 DataLoader 的一个参数, 作为回调函数, 其作用在于将一个样本列表转化成代表一个mini-batch的Tensor(s)
    def collate_fn(self, batch):
        # 这里的 每个 x 对应着 batch 中的一个 sample, 也即 dataset[i], 也即一个[eng_text, chn_text]二元组
        src_text = [x[0] for x in batch]    # 取 Dataset 里面的英文文本
        tgt_text = [x[1] for x in batch]    # 取 Dataset 里面的中文文本

        # 很明显, 这里说明了将一个句子 从 原始的 文本符号 转化为 对应词汇表中的index
        # 很明显, 不同的句子长度不同, 就会导致不同句子对应的 list of token 的长度是不同的
        # 所以这里需要将变长的句子进行填充 pad token 从而形成多个等长的句子, 最后形成一个 batch
        src_tokens = [[self.BOS] + self.sp_eng.EncodeAsIds(sent) + [self.EOS] for sent in src_text]
        tgt_tokens = [[self.BOS] + self.sp_chn.EncodeAsIds(sent) + [self.EOS] for sent in tgt_text]

        # pad_sequence: Pad a list of variable length Tensors with ``padding_value``
        # 因为 batch_first=True 所以output 的 shape 的第一个数字代表 batch size, 第二个数字代表时间长度,也即 Tensor of size ``B x T x *``
        batch_input = pad_sequence([torch.LongTensor(np.array(l_)) for l_ in src_tokens],
                                   batch_first=True, padding_value=self.PAD)
        batch_target = pad_sequence([torch.LongTensor(np.array(l_)) for l_ in tgt_tokens],
                                    batch_first=True, padding_value=self.PAD)
    
        return Batch(src_text, tgt_text, batch_input, batch_target, self.PAD)
