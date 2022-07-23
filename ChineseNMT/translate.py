import config
import numpy as np

import torch
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

# from train import train, test # , translate
# from data_loader import MTDataset
from utils import chinese_tokenizer_load, english_tokenizer_load
from model import make_model, batch_greedy_decode    # , LabelSmoothing
from beam_decoder import beam_search


def translate_sentences(sentences, model, beam_search=True):
    """
    传入一句或多句话, 用已训练好的模型进行翻译
    sentences:   a list of sentence - 字符串列表 — 需要翻译的句子(En)
    model:  训练好的模型
    use_beam: 表明是否要使用 beam_search
    """
    sp_eng = english_tokenizer_load()
    PAD = sp_eng.pad_id()  # 0
    BOS = sp_eng.bos_id()  # 2
    EOS = sp_eng.eos_id()  # 3

    sentences_tokens = [[BOS] + sp_eng.EncodeAsIds(sent) + [EOS] for sent in sentences]
    
    # 形成 Transformer 能够看懂的 句子表示方式: vocab indices 
    batch_input = pad_sequence([torch.LongTensor(np.array(l_)) for l_ in sentences_tokens],
                                batch_first = True, padding_value = PAD).to(config.device)
    translate(sentences, batch_input, model, use_beam=beam_search)



def translate(sentences, src, model, use_beam = True):
    """
    用训练好的模型预测单个语句, 并打印模型的结果
    src:    a list of sentences, 一个batch里的所有句子, 每个句子都已经转换成 vocab indices 的表示
    model:  训练好的模型
    use_beam: 表明是否要使用 beam_search
    """
    sp_chn = chinese_tokenizer_load()
    # src.shape = [B, T]
    with torch.no_grad():
        model.eval()
        # src_mask.shape = [B, 1, T]
        src_mask = (src != 0).unsqueeze(-2)
        if use_beam:
            decode_result, _ = beam_search(model, src, src_mask, config.max_len,
                                           config.padding_idx, config.bos_idx, config.eos_idx,
                                           config.beam_size, config.device)
            decode_result = [h[0] for h in decode_result]
        else:
            decode_result = batch_greedy_decode(model, src, src_mask, max_len=config.max_len)
        translation = [sp_chn.decode_ids(_s) for _s in decode_result]
    for idx,trans in enumerate(translation):
        print(f"第 {idx} 句话的翻译情况:")
        print(f"原句子为: {sentences[idx]}") 
        print(f"翻译结果: {trans}\n")


if __name__ == "__main__":
    # 参考博客: https://blog.csdn.net/weixin_43525427/article/details/104865262
    # 服务器的默认gpu显卡正在使用，需要使用gpu的另一个空闲的显卡；
    import os,sys,getopt
    os.environ['CUDA_VISIBLE_DEVICES'] = '2, 3' # 这里相当于是告诉给 1号 gpu 是可以访问并使用的 (由于0号gpu在使用中且内存不足,所以就不用0号gpu了)
    # import warnings
    # warnings.filterwarnings('ignore')
    # run()
    # translate_example()
    sentence = None
    beam_search_flag = False
    try:
        opts,args = getopt.getopt(args=sys.argv[1:],
                    shortopts="t:b", longopts=["translate=","beamsearch"])
        print(f"opts: {opts}")
        print(f"args: {args}")
    except getopt.GetoptError:
        print("usage: python translate.py -t <sentence to be translated> --translate <sentence to be translated> --beamsearch otherArgs")
        sys.exit(2)
    for opt in opts:
        if opt[0] in ("-t","--translate"):
            sentence = [opt[1]]
        elif opt[0] in ("-b","--beamsearch"):
            beam_search_flag = True
    
    # 加载已训练的模型;
    print("Model Initializing...")
    model = make_model(config.src_vocab_size, config.tgt_vocab_size, config.n_layers,
                       config.d_model, config.d_ff, config.n_heads, config.dropout)
    print("Loading the trained model...")
    model.load_state_dict(torch.load(config.model_path))
    print("Model loaded.\n *********")

    print("Inferences begin.")
    
    # translate_example(model, beam_search=False)
    sentences = [
        "Why are you so happy ?",
        "I will come to China next year .",
        "He showed me her picture .",
        "Where can you get tickets ?",
        "Most boys like computer games .",
        "I'm the champion.",
        "I live a happy life in China.",
        "She bought a hot dog from a stand on a street corner and wolfed it down.",
        "The near-term policy remedies are clear: raise the minimum wage to a level that will keep a " \
           "fully employed worker and his or her family out of poverty, and extend the earned-income tax credit " \
           "to childless workers.",
        "Military leaders know this, and the threat that they will eventually push him aside will plague his presidency well into next year.",
        "These leaders are unlikely to accept any power-sharing arrangement that includes the Taliban."
    ]
    if sentence:
        translate_sentences(sentences=sentence, model=model, beam_search=beam_search_flag)
    else:
        translate_sentences(sentences=sentences, model=model, beam_search=beam_search_flag)

# translate_sentences(sentences=sentences, model=model, beam_search=True)


    # # 测试 tokenization
    # sent = "I have never seen such a brazen man"
    # sp_eng = english_tokenizer_load()
    # PAD = sp_eng.pad_id()  # 0
    # BOS = sp_eng.bos_id()  # 2
    # EOS = sp_eng.eos_id()  # 3

    # sentences_tokens = [[BOS] + sp_eng.EncodeAsIds(sent) + [EOS]]
    # print(f"输入句子的 tokens: {sentences_tokens}")
    # translation = [sp_eng.decode_ids(_s) for _s in sentences_tokens]
    # print(f"输入句子再将tokens反转回来: {translation}")