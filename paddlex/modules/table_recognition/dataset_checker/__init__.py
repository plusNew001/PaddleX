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
from collections import defaultdict, Counter
from PIL import Image
import json

from ...base import BaseDatasetChecker
from .dataset_src import check, split_dataset, deep_analyse

from ..model_list import MODELS


class TableRecDatasetChecker(BaseDatasetChecker):
    """Dataset Checker for Table Recognition Model
    """
    entities = MODELS

    def convert_dataset(self, src_dataset_dir: str) -> str:
        """convert the dataset from other type to specified type

        Args:
            src_dataset_dir (str): the root directory of dataset.

        Returns:
            str: the root directory of converted dataset.
        """
        return src_dataset_dir

    def split_dataset(self, src_dataset_dir: str) -> str:
        """repartition the train and validation dataset

        Args:
            src_dataset_dir (str): the root directory of dataset.

        Returns:
            str: the root directory of splited dataset.
        """
        return split_dataset(src_dataset_dir,
                             self.check_dataset_config.split.train_percent,
                             self.check_dataset_config.split.val_percent)

    def check_dataset(self, dataset_dir: str) -> dict:
        """check if the dataset meets the specifications and get dataset summary

        Args:
            dataset_dir (str): the root directory of dataset.
        Returns:
            dict: dataset summary.
        """
        return check(dataset_dir, self.global_config.output, sample_num=10)

    def get_show_type(self) -> str:
        """get the show type of dataset

        Returns:
            str: show type
        """
        return "image"

    def get_dataset_type(self) -> str:
        """return the dataset type

        Returns:
            str: dataset type
        """
        return "PubTabTableRecDataset"
