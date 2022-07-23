# 用来检测各个变量;
from gettext import translation
import config

# test the data_loader.py
# import os
# import torch
# import data_loader
# # print(os.chdir("./tokenizer"))
# root = "/home/newdisk/ziqin.luo/projects/explainable-transformer/ChineseNMT"
# train_dataset = data_loader.MTDataset(root+"/data/json/train.json")

# # Dataset 可以更自由地定义数据的组织构成和访问方式;
# print(f"train_dataset[0] = {train_dataset[0]}")
# print(f"length of train_dataset = {len(train_dataset)}")
# print("~~~~********************")

# # DataLoader 可以更便捷地访问数据集;
# train_dataloader = torch.utils.data.DataLoader(train_dataset, 
#     shuffle=True, # 从 Dataset 中取样本时, 会打乱采样顺序
#     batch_size=config.batch_size,   # 32
#     # collate_fn = None   # default
#     collate_fn=train_dataset.collate_fn # 定义了 每个 batch 返回的是什么 - 默认是None, 也即一个 batch 就是 a list of samples
# )

# for batch in train_dataloader:
#     # 可以知道每个 batch 有什么
#     if isinstance(batch,data_loader.Batch):
#         print("src_texts:")
#         print(batch.src_text[:2]) # 当 collate_fn=train_dataset.collate_fn 时, 此时的 batch 是 data_loader.Batch 的一个对象
#         print("trg_texts:")
#         print(batch.trg_text[:2])
#         print(f"length of srcs (batch size): {len(batch.src)}")
#         print("srcs:")
#         print(batch.src[:2])
#         print("src_masks:")
#         print(batch.src_mask[:2])
#     else:   # collate_fn == None, 不做任何整理, 直接得到的每个 batch 的返回值
#         print(batch.__class__)  # list
#         print(len(batch))       # 2   (2个元组)
#         print(len(batch[0]))    # 32  (每个元组内是一个batch里所有的 eng_text 和 chn_text)   
#         print(batch)    # [(eng_texts of all the samples in a batch), (chn_texts of all the samples in a batch)]
#     break



# # test the Encoder
# import torch
# import torch.nn.functional as F
# import model
# Bsize = 3
# numFeatures = 10
# # x = torch.randint(-10,-1,(Bsize,numFeatures)) # log-probs
# # target = F.softmax(torch.randn((Bsize,numFeatures)),dim=1)    # target probs
# x = torch.arange(30).reshape(3,-1) # [B,T] = [2,10] - 表示这个 batch 里有 2 个句子, 每个长度对其后为10
# x = x.to(device=config.device)  # 为了后续计算能够兼容 - on the same device
# print(f"Initial shape: {x.size()}")

# embeddingLayer = model.Embeddings(config.d_model, config.src_vocab_size).to(config.device)
# x = embeddingLayer(x)
# print(f"after embedding: {x.size()}")   # torch.Size([3, 10, 512]) = [B,T,d_model] # 在最后维进行编码

# peLayer = model.PositionalEncoding(config.d_model,dropout=config.dropout,max_len=config.max_len)
# x = peLayer(x)
# print(f"after pos encoding: {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]

# LN1Attention = model.LayerNorm(features=config.d_model).to(config.device)
# x = LN1Attention(x)
# print(f"after LayerNorm: {x.size()}") #  torch.Size([3, 10, 512]) = [B,T,d_model]

# # h=8, d_model=512, dropout=0.1
# multiHeadAttentionLayer = model.MultiHeadedAttention(h=config.n_heads,d_model=config.d_model,dropout=config.dropout).to(config.device)
# x_copy = x.data.clone() # 只 clone x 的数值, 其余x的梯度等等属性不克隆
# # x = multiHeadAttentionLayer(multiHeadAttentionLayer.linears[0](x),
# #                             multiHeadAttentionLayer.linears[1](x),
# #                             multiHeadAttentionLayer.linears[2](x))
# x = multiHeadAttentionLayer(x,x,x,None) # x = sublayer(x)
# print(f"after 1st MultiHeadedAttention sublayer: {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]

# dropoutLayer = torch.nn.Dropout(p=config.dropout)
# x = x + dropoutLayer(x) # x = x + dropout(sublayer(x))
# print(f"after 1st residual connection: {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]
# # 上面步骤等价于做了一次残差链接 : SublayerConnection(x,sublayer) ->  x + self.dropout(sublayer(self.norm(x)))

# # 这个 mlp 输入和输出通道均为 d_model=512, 可以直接将 x 传入, mlp 直接作用于 x 的最后一维, 相当于 mlp 同时作用于这个 batch 的所有 sequence 的每个 embedding 上
# LN1MLP = model.LayerNorm(features=config.d_model).to(config.device)
# feedForwardLayer = model.PositionwiseFeedForward(d_model=config.d_model,d_ff=config.d_ff,dropout=config.dropout).to(config.device)
# x = x + dropoutLayer(feedForwardLayer(LN1MLP(x)))
# # 第二次残差链接 : SublayerConnection(x,sublayer) ->  x + self.dropout(sublayer(self.norm(x)))
# print(f"after 1st feed forward and residual connection (i.e. the output of the first encoder layer): {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]



