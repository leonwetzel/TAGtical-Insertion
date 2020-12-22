#!/usr/bin/env python3
import os

import requests
from tqdm import tqdm

FILES = [
    "https://raw.githubusercontent.com/RikVN/DRS_parsing/master/parsing/layer_data/gold/en/dev.conll",
    "https://raw.githubusercontent.com/RikVN/DRS_parsing/master/parsing/layer_data/gold/en/test.conll",
    "https://raw.githubusercontent.com/RikVN/DRS_parsing/master/parsing/layer_data/gold/en/train.conll"
]


class DownloadManager:

    @staticmethod
    def download():
        """

        Returns
        -------

        """
        if not os.path.isdir("data"):
            os.mkdir("data")

        for file in FILES:
            response = requests.get(file, stream=True,
                                    allow_redirects=True)
            total_size_in_bytes = int(
                response.headers.get('content-length'))

            with open(rf"data/{file.split('/')[-1]}", 'wb') as f:
                with tqdm(total=total_size_in_bytes, unit="B",
                          unit_scale=True, desc=file,
                          initial=0, ascii=True) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
