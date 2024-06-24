# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: PaddlePaddle Authors
"""
import os
import os.path as osp
from collections import defaultdict
from pathlib import Path
import pandas as pd

from .....utils.errors import DatasetFileNotFoundError


def check(dataset_dir, output, sample_num=10):
    """ check dataset """
    dataset_dir = osp.abspath(dataset_dir)
    if not osp.exists(dataset_dir) or not osp.isdir(dataset_dir):
        raise DatasetFileNotFoundError(file_path=dataset_dir)

    sample_cnts = dict()
    tables = defaultdict(list)
    vis_save_dir = osp.join(output, 'demo_data')

    tags = ['train', 'val']
    for _, tag in enumerate(tags):
        file_list = osp.join(dataset_dir, f'{tag}.csv')
        if not osp.exists(file_list):
            if tag in ('train', 'val'):
                # train and val file lists must exist
                raise DatasetFileNotFoundError(
                    file_path=file_list,
                    solution=f"Ensure that both `train.csv` and `val.csv` exist in \
{dataset_dir}")
            else:
                continue
        else:
            df = pd.read_csv(file_list)
            sample_cnts[tag] = len(df)
            vis_path = osp.join(vis_save_dir, f'{tag}.csv')
            Path(vis_path).parent.mkdir(parents=True, exist_ok=True)
            vis_df = df.iloc[:sample_num, :]
            vis_df.to_csv(vis_path, index=False)
            header_list = df.columns.to_list()
            data_list = df.head(10).values.tolist()
            tables[tag] = [header_list] + data_list

    attrs = {}
    attrs['train_samples'] = sample_cnts['train']
    attrs['train_table'] = tables['train']
    attrs['val_samples'] = sample_cnts['val']
    attrs['val_table'] = tables['val']
    return attrs
