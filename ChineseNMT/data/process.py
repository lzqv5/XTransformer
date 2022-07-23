# process the dev data
import json

# 加载 json 数据并形成 python 格式

# 根据 closed issue 7, 我们跳过 dev data 的  2000-3000 行

with open('./json/dev.json','r') as f:
    devData = json.load(f)
    newDevData = devData[:2000] + devData[3001:]    # 忽略掉 dev 中的损坏的数据

with open('./json/newDev.json','w') as f:
    json.dump(newDevData, f)
    print("加载入文件完成...")
