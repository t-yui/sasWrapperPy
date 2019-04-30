# sasWrapperPy
WSL でコマンドにより SAS を動かすための Wrapper です。

## システム要件
- Windows 10
- ubuntu on Windows Subsystem for Linux
- SAS >= 9.4 on Windows
- python3 and pip3 installed in wsl ubuntu

## 機能
### SAS プログラム（.sas）の実行
```bash
$ sas -i example.sas [-l <logfile>] [-o <outfile>]
```

- オプション
    - `-i` : [必須] .sas ファイル名とパスを指定（相対パスでも可）
    - `-l` : .log ファイル（SAS のログファイル）名とパスを指定（フルパスで記述）
    - `-o` : .lst ファイル（SAS の出力ファイル）名とパスを指定（フルパスで記述）

### SAS データセット（.sas7bdat）の CSV ファイルへの変換
```bash
$ sas -i data.sas7bdat
```

- オプション
    - `-i` : [必須] .sas7bdat ファイル名とパスを指定（相対パスでも可）

### SAS 出力ファイル（.log, .lst）の文字コード変換
```bash
$ sas -i output.log [-e <encode>]
```

- オプション
    - `-i` : [必須] .log または .lst ファイル名とパスを指定（相対パスでも可）
    - `-e` : 変換後の文字コードを以下より指定
        - `utf-8`（デフォルト）
        - `shift-jis`

### SAS Help（documentation）の表示
```bash
$ sas -d
```

## 使用方法
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
