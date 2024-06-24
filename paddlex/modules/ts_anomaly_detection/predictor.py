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

from ..ts_forecast import TSFCPredictor
from .model_list import MODELS


class TSADPredictor(TSFCPredictor):
    """ TS Anomaly Detection Model Predictor """
    entities = MODELS