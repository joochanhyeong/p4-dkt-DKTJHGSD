import os, random, torch
import numpy as np
import datetime
import pandas as pd

def setSeeds(seed = 42):
    # 랜덤 시드를 설정하여 매 코드를 실행할 때마다 동일한 결과를 얻게 합니다.
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)    
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


def get_timestamp(): 
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)
    now2str = now.strftime("%H:%M")
    return now2str


def kfold_ensemble(output_dir, save_dir):
    file_lists = os.listdir(output_dir)
    df = pd.read_csv(os.path.join(output_dir, file_lists[0]))
    for file in file_lists[1:]:
        tmp = pd.read_csv(os.path.join(output_dir,file))
        df = pd.concat([df,tmp['prediction']],axis=1)
    tmp = df.values
    tmp = tmp[:,1:].mean(axis = 1)
    df = df.iloc[:, :1]
    df['prediction'] = tmp
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    df.to_csv(os.path.join(save_dir, "kfold_output.csv"), index = False)

