# sasWrapperPy
WSL でコマンドにより SAS を動かすための Wrapper です。

# 機能
### sas プログラムの実行
```bash
$ sas -i example.sas
```

### sas データセット（.sas7bdat）の CSV ファイルへの変換
```bash
$ sas -i data.sas7bdat
```

# 使用方法
### 1. 依存ライブラリのインストール
```bash
$ pip install -r requirements.txt
```

### 2. バイナリの生成
```bash
$ python3 setup.py build
```

### 3. 実行準備
- sas.ini ファイルに、WSL でマウントしている windows ホスト における sas.exe ファイルのパスを記述
```sas.ini
[GENERAL]
sas_path=/mnt/c/'Program Files'/SASHome/SASFoundation/'9.4'
```

- sas.ini ファイルをバイナリと同じディレクトリへコピー
```bash
$ cp sasWrapperPy/sasWrapperPy/sas.ini sasWrapperPy/build/exe.linux-x86_64-3.6/
```

- バイナリのパスを通す
```bash
$ echo export PATH="${HOME}/sasWrapperPy/sasWrapperPy/sas.ini sasWrapperPy/build/exe.linux-x86_64-3.6/:$PATH" >> ~/.bashrc
$ source ~/.bashrc
```
