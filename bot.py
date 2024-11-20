import discord
from discord.ext import tasks
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import asyncio

# Discord botのトークンを設定
TOKEN = 'abcdefgh123456789ijkl' #ここにbotのTokenを張り付ける
CHANNEL_ID = 12345678910111213  # ここに情報を送信したいチャンネルIDを張り付ける

# クライアントインスタンスを生成
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# 送信する時間のリスト（8:40, 9:00, ..., 21:40, 22:00）
SCHEDULED_TIMES = [
    (8, 40), (9, 0), (9, 20), (9, 40), (10, 0), (10, 20), (10, 40),
    (11, 0), (11, 20), (11, 40), (12, 0), (12, 20), (12, 40),
    (13, 0), (13, 20), (13, 40), (14, 0), (14, 20), (14, 40),
    (15, 0), (15, 20), (15, 40), (16, 0), (16, 20), (16, 40),
    (17, 0), (17, 20), (17, 40), (18, 0), (18, 20), (18, 40),
    (19, 0), (19, 20), (19, 40), (20, 0), (20, 20), (20, 40),
    (21, 0), (21, 20), (21, 40), (22, 0)
]


# データ取得関数
def get_attraction_status():
    disneyland_url = 'https://tokyodisneyresort.info/realtime.php?park=land&order=area'
    disneysea_url = 'https://tokyodisneyresort.info/realtime.php?park=sea&order=area'

    def fetch_data(park_name, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        names = [name.text.strip() for name in soup.find_all("div", class_="realtime-attr-name")]
        times = []
        for time in soup.find_all("div", class_="realtime-attr-condition"):
            greeting_timetable = time.find("div", class_="greeting_timetable")
            if greeting_timetable:
                greeting_timetable.extract()
            times.append(time.text.strip())
        attractions = [{"name": name, "status": time} for name, time in zip(names, times)]
        return {"park": park_name, "attractions": attractions}

    # 各パークのデータ取得
    disneyland_data = fetch_data("ディズニーランド", disneyland_url)
    disneysea_data = fetch_data("ディズニーシー", disneysea_url)
    output = {"parks": [disneyland_data, disneysea_data]}

    # JSONファイルをクリアしてからデータを書き込み
    with open("disney_attractions_status.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return output

# データ読み込み関数
def load_attraction_status():
    try:
        with open("disney_attractions_status.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("JSONファイルが見つかりません")
        return None

# アトラクション情報をDiscordに送信
async def send_attractions(channel):
    data = load_attraction_status()
    if data is None:
        await channel.send("アトラクション情報の読み込みに失敗しました。")
        return

    now_time = datetime.now().strftime("%H時%M分")  # 現在の時刻を取得してタイトルに使用

    for park_data in data["parks"]:
        message = f"# {now_time}の{park_data['park']}\n\n"
        for attraction in park_data["attractions"]:
            message += f"**{attraction['name']}**\n{attraction['status']}\n\n"
        
        # メッセージをチャンネルに送信
        await channel.send(message)

    # 最後のスクレイピング時刻をステータスに反映
    await client.change_presence(activity=discord.Game(name=f"最終スクレイピング時刻: {now_time}"))

# Bot初回起動時の処理
@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

    # 初回スクレイピングとJSON保存
    get_attraction_status()
    
    # 最終スクレイピング時刻をステータスに反映
    now = datetime.now().strftime("%H時%M分")
    await client.change_presence(activity=discord.Game(name=f"最終スクレイピング時刻: {now}"))

    # 初回起動完了メッセージを送信
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=discord.Embed(title="初回起動完了"))
        await channel.send(embed=discord.Embed(title="初回スクレイピング完了"))

    # スケジュールタスク開始
    scheduled_task.start()

# 毎分実行して時間チェック
@tasks.loop(minutes=1)
async def scheduled_task():
    now = datetime.now()
    current_time = (now.hour, now.minute)

    # 現在の時刻が指定した送信時間に一致しているか確認
    if current_time in SCHEDULED_TIMES:
        # スクレイピングを再実行して最新データを取得・保存
        get_attraction_status()
        
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await send_attractions(channel)
            
# Botを実行
client.run(TOKEN)