# test the decoder
import os
import torch
import torch.nn.functional as F
import utils
import data_loader
import model
from copy import deepcopy

# 获取数据集
train_dataset = data_loader.MTDataset("./data/json/train.json")

# 定义数据访问方式
train_dataloader = torch.utils.data.DataLoader(train_dataset, 
    shuffle=True, # 从 Dataset 中取样本时, 不会打乱采样顺序
    batch_size=config.batch_size,   # 32
    collate_fn=train_dataset.collate_fn # 定义了 每个 batch 返回的是什么 - 默认是None, 也即一个 batch 就是 a list of samples
)

# 获得一个 mini-batch 的数据;
# batch 是 data_loader.Batch 的一个对象
for batch in train_dataloader:
    break

src_text = batch.src_text
trg_text = batch.trg_text
src = batch.src     # src.shape = [B, Ts]
src_mask = batch.src_mask   # src_mask.shape = [B, 1, Ts]
trg = batch.trg     # trg.shape = [B, Tt]
trg_y = batch.trg_y 
trg_mask = batch.trg_mask   # trg_mask.shape = [B, Tt, Tt]
ntokens = batch.ntokens

# embeddingLayerEncoder = model.Embeddings(config.d_model, config.src_vocab_size).to(config.device)
# x = embeddingLayerEncoder(src)
# print(f"after embedding: {x.size()}")   # torch.Size([32, T, 512]) = [B,T,d_model] # 在最后维进行编码

# peLayer = model.PositionalEncoding(config.d_model,dropout=config.dropout,max_len=config.max_len)
# x = peLayer(x)
# print(f"after pos encoding: {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]

# LN1Attention = model.LayerNorm(features=config.d_model).to(config.device)
# x = LN1Attention(x)
# print(f"after LayerNorm: {x.size()}") #  torch.Size([3, 10, 512]) = [B,T,d_model]

# # h=8, d_model=512, dropout=0.1
# multiHeadAttentionLayer = model.MultiHeadedAttention(h=config.n_heads,d_model=config.d_model,dropout=config.dropout).to(config.device)
# dropoutLayer = torch.nn.Dropout(p=config.dropout)
# x = x + dropoutLayer(multiHeadAttentionLayer(x,x,x,None)) # x = x + dropout(sublayer(x))
# print(f"after 1st residual connection: {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]
# # 上面步骤等价于做了一次残差链接 : SublayerConnection(x,sublayer) ->  x + self.dropout(sublayer(self.norm(x)))

# # 这个 mlp 输入和输出通道均为 d_model=512, 可以直接将 x 传入, mlp 直接作用于 x 的最后一维, 相当于 mlp 同时作用于这个 batch 的所有 sequence 的每个 embedding 上
# LN1MLP = model.LayerNorm(features=config.d_model).to(config.device)
# feedForwardLayer = model.PositionwiseFeedForward(d_model=config.d_model,d_ff=config.d_ff,dropout=config.dropout).to(config.device)
# x = x + dropoutLayer(feedForwardLayer(LN1MLP(x)))
# print(f"after 2nd residual connection: {x.size()}") # torch.Size([3, 10, 512]) = [B,T,d_model]
# # 第二次残差链接 : SublayerConnection(x,sublayer) ->  x + self.dropout(sublayer(self.norm(x)))

# memory = x  # torch.Size([32, T, 512])
# attn = model.MultiHeadedAttention(config.n_heads, config.d_model).to(config.device)
# ff = model.PositionwiseFeedForward(config.d_model, config.d_ff, config.dropout).to(config.device)
# decoderLayer = model.DecoderLayer(config.d_model,
#             self_attn=deepcopy(attn),
#             src_attn=deepcopy(attn),
#             feed_forward=deepcopy(ff),
#             dropout=config.dropout)

# decoderLayer(x=1, memory=memory, src_mask=src_mask, tgt_mask=trg_mask)


mymodel = model.make_model(config.src_vocab_size, config.tgt_vocab_size, config.n_layers,
                       config.d_model, config.d_ff, config.n_heads, config.dropout)
# print(f"model structure: {mymodel}")
# print("********** \n one sentence translation")


# model = model.make_model(config.src_vocab_size, config.tgt_vocab_size, config.n_layers,
#                        config.d_model, config.d_ff, config.n_heads, config.dropout)
# if __name__ == "__main":
#     print("enter the file...")
#     train_dataset = data_loader.MTDataset(config.train_data_path)
