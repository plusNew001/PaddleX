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

import codecs

import yaml

from ....utils import logging
from ...base.predictor.transforms import image_common
from .transforms import SaveDetResults, PadStride, DetResize


class InnerConfig(object):
    """Inner Config"""

    def __init__(self, config_path):
        self.inner_cfg = self.load(config_path)

    def load(self, config_path):
        """ load infer config """
        with codecs.open(config_path, 'r', 'utf-8') as file:
            dic = yaml.load(file, Loader=yaml.FullLoader)
        return dic

    @property
    def pre_transforms(self):
        """ read preprocess transforms from  config file """
        tfs_cfg = self.inner_cfg["Preprocess"]
        tfs = []
        for cfg in tfs_cfg:
            if cfg['type'] == 'NormalizeImage':
                mean = cfg.get('mean', 0.5)
                std = cfg.get('std', 0.5)
                scale = 1. / 255. if cfg.get('is_scale', True) else 1

                norm_type = cfg.get('norm_type', "mean_std")
                if norm_type != "mean_std":
                    mean = 0
                    std = 1

                tf = image_common.Normalize(mean=mean, std=std, scale=scale)
            elif cfg['type'] == 'Resize':
                interp = cfg.get('interp', 'LINEAR')
                if isinstance(interp, int):
                    interp = {
                        0: 'NEAREST',
                        1: 'LINEAR',
                        2: 'CUBIC',
                        3: 'AREA',
                        4: 'LANCZOS4'
                    }[interp]
                tf = DetResize(
                    target_hw=cfg['target_size'],
                    keep_ratio=cfg.get('keep_ratio', True),
                    interp=interp)
            elif cfg['type'] == 'Permute':
                tf = image_common.ToCHWImage()
            elif cfg['type'] == 'PadStride':
                stride = cfg.get('stride', 32)
                tf = PadStride(stride=stride)
            else:
                raise RuntimeError(f"Unsupported type: {cfg['type']}")
            tfs.append(tf)
        return tfs

    @property
    def labels(self):
        """ the labels in inner config """
        return self.inner_cfg["label_list"]
