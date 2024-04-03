## Authore M22AIE227
#this code is initally implemented in Google Colab that can also be accessed using  this link
#https://colab.research.google.com/drive/1H08QkulLflKnuvNL_yLRRZvmYbAmlaJn?usp=sharing


#### git clone LibriMix Repo
"""

!git clone https://github.com/JorisCos/LibriMix

"""#### Update Script for test-clean"""

# keeping only mixing for test-clean subset, hence removing script for dev-clean, train-clen etc.
#below commented script is updated to generate_librimix.sh file

# # /content/LibriMix/generate_librimix.sh
# #!/bin/bash
# set -eu  # Exit on error

# storage_dir=$1
# librispeech_dir=$storage_dir/LibriSpeech
# wham_dir=$storage_dir/wham_noise
# librimix_outdir=$storage_dir/

# function LibriSpeech_test_clean() {
# 	if ! test -e $librispeech_dir/test-clean; then
# 		echo "Download LibriSpeech/test-clean into $storage_dir"
# 		# If downloading stalls for more than 20s, relaunch from previous state.
# 		wget -c --tries=0 --read-timeout=20 http://www.openslr.org/resources/12/test-clean.tar.gz -P $storage_dir
# 		tar -xzf $storage_dir/test-clean.tar.gz -C $storage_dir
# 		rm -rf $storage_dir/test-clean.tar.gz
# 	fi
# }

# function wham() {
# 	if ! test -e $wham_dir; then
# 		echo "Download wham_noise into $storage_dir"
# 		# If downloading stalls for more than 20s, relaunch from previous state.
# 		wget -c --tries=0 --read-timeout=20 https://my-bucket-a8b4b49c25c811ee9a7e8bba05fa24c7.s3.amazonaws.com/wham_noise.zip -P $storage_dir
# 		unzip -qn $storage_dir/wham_noise.zip -d $storage_dir
# 		rm -rf $storage_dir/wham_noise.zip
# 	fi
# }

# LibriSpeech_test_clean &
# wham &

# wait

#

"""#### Install SoX , soundfile etc requirements"""

!apt-get install sox

!pip install soundfile==0.10.3.post1

"""#### Update Repo code to mix only test-clean"""

# Commented out IPython magic to ensure Python compatibility.
!mkdir /content/data
storage_dir = '/content/data'
# %cd /content/LibriMix

"""##### changge directory permission for execution"""

!ls -l generate_librimix.sh

!chmod +x generate_librimix.sh

!chmod +x scripts/create_librimix_from_metadata.py

!find /content/LibriMix -type f -exec chmod +x {} +

"""##### Updating Repo code"""

#only kept test-clean.csv in metadata/LibriSpeech and deleted other csv files
#only kept libri2mix_test-clean and its info .csv files and storage info txt and deleted other csv files

# added below comenetd line at line 68 in create_librimix_from_metadata.py
# md_filename_list = [f for f in md_filename_list if 'ipynb_checkpoints' not in f]

"""#### Run updated Script that download test-clean and mix it using create_librimix_from_metadata.py"""

# executiong generate_librimix.sh script that will download librimix test-clean dataset and wham noise
#will  execute create_librimix_from_metadata.py sepratly

!./generate_librimix.sh storage_dir

#I have executed create_librimix_from_metadata.py with n_src eqaul to 2, and kept all other satting intact, hence
#kept both freq 8k & 16k, also both mode min & max
#and all three type type of mixture : mix_clean (utterances only) mix_both (utterances + noise) mix_single (1 utterance + noise)
#But actually we need to add 2 clean signal into one  only  hence in next part i only zipped and stored results of mix_clean type of mixutre
#for 8k freq in max mode.

n_src = 2
librispeech_dir = '/content/LibriMix/storage_dir/LibriSpeech'
wham_dir = '/content/LibriMix/storage_dir/wham_noise'
librimix_outdir = '/content/LibriMix/storage_dir/'
metadata_dir="metadata/Libri2Mix"
!python scripts/create_librimix_from_metadata.py --librispeech_dir $librispeech_dir \
  --wham_dir $wham_dir \
  --metadata_dir $metadata_dir \
  --librimix_outdir $librimix_outdir \
  --n_src $n_src \
  --freqs 8k 16k \
  --modes min max \
  --types mix_clean mix_both mix_single

"""#### ZIP mixed dataset and store it for further use"""

libri2mix_dataset_path = '/content/LibriMix/storage_dir/Libri2Mix'

!zip -r /content/libri2mix_dataset.zip '/content/LibriMix/storage_dir/Libri2Mix'

#when we mix for all possible scenerio like 8k/16k, min/max and all three types -- then resultant is 9gb data in zip format

import glob
len(glob.glob('/content/LibriMix/storage_dir/Libri2Mix/wav8k/max/test/mix_clean/*.wav'))

!zip -r /content/libri2mix_test_clean_8k_max_mix_clean.zip '/content/LibriMix/storage_dir/Libri2Mix/wav8k/max/test/mix_clean'

#where as for our purpose we need to do only one type that is mix clean (mixing 2 clean speaker together)
# that also i hv done for 8k and in max mode on test_clean dataset resulting in yoyal 3000 wav files
# and in zip format it is of 320 mb size

