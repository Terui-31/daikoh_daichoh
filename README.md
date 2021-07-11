# daikoh_daichoh

## Introduction
工事写真台帳を自動作成するツール（Beta）

## Quick Start
1. ダウンロード
```
git clone https://github.com/Terui-31/daikoh_daichoh.git
```
2. 仮想環境構築
```
conda create conda create -n daikoh_daichoh python=3.7.10
```
3. 必要なライブラリのインストール
```
pip install -r requirements.txt
```
4. data ディレクトリに .jpg ファイルを入れる

5. weights 直下に移動
```
cd weights
```
6. weights のダウンロード

##### download wieghts for classifier
```
wget "https://drive.google.com/uc?export=download&id=1ShoR4shnmNFY85YUyB5-hddSw7Qr9NEG" -O classifier_weight_ver07-02.h5
```
##### detector weight for detector
```
wget "https://drive.google.com/uc?export=download&id=1V_3fyxIo9QtCxWO9trpxE8YJcImskfB0" -O detecter_weight.h5
```
7. daikoh_daichoh 直下に移動
```
cd ..
```
8. 実行
```
python main.py
```
9. outディレクトリに xlsx が入る




