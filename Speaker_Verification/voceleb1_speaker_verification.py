# -*- coding: utf-8 -*-
"""SU2_speaker_verification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uHwrWEgbcEXhLI1ezxG-68uSICiqTArm
"""

# ### only able to download below model form list, other link were not working
# 1. hubert_large --- require fairseq.
# 2. wavlm_larg --- require pip install s3prl@git+https://github.com/s3prl/s3prl.git@7ab62aaf2606d83da6c71ee74e7d16e0979edbc3#egg=s3prl
# 3.UniSpeech-SAT large
# 4.Wav2Vec2.0 (XLSR)

# already downloaded -- uploaded it drive for anytime use
#/content/drive/MyDrive/Classroom/hubert_large_finetune.pth
# /content/drive/MyDrive/Classroom/wavlm_large_finetune.pth

"""#### Voxceleb1H datasat download"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content
!mkdir /content/voxceleb1h

from torchaudio.datasets import VoxCeleb1Verification

voxceleb1h_dataset = VoxCeleb1Verification(root='/content/voxceleb1h',
                             meta_url = 'https://mm.kaist.ac.kr/datasets/voxceleb/meta/list_test_hard.txt',
                            download=True)

#above cell execution results in disk out of space error ads it download more then 40 GB ,
#  this is also  executed in seprate notebook and commited in github repo
#hence taking subsample of voxceleb to run prediction in below cell

"""#### take subsample of vocxceleb dataset"""

import glob

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/voxceleb1_sample_data.zip

wav_files_list = glob.glob('/content/voxceleb_sample_data/*/*/*.wav')
len(wav_files_list),wav_files_list[0]

"""#### install fairseq"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/pytorch/fairseq

# Change current working directory
!pwd
# %cd "/content/fairseq"
!pip install --editable ./

!pip install fairseq

"""#### clone UniSpeech"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content

!git clone https://github.com/microsoft/UniSpeech

"""#### install requirements"""

# !pip install s3prl==0.3.1
!pip install fire==0.4.0
!pip install sentencepiece==0.1.96

!pip install omegaconf==2.0.6

!sudo apt-get install sox

!pip install s3prl@git+https://github.com/s3prl/s3prl.git@7ab62aaf2606d83da6c71ee74e7d16e0979edbc3#egg=s3prl

!pip install s3prl

"""#### Speaker verification using pretrianned Wavlm_Large model (few sample)"""

!pwd

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/UniSpeech/downstreams/speaker_verification

# checkpoint_path = 'config/unispeech_sat.th'
# checkpoint_path = "/content/drive/MyDrive/hubert_large_finetune.pth"
checkpoint_path = "/content/drive/MyDrive/wavlm_large_finetune.pth"

"""##### 2 different speaker"""

!python verification.py --model_name wavlm_large \
 --wav1 vox1_data/David_Faustino/hn8GyCJIfLM_0000012.wav \
 --wav2 vox1_data/Josh_Gad/HXUqYaOwrxA_0000015.wav  \
 --checkpoint /content/drive/MyDrive/wavlm_large_finetune.pth
# output: The similarity score between two audios is 0.0317 (-1.0, 1.0).

"""##### 2 same speakers"""

!python verification.py --model_name wavlm_large \
 --wav1 /content/voxceleb_sample_data/id10002/cMGEuZ1zqXk/00001.wav \
 --wav2 /content/voxceleb_sample_data/id10002/cMGEuZ1zqXk/00001.wav  \
 --checkpoint /content/drive/MyDrive/wavlm_large_finetune.pth

"""##### 2 different speaker"""

!python verification.py --model_name wavlm_large \
 --wav1 /content/voxceleb_sample_data/id10010/QlrC83eEY2s/00001.wav \
 --wav2 /content/voxceleb_sample_data/id10002/cMGEuZ1zqXk/00001.wav  \
 --checkpoint /content/drive/MyDrive/wavlm_large_finetune.pth

"""#### Speaker verification using Hubert_Large model (few sampels)"""

# %cd /content/UniSpeech/downstreams/speaker_verification

# checkpoint_path = 'config/unispeech_sat.th'
checkpoint_path = "/content/drive/MyDrive/hubert_large_finetune.pth"
# checkpoint_path = "/content/drive/MyDrive/wavlm_large_finetune.pth"

