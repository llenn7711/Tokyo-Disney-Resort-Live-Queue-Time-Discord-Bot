# Tokyo-Disney-Resort-Live-Queue-Time-Discord-Bot
東京ディズニーランドと東京ディズニーシーのアトラクション名とQラインのリアルタイム待ち時間をdiscordに送信します。

## Botについて
- [Tokyo-Disney-Resort-Live-Queue-Time](https://github.com/llenn7711/Tokyo-Disney-Resort-Live-Queue-Time)をもとに作成しました。

- 8:40～22:00まで20分間隔で指定したチャンネルに東京ディズニーランドと東京ディズニーシーのアトラクション待ち時間を送信します。
  これはBot.py内の```CHEDULED_TIMES```を変更することで送信する時刻を変更できます。

- Botのスタッツにスクレイピングを実施した時刻を表示します。

## 仕様
### Discord Botアカウントの作成
- [Discord Developer Portal](https://discord.com/developers/applications)よりBotアカウントを作成します。

### コードの書き換え
- 10行目 ```TOKEN```を使用したいBotのTokenに置き換えます。
- 11行目 ```CHANNEL_ID```をメッセージを送信したいチャンネルのチャンネルIDに置き換えます。
  
### インストール
- Python 3.x
- 必要なライブラリのインストール
- discord.py
   詳しくは[Discord.py](https://github.com/Rapptz/discord.py)
  
```
py -3 -m pip install -U discord.py
```

  - requests
  - beautifulsoup4

```
pip install requests beautifulsoup4
```

### プログラムの実行

```
python bot.py
```

### 注意
- スクレイピングを使用しています

## 引用
ディズニーランドのアトラクション待ち時間

[ディズニーランド](https://tokyodisneyresort.info/realtime.php?park=land&order=area)

ディズニーシーのアトラクション待ち時間

[ディズニーシー](https://tokyodisneyresort.info/realtime.php?park=sea&order=area)
