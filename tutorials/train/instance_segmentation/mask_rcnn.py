import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import paddlex as pdx
from paddlex import transforms
import cv2

xiaoduxiong_dataset = 'https://bj.bcebos.com/paddlex/datasets/xiaoduxiong_ins_det.tar.gz'
pdx.utils.download_and_decompress(xiaoduxiong_dataset, path='./')

train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(), transforms.ResizeByShort(
        short_size=800, max_size=1333, interp=cv2.INTER_CUBIC),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

eval_transforms = transforms.Compose([
    transforms.ResizeByShort(
        short_size=800, max_size=1333, interp=cv2.INTER_CUBIC),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = pdx.datasets.VOCDetection(
    data_dir='insect_det',
    file_list='insect_det/train_list.txt',
    label_list='insect_det/labels.txt',
    transforms=train_transforms,
    shuffle=True)

eval_dataset = pdx.datasets.VOCDetection(
    data_dir='insect_det',
    file_list='insect_det/val_list.txt',
    label_list='insect_det/labels.txt',
    transforms=eval_transforms,
    shuffle=False)

num_classes = len(train_dataset.labels) + 1

model = pdx.det.MaskRCNN(
    num_classes=num_classes, backbone='ResNet50_vd', with_fpn=True)

model.train(
    num_epochs=12,
    train_dataset=train_dataset,
    train_batch_size=1,
    eval_dataset=eval_dataset,
    learning_rate=0.00125,
    warmup_steps=10,
    lr_decay_epochs=[8, 11],
    save_dir='output/mask_rcnn_r50vd_fpn',
    use_vdl=True)