"""##### 2 different speaker"""

!python verification.py --model_name hubert_large \
 --wav1 vox1_data/David_Faustino/hn8GyCJIfLM_0000012.wav \
 --wav2 vox1_data/Josh_Gad/HXUqYaOwrxA_0000015.wav  \
 --checkpoint /content/drive/MyDrive/hubert_large_finetune.pth
# output: The similarity score between two audios is 0.0317 (-1.0, 1.0).

"""##### 2 same speaker"""

!python verification.py --model_name hubert_large \
 --wav1 /content/voxceleb_sample_data/id10002/cMGEuZ1zqXk/00001.wav \
 --wav2 /content/voxceleb_sample_data/id10002/cMGEuZ1zqXk/00001.wav  \
 --checkpoint /content/drive/MyDrive/hubert_large_finetune.pth

"""##### 2 different speaker"""

!python verification.py --model_name hubert_large \
 --wav1 /content/voxceleb_sample_data/id10010/QlrC83eEY2s/00001.wav \
 --wav2 /content/voxceleb_sample_data/id10002/cMGEuZ1zqXk/00001.wav  \
 --checkpoint /content/drive/MyDrive/hubert_large_finetune.pth

"""#### prediction on subsample of voxcele1"""

from verification import verification
# added return sim[0].item() at end of verificaion function in verification.py to return score

similarity_score = verification(model_name = 'hubert_large',
 wav1 =  '/content/voxceleb_sample_data/id10003/EGPV-Xa0LGk/00009.wav',
 wav2 = '/content/voxceleb_sample_data/id10003/K5zRxtXc27s/00005.wav' ,
 checkpoint=  '/content/drive/MyDrive/hubert_large_finetune.pth')

import pandas as pd
import itertools
import random
from tqdm import tqdm
tqdm.pandas()

df = pd.DataFrame(wav_files_list, columns = ['wav_file'])
df['speaker_id'] = df.wav_file.apply(lambda x : x.split('/')[3])
df.head(2)

same_speaker_pairs = []
different_speaker_pairs = []

grouped = df.groupby('speaker_id')
for speaker_id, group in grouped:
    pairs = list(itertools.combinations(group['wav_file'], 2))
    same_speaker_pairs.extend(pairs)

    other_speaker_groups = [g['wav_file'] for s_id, g in grouped if s_id != speaker_id]
    for other_group in other_speaker_groups:
        different_speaker_pairs.extend(list(itertools.product(group['wav_file'], other_group)))

random.shuffle(same_speaker_pairs)
random.shuffle(different_speaker_pairs)
#taking 100 pair for same spekar and 100 for differnt spkear
pair1 = same_speaker_pairs[:100]
pair0 = different_speaker_pairs[:100]

df1 = pd.DataFrame(pair0)
df1['label'] = 0
df2 = pd.DataFrame(pair1)
df2['label'] = 1
data_df= pd.concat([df1, df2])
data_df.columns = ['wav1', 'wav2', 'label']
data_df.shape, data_df.columns

data_df.head(2)

data_df['hubert_large_pred'] = data_df.progress_apply(lambda x:verification(model_name = 'hubert_large',wav1 =x['wav1'],wav2 = x['wav2'],
                                          checkpoint=  '/content/drive/MyDrive/hubert_large_finetune.pth'), axis =1)

data_df['wavlm_large_pred'] = data_df.progress_apply(lambda x:verification(model_name = 'wavlm_large',wav1 =x['wav1'],wav2 = x['wav2'],
                                          checkpoint=  '/content/drive/MyDrive/wavlm_large_finetune.pth'), axis =1)

