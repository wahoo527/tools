from tqdm import tqdm
from time import sleep

with tqdm(total=100) as pbar:
    sleep(1)
    str_pbar = str(pbar)
    print(str_pbar)
    pbar.update(1)
