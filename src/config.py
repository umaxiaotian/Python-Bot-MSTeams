#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class DefaultConfig:
    """ Bot Configuration """
    PORT = os.getenv("PORT", 8080)
    APP_ID = os.getenv("MICROSOFT_APP_ID")
    APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")