data_df.to_csv("/content/drive/MyDrive/speaker_verification_result.csv"

# stored above prediction logs into txt file by manully copying stdout of code run from above cell for
#both hubert and wavlm large, as gpu accessed got revoked on both of my accounts and i lost data_df as session terminated
hubert_pred_logs = '/content/hubert_large_pre_logs.txt'
wavlm_pred_logs = "/content/wavlm_large_pre_logs.txt"

#we will read these txt files and get prediction score for each file form logs line (The similarity score between two audios is 0.5336 (-1.0, 1.0))

"""#### Evaluation  (EER)"""

import re

def read_file_into_list(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    return lines
hubert_pred_lines = read_file_into_list(hubert_pred_logs)
wemlm_pred_lines = read_file_into_list(wavlm_pred_logs)

hubert_pred_score = []
for line in hubert_pred_lines:
  if "similarity score between two audios" in line :
    sim_score = line.split('similarity score between two audios is ')[-1].split(' ')[0]
    hubert_pred_score.append(float(sim_score))
len(hubert_pred_score)

#making truth labels as i know that first 100 were 0 label and  next 100 were 1 label
hubert_true_score  = [0]*100 + [1]*100
len(hubert_true_score)

wavlm_pred_score = []
for line in wemlm_pred_lines:
  if "similarity score between two audios" in line :
    sim_score = line.split('similarity score between two audios is ')[-1].split(' ')[0]
    wavlm_pred_score.append(float(sim_score))
len(wavlm_pred_score)

#making truth labels as i know that first 100 were 0 label and  next 100 were 1 label,
# but pred run for only 126 files hence , 100 with 0 label and 26 with 1 label
wavlm_true_score  = [0]*100 + [1]*26
len(wavlm_true_score)

wavlm_pred_label = [ 0 if each < 0.5 else 1 for each in wavlm_pred_score]
hubert_pred_label = [ 0 if each < 0.5 else 1 for each in hubert_pred_score]

from sklearn.metrics import accuracy_score, precision_score, recall_score

def calculate_metrics(true_labels, predicted_labels):
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels)
    recall = recall_score(true_labels, predicted_labels)
    return accuracy, precision, recall

accuracy, precision, recall = calculate_metrics(wavlm_true_score, wavlm_pred_label)
print("Wavelm Large Accuracy:", accuracy)
print("Wavelm Large Precision:", precision)
print("Wavelm Large Recall:", recall)

accuracy, precision, recall = calculate_metrics(hubert_true_score, hubert_pred_label)
print("Hubert Large Accuracy:", accuracy)
print("Hubert Large Precision:", precision)
print("Hubert Large Recall:", recall)

import numpy as np
from sklearn.metrics import confusion_matrix

def calculate_far_frr(true_labels, similarity_scores, thresholds):
    eer = float('inf')
    eer_threshold = None
    far_frr = []

    for threshold in thresholds:
        # Calculate predictions based on the given threshold
        predictions = (similarity_scores >= threshold).astype(int)

        # Generate confusion matrix
        cm = confusion_matrix(true_labels, predictions)

        # Extract values from confusion matrix
        tn, fp, fn, tp = cm.ravel()

        # Calculate FAR and FRR
        far = fp / (fp + tn)
        frr = fn / (fn + tp)

        far_frr.append((threshold, far * 100, frr * 100))

        # Check if EER threshold needs to be updated
        if abs(far - frr) < eer:
            eer = abs(far - frr)
            eer_threshold = threshold

    return far_frr, eer_threshold

#true labels and similarity scores
true_labels = hubert_true_score
similarity_scores = hubert_pred_score

# Define a range of thresholds
thresholds = np.linspace(-1, 1, num=100)

# Calculate FAR, FRR, and EER
far_frr, eer_threshold = calculate_far_frr(true_labels, similarity_scores, thresholds)

print("Threshold\tFAR\t\tFRR")
for threshold, far, frr in far_frr:
  print("{:.4f}\t\t{:.2f}%\t\t{:.2f}%".format(threshold, far, frr))

print("\nEqual Error Rate (EER) Threshold:", eer_threshold)

# true labels and similarity scores
true_labels = wavlm_true_score
similarity_scores = wavlm_pred_score

# Define a range of thresholds
thresholds = np.linspace(-1, 1, num=100)

# Calculate FAR, FRR, and EER
far_frr, eer_threshold = calculate_far_frr(true_labels, similarity_scores, thresholds)

print("Threshold\tFAR\t\tFRR")
for threshold, far, frr in far_frr:
  print("{:.4f}\t\t{:.2f}%\t\t{:.2f}%".format(threshold, far, frr))

print("\nEqual Error Rate (EER) Threshold:", eer_threshold)

