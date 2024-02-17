#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime

from fastapi import FastAPI, Request, Response
from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter
from botbuilder.schema import Activity, ActivityTypes

from src.bot import MyBot
from src.config import DefaultConfig

# 設定を読み込む
CONFIG = DefaultConfig()

# 与えられた設定でアダプターを作成
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# エラーハンドリング
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] 処理されなかったエラー: {error}", file=sys.stderr)
    traceback.print_exc()

    # ユーザーにエラーを通知
    await context.send_activity("ボットがエラーまたはバグに遭遇しました。")
    await context.send_activity("このボットを実行し続けるには、ボットのソースコードを修正してください。")

    # エミュレーターと通信している場合はトレースアクティビティを送信
    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)

# エラーハンドラーをアダプターに割り当てる
ADAPTER.on_turn_error = on_error

# ボットを作成
BOT = MyBot()

# FastAPIアプリを作成
app = FastAPI()

@app.post("/api/messages")
async def messages(req: Request) -> Response:
    if "application/json" in req.headers["content-type"]:
        body = await req.json()
    else:
        return Response(status_code=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return Response(content=response.body, status_code=response.status)
    return Response(status_code=201)

@app.get("/")
async def hello() -> Response:
    return Response(content="Hello ObaBot!", status_code=200)
