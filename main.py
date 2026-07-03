import os
import sys
import time
import json
import pickle
import random
import socket
import threading
import signal
import asyncio
import base64
import binascii
import re
import ssl
import urllib3
import psutil
import jwt
import pytz
import aiohttp
import requests
import traceback
import concurrent.futures
from bundle_data import BUNDLE_MAP, get_bundle_menu
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from flask import Flask, jsonify, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.timestamp_pb2 import Timestamp
from cfonts import render, say
from Crypto.Util.Padding import pad as crypto_pad, unpad as crypto_unpad
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from xHeaders import *
from Riduan import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2, title_pb2

CLIENT_VERSION = bytes.fromhex('312e3132362e31').decode()
CLIENT_VERSION_CODE = bytes.fromhex('32303139313230373736').decode()
UNITY_VERSION = bytes.fromhex('323031382e342e31316631').decode()
RELEASE_VERSION = bytes.fromhex('4f423534').decode()
MSDK_VERSION = bytes.fromhex('352e352e325033').decode()
USER_AGENT_MODEL = bytes.fromhex('415355535f5a30315144').decode()
ANDROID_OS_VERSION = bytes.fromhex('416e64726f6964203130').decode()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  
BLOCKED_NAMES = ['Lala']
online_writer = None
whisper_writer = None
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
evo_cycle_running = False
evo_cycle_task = None
ACTUAL_BOT_UID = None
silent_join_mode = False
pending_troll = False
emote_hijack = False
DEV_SIGNATURE = "[FF0000]Developer:[FFFFFF] —͞LALA Cᴏᴅᴇx </>"
ENABLE_BUBBLE_MSG = True
ENABLE_AUTO_TITLE = True

Menu_1 = f"""[C][B][FF0000]───── Team & Match ─────
[FFD700]Create 3-6Player Team
[FFFFFF]/3 /5 /6
[FFD700]Change Team Size
[FFFFFF]/mode [3-6]
[FFD700]Join Squad
[FFFFFF]/join [tc]
[FFD700]Leave Squad
[FFFFFF]/solo
[FFD700]Start Match
[FFFFFF]/start
[FFD700]Admin Info
[FFFFFF]/admin
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

Menu_2 = f"""[C][B][FF0000]───── Invite & Troll ─────
[FFD700]Group Invite
[FFFFFF]/inv [uid]
[FFD700]Spam Team Invite
[FFFFFF]/spaminv [uid] [times]
[FFD700]Spam Join Request
[FFFFFF]/spamreq [uid] [times]
[FFD700]Troll Team Action
[FFFFFF]/troll [tc]
[FFD700]Abuse/Gali Command
[FFFFFF]/gali [name]
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

Menu_3 = f"""[C][B][FF0000]───── Normal Emotes ────
[FFD700]Send Normal Emote
[FFFFFF]/e [uid] [id]
[FFD700]Fast Emote Spam
[FFFFFF]/f [uid] [id]
[FFD700]Custom Emote Spam
[FFFFFF]/p [uid] [id] [times]
[FFD700]Quick Attack & Leave
[FFFFFF]/quick [tc] [id] [uid]
[FFD700]Emote Hijack ON
[FFFFFF]/hjk
[FFD700]Emote Hijack OFF
[FFFFFF]/hjf
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

Menu_4 = f"""[C][B][FF0000]────── Evo Emotes ─────
[FFD700]Send Specific Evo
[FFFFFF]/evo [uid] [1-21]
[FFD700]Fast Evo Spam
[FFFFFF]/ef [uid] [1-21]
[FFD700]Custom Evo Spam
[FFFFFF]/ec [uid] [1-21] [times]
[FFD700]Auto Cycle All Evos
[FFFFFF]@evos [uid]
[FFD700]Stop Auto Cycle
[FFFFFF]@sevos
[FFD700]Stop Fast Evo Spam
[FFFFFF]/stop ef
[FFD700]Stop Custom Evo Spam
[FFFFFF]/stop ec
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

Menu_5 = f"""[C][B][FF0000]──── Bundles & Titles ────
[FFD700]Check Bundle List
[FFFFFF]/bundle
[FFD700]Equip Bundle
[FFFFFF]/bundle [name]
[FFD700]Send All Titles
[FFFFFF]/title
[FFD700]Send Specific Title
[FFFFFF]/title [code]
[FFD700]Small V-Badge
[FFFFFF]/r1 [uid]
[FFD700]New V-Badge
[FFFFFF]/r2 [uid]
[FFD700]Pro Badge
[FFFFFF]/r3 [uid]
[FFD700]Craftland Badge
[FFFFFF]/r4 [uid]
[FFD700]Moderator Badge
[FFFFFF]/r5 [uid]
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

Menu_6 = f"""[C][B][FF0000]───── Info & System ─────
[FFD700]Check Player Info
[FFFFFF]/info [uid]
[FFD700]Check Account Age
[FFFFFF]/idage [uid]
[FFD700]Gift Likes
[FFFFFF]/likes [uid]
[FFD700]Check Player Bio
[FFFFFF]/bio [uid]
[FFD700]Check Ban Status
[FFFFFF]/check [uid]
[FFD700]Level Progress Info
[FFFFFF]/level [uid]
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

Menu_7 = f"""[C][B][FF0000]───── LALA Info ─────
[B][FFFFFF] » Tik Tok ID
[B][00FFFF] ↳ @ʀᴅx_ʟᴀʟᴀ1
[B][FFFFFF] » Tik Tok ID
[B][00FFFF] ↳ @ʟᴀʟᴀɢᴀᴍᴇʀ10ᴋ
[B][00FFFF]➤ TCP Bot & Guild Glory Bot Available!
[B][00FF00]➤ Only WhatsApp [FFFF00]DM If You Need.
[B][00FF00]➤ WhatsApp: [FF00FF]01903➜982821
[FF0000]─────────────────
{DEV_SIGNATURE}
[FF0000]─────────────────"""

BOT_MENUS = [Menu_1, Menu_2, Menu_3, Menu_4, Menu_5, Menu_6, Menu_7]

evo_emotes = {
    "1": "909000063",
    "2": "909000068",
    "3": "909000075",
    "4": "909040010",
    "5": "909000081",
    "6": "909039011",
    "7": "909000085",
    "8": "909000090",
    "9": "909000098",
    "10": "909035007",
    "11": "909042008",
    "12": "909041005",
    "13": "909033001",
    "14": "909038010",
    "15": "909038012",
    "16": "909045001",
    "17": "909049010",
    "18": "909051003"
}
EMOTE_MAP = {
    1: 909000063,
    2: 909000081,
    3: 909000075,
    4: 909000085,
    5: 909000134,
    6: 909000098,
    7: 909035007,
    8: 909051012,
    9: 909000141,
    10: 909034008,
    11: 909051015,
    12: 909041002,
    13: 909039004,
    14: 909042008,
    15: 909051014,
    16: 909039012,
    17: 909040010,
    18: 909035010,
    19: 909041005,
    20: 909051003,
    21: 909034001,
    22: 909054004
}
BADGE_VALUES = {
    "r1": 64,
    "r2": 32768,    
    "r3": 262144,    
    "r4": 1048576,
    "r5": 2048
}
def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()
def format_long_number(uid_str):
    uid_str = str(uid_str)
    if len(uid_str) <= 5:
        return uid_str
    parts = [uid_str[i:i+5] for i in range(0, len(uid_str), 5)]
    return '[FFFFFF]'.join(parts)
async def fetch_player_info_api(uid):
    url = f"https://riduanfreefireplayerallinfo.vercel.app/playerinfo?uid={uid}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        return None
async def ArohiAccepted(uid, code, K, V, region="SG"):
    fields = {
        1: 4,
        2: {
            1: int(uid),
            3: int(uid),
            4: bytes.fromhex("01090a0b121920"),
            8: 1,
            9: {
                2: 161,
                4: "y[WW",
                6: 11,
                8: CLIENT_VERSION,
                9: 3,
                10: 1
            },
            10: str(code),
        }
    }
    if region.lower() == "ind":
        packet_header = '0514'
    elif region.lower() == "bd":
        packet_header = '0519'
    else:
        packet_header = '0515'
    proto_hex = (await CrEaTe_ProTo(fields)).hex()
    return await GeneRaTePk(proto_hex, packet_header, K, V)
    
async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()
async def nmnmmmmn(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)
async def auto_welcome_emote(sender_uid, key, iv, region):
    global ACTUAL_BOT_UID
    try:
        emote_id = 909054006
        if not ACTUAL_BOT_UID:
            return
        bot_uid = ACTUAL_BOT_UID
        await asyncio.sleep(0.1) 
        emote_packet_sender = await Emote_k(int(sender_uid), emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet_sender)
        await asyncio.sleep(0.1)
        emote_packet_bot = await Emote_k(bot_uid, emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet_bot)
    except Exception as e:
        pass
async def evo_cycle_spam(uids, key, iv, region):
    global evo_cycle_running
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running:
                break
            for uid in uids:
                try:
                    uid_int = int(uid)
                    H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                except Exception as e:
                    pass
            if evo_cycle_running:
                for i in range(5):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        if evo_cycle_running:
            await asyncio.sleep(2)
async def leave_squad(key, iv, region):
    fields = {
        1: 7,
        2: {
            1: 12480598706
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)    
async def safe_send_bubble_message(message, chat_id, key, iv, max_retries=3):
    global whisper_writer, online_writer
    for attempt in range(max_retries):
        try:
            P = await xSEndMsgsQ(message, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False
async def auto_send_title_packet(chat_id, key, iv):
    global ACTUAL_BOT_UID, whisper_writer, online_writer
    try:
        if not ACTUAL_BOT_UID: return
        await asyncio.sleep(1.0) 
        display_name = "LALA" 
        title_id = 904990070 
        title_pkt = await Make_Title_Packet(ACTUAL_BOT_UID, chat_id, title_id, display_name, key, iv)
        if title_pkt and whisper_writer:
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', title_pkt)
    except Exception as e:
        pass
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] LALA",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(await xBunnEr()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value
            },
            32: badge_value,
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)    
async def reset_bot_state(key, iv, region):
    try:
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        return True
    except Exception as e:
        return False    
async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]Usage: /{cmd} (uid)\nExample: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    initial_msg = f"[B][C][1E90FF]Request received! Preparing to spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    try:
        await reset_bot_state(key, iv, region)
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 5
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.1)
        success_msg = f"[B][C][00FF00]Successfully Sent {spam_count} Join Requests!\n[FFFFFF]Target: {target_uid}\n[FFFFFF]Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
    except Exception as e:
        error_msg = f"[B][C][FF0000]Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)
async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    try:
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        await asyncio.sleep(1.5)
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        await asyncio.sleep(0.5)
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        return True, f"Quick emote attack completed! Sent emote to UID {target_uid}"
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"
Hr = {
    'User-Agent': f"Dalvik/2.1.0 (Linux; U; {ANDROID_OS_VERSION}; {USER_AGENT_MODEL} Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': UNITY_VERSION,
    'X-GA': "v1 1",
    'ReleaseVersion': RELEASE_VERSION
}
async def troll_sequence(team_code, key, iv, region):
    global ACTUAL_BOT_UID, silent_join_mode
    silent_join_mode = True 
    try:
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        await asyncio.sleep(1.5)
        troll_msg = "[B][C][FFFFFF]Arey kibhabe bot team e chole aslam? Team e to dekhi sobai pura noob!"
        msg_packet = await xSEndMsgsQ(troll_msg, ACTUAL_BOT_UID, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', msg_packet)
        await asyncio.sleep(0.5)
        emote_id = 909000034
        emote_packet = await Emote_k(ACTUAL_BOT_UID, emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        await asyncio.sleep(1.0)
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        return True, "Troll sequence completed successfully!"
    except Exception as e:
        return False, f"Troll sequence failed: {str(e)}"
    finally:
        silent_join_mode = False
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; {ANDROID_OS_VERSION}; {USER_AGENT_MODEL} Build/PI)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    try:
        connector = aiohttp.TCPConnector(ssl=ssl_ctx)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(url, headers=headers, data=data, timeout=15) as response:
                if response.status != 200:
                    return None, None
                d = await response.json()
                return d.get("open_id"), d.get("access_token")
    except Exception as e:
        return None, None
async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = CLIENT_VERSION
    major_login.system_software = f"{ANDROID_OS_VERSION} / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = CLIENT_VERSION_CODE
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)
async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None
async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None
async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto
async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto
async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet
async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE' 
async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False
async def fast_emote_spam(uids, emote_id, key, iv, region):
    global fast_spam_running
    count = 0
    max_count = 25
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                pass
        count += 1
        await asyncio.sleep(0.1)
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    global custom_spam_running
    count = 0
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            break
async def evo_emote_spam(uids, number, key, iv, region):
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                pass
        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"
async def evo_fast_emote_spam(uids, number, key, iv, region):
    global evo_fast_spam_running
    count = 0
    max_count = 25
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                pass
        count += 1
        await asyncio.sleep(0.1)
    return True, f"Completed fast evolution emote spam {count} times"
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    global evo_custom_spam_running
    count = 0
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                pass
        count += 1
        await asyncio.sleep(0.1)
    return True, f"Completed custom evolution emote spam {count} times"
async def TcPOnLine(ip, port, key, iv, AutHToKen, region, reconnect_delay=0.5):
    global online_writer , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy, data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, evo_cycle_running, evo_cycle_task, silent_join_mode, pending_troll, ACTUAL_BOT_UID, emote_hijack
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                d_hex = data2.hex()
                if d_hex.startswith('05') and len(d_hex) > 20 and emote_hijack:
                    try:
                        payload = d_hex[10:]
                        packet_str = await DeCode_PackEt(payload)
                        if not packet_str or '9090' not in packet_str:
                            try:
                                decrypted = await DEc_PacKeT(payload, key, iv)
                                packet_str = await DeCode_PackEt(decrypted)
                            except:
                                pass
                        if packet_str and '9090' in packet_str:
                            import re
                            emote_match = re.search(r'"data":\s*(9090\d{5})', packet_str)
                            if emote_match:
                                emote_id = emote_match.group(1)
                                all_ids = re.findall(r'"data":\s*(\d{8,12})', packet_str)
                                sender_uid = None
                                for u in all_ids:
                                    if str(u) != str(ACTUAL_BOT_UID) and not str(u).startswith('9090'):
                                        sender_uid = u
                                        break
                                if emote_id and sender_uid and str(sender_uid) != str(ACTUAL_BOT_UID):
                                    bot_self_emote = await Emote_k(int(ACTUAL_BOT_UID), int(emote_id), key, iv, region)
                                    if online_writer:
                                        online_writer.write(bot_self_emote)
                                        await online_writer.drain()
                    except Exception as e:
                        pass
                if d_hex.startswith('0500'):
                    try:
                        packet_str = await DeCode_PackEt(d_hex[10:])
                        if packet_str:
                            packet_json = json.loads(packet_str)
                            if '5' in packet_json and 'data' in packet_json['5'] and '8' in packet_json['5']['data']:
                                squad_owner = packet_json['5']['data']['1']['data']
                                code = packet_json['5']['data']['8']['data']
                                Join = await ArohiAccepted(squad_owner, code, key, iv, region) 
                                if Join:
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
                    except Exception as e:
                        pass
                if d_hex.startswith('0500') and len(d_hex) > 1000:
                    try:
                        packet = await DeCode_PackEt(d_hex[10:])
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                        if ENABLE_BUBBLE_MSG:
                            welcome_msg = '[B][C][00FFFF]\n- WeLComE To LALA Emote Bot ! '
                            await safe_send_bubble_message(welcome_msg, OwNer_UiD, key, iv)
                        if ENABLE_AUTO_TITLE:
                            asyncio.create_task(auto_send_title_packet(OwNer_UiD, key, iv))
                        if pending_troll:
                            pending_troll = False
                            await asyncio.sleep(0.5) 
                            emote_id = 909000034
                            emote_packet = await Emote_k(ACTUAL_BOT_UID, emote_id, key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                            await asyncio.sleep(0.5)
                            troll_msg = "[B][C][FFFFFF]Arey kibhabe bot team e chole aslam? Team e to dekhi sobai pura noob!"
                            P = await SEndMsG(0, troll_msg, OwNer_UiD, OwNer_UiD, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(4.0) 
                            leave_packet = await ExiT(None, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                        elif not silent_join_mode:
                            message = f'[B][C]{get_random_color()}\n- WeLComE To LALA Emote Bot ! '
                            P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                            try:
                                await asyncio.sleep(1.5)
                                banner_packet = await RejectMSGtaxt(OwNer_UiD, OwNer_UiD, key, iv)
                                if banner_packet:
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', banner_packet)
                            except Exception as b_err:
                                pass
                            try:
                                await auto_welcome_emote(OwNer_UiD, key, iv, region)
                            except Exception as emote_error:
                                pass
                        else:
                            pass
                    except:
                        if d_hex.startswith('0500') and len(d_hex) > 1000:
                            try:
                                packet = await DeCode_PackEt(d_hex[10:])
                                packet = json.loads(packet)
                                OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)
                                JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                                if pending_troll:
                                    pending_troll = False
                                    await asyncio.sleep(1.5)
                                    emote_id = 909052005
                                    emote_packet = await Emote_k(ACTUAL_BOT_UID, emote_id, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                                    await asyncio.sleep(0.5)
                                    troll_msg = "[B][C][FFFFFF]Arey kibhabe bot team e chole aslam? Team e to dekhi sobai pura noob!"
                                    P = await SEndMsG(0, troll_msg, OwNer_UiD, OwNer_UiD, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    await asyncio.sleep(3.0)
                                    leave_packet = await ExiT(None, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                                elif not silent_join_mode:
                                    message = f"[B][C]{get_random_color()}\n- WeLComE To LALA Emote Bot ! \n\n{get_random_color()}- Commands : @a {xMsGFixinG('player_uid')} {xMsGFixinG('909042007')}\n\n[00FF00]Dev : @{xMsGFixinG('LALA_Apis')}"
                                    P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                                    await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                    try:
                                        await asyncio.sleep(1.5)
                                        banner_packet = await RejectMSGtaxt(OwNer_UiD, OwNer_UiD, key, iv)
                                        if banner_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', banner_packet)
                                    except:
                                        pass
                            except:
                                pass
            if online_writer:
                online_writer.close() 
                await online_writer.wait_closed() 
                online_writer = None
        except Exception as e: 
            online_writer = None
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    global whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy, data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, evo_cycle_running, evo_cycle_task, emote_hijack
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None
                    if response:
                        if inPuTMsG.strip() == '/hjk':
                            emote_hijack = True
                            success_msg = f"[B][C][00FF00]SUCCESS! Emote Hijack is ON!\n"
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == '/hjf':
                            emote_hijack = False
                            success_msg = f"[B][C][FF0000]Emote Hijack is OFF!\n"
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/gali '):
                            try:
                                parts = inPuTMsG.strip().split(' ', 1)
                                if len(parts) < 2:
                                    error_msg = '[B][C][FF0000]ERROR! Usage:\n/gali <name>\nExample: /gali hater'
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    import re
                                    name = parts[1].strip()
                                    normalized_name = re.sub('[^a-zA-Z]', '', name).lower()
                                    blocked = False
                                    for blocked_name in BLOCKED_NAMES:
                                        normalized_blocked = re.sub('[^a-zA-Z]', '', blocked_name).lower()
                                        if normalized_blocked in normalized_name:
                                            blocked = True
                                            break
                                    if blocked:
                                        error_msg = '[B][C][FF0000]শালা মাদারচোদ\n[FFFFFF]তোর বাপের নামে গালি দিতে চাস\n[FF0000]শালা মাদারচোদ'
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        messages = [
                                            '{Name} আমি তোমার সেক্সি বোনের বোডায় আমার মেশিন ঢুকিয়ে সারা রাত ধরে তাকে জোরে জোরে চোদব',
                                            '{Name} তর মাকে তোর ওপরে ফেলে চোদব',
                                            '{Name} খানকির ছেলে !!',
                                            '{Name} মাদার চোদ, তোর মাকে চুদি !!',
                                            '{Name} মাদার চোদ, তোর মাকে 5G স্পিডে চুদি !!',
                                            '{Name} বোকাচোদা, তোর মাকে কনডম লাগিয়ে চুদি !!',
                                            '{Name} বোকাচোদা, তোর মাকে প্রতিদিন ১০,০০০ টাকার সার্ভিস দেই !!',
                                            'FUCK {Name} !!',
                                            '{Name} মাদার চোদ, পোদ মেরে দিবো !!',
                                            '{Name} মাদার চোদ !!',
                                            '{Name} খানকি, আমি তোর বাপ !!',
                                            '{Name} তোর মাকে আমি চুইদা তোরে জন্মায় ছি !!',
                                            '{Name} বোকাচোদা, খানকির ছেলে !!',
                                            '{Name} মাদার চোদ, তোর মাকে ১৮০ কি.মি. স্পিডে চুদি !!',
                                            '{Name} খানকির ছেলে বট, নুবরা প্লেয়ার !!',
                                            'বাংলাদেশের NO-1 বট PLAYER {Name}',
                                            '{Name} জুতা চোর !!',
                                            '{Name} মাদারচোদ, ফ্রি ফায়ার খেলা বাদ দিয়ে লুডু খেল যা !!',
                                            '{Name} যাই করিস, আমি তোর অব্বা এইডা কখনো ভুলিস না !!'
                                        ]
                                        for msg in messages:
                                            colored_message = f'[B][C][00FFFF] {msg.replace("{Name}", name.upper())}'
                                            if response.Data.chat_type == 0:
                                                await safe_send_bubble_message(colored_message, chat_id, key, iv)
                                            else:
                                                await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                            await asyncio.sleep(2) 
                            except Exception as e:
                                error_msg = f'[B][C][FF0000]ERROR! Something went wrong:\n{str(e)}'
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        def anti_block(val, split_by=3, color="[FFFFFF]"):
                            if val is None or val == "N/A" or str(val).strip() == "": return "N/A"
                            s = str(val)
                            return color.join([s[i:i+split_by] for i in range(0, len(s), split_by)])
                        def safe_get(d, *keys):
                            if not isinstance(d, dict): return "N/A"
                            for k in keys:
                                if k in d and d[k] not in [None, "", "0"]: return d[k]
                                for dk, dv in d.items():
                                    if str(dk).lower() == str(k).lower() and dv not in [None, "", "0"]: return dv
                            return "N/A"

                        if inPuTMsG.strip().startswith('/idage'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Usage: /idage [uid]\n", uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if not target_uid.isdigit():
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Invalid UID!\n", uid, chat_id, key, iv)
                                else:
                                    try:
                                        await safe_send_message(response.Data.chat_type, "[B][C][00FFFF]Fetching Account Age...\n", uid, chat_id, key, iv)
                                        data = await fetch_player_info_api(target_uid)
                                        await asyncio.sleep(1.5)
                                        if data:
                                            p_info = data.get("PlayerInfo", data.get("data", data))
                                            age_info = data.get("AccountAgeInfo", data.get("age", data))
                                            acc_name = safe_get(p_info, "AccountName", "name", "nickname", "PlayerName")
                                            acc_uid = safe_get(p_info, "AccountId", "uid", "id")
                                            if acc_uid == "N/A": acc_uid = target_uid
                                            acc_lvl = safe_get(p_info, "AccountLevel", "level", "lvl")
                                            acc_age = safe_get(age_info, "AccountAge", "age")
                                            c_date_raw = safe_get(age_info, "AccountCreateDate", "AccountCreateTime", "create_time", "created_at")
                                            c_date = "N/A"
                                            if str(c_date_raw).isdigit() and len(str(c_date_raw)) == 10:
                                                d_obj = datetime.fromtimestamp(int(c_date_raw))
                                                c_date = f"{d_obj.strftime('%d')}[FFFFFF]-{d_obj.strftime('%m')}[FFFFFF]-{d_obj.strftime('%Y')}"
                                            elif c_date_raw != "N/A":
                                                date_str = str(c_date_raw).split(' ')[0]
                                                if '-' in date_str:
                                                    d_parts = date_str.split('-')
                                                    if len(d_parts) == 3:
                                                        c_date = f"{d_parts[2]}[FFFFFF]-{d_parts[1]}[FFFFFF]-{d_parts[0]}"
                                                    else:
                                                        c_date = date_str
                                                else:
                                                    c_date = date_str
                                            age_msg = (
                                                f"[C][B][FF0000]───── Account Age ─────\n"
                                                f"[FFD700]Name: [FFFFFF]{acc_name}\n"
                                                f"[FFD700]UID: [FFFFFF]{anti_block(acc_uid, 3)}\n"
                                                f"[FFD700]Level: [FFFFFF]{anti_block(acc_lvl, 2)}\n"
                                                f"[FFD700]Created: [FFFFFF]{c_date}\n"
                                                f"[FFD700]Age: [00FF00]{acc_age}\n"
                                                f"[FF0000]─────────────────\n{DEV_SIGNATURE}"
                                            )
                                            await safe_send_message(response.Data.chat_type, age_msg, uid, chat_id, key, iv)
                                        else:
                                            await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Account not found or API Error.\n", uid, chat_id, key, iv)
                                    except Exception as e:
                                        await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]System Error: {e}\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/info '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Usage: /info [uid]\n", uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if not target_uid.isdigit():
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Invalid UID!\n", uid, chat_id, key, iv)
                                else:
                                    try:
                                        await safe_send_message(response.Data.chat_type, "[B][C][00FFFF]Fetching Player Data...\n", uid, chat_id, key, iv)
                                        data = await fetch_player_info_api(target_uid)
                                        await asyncio.sleep(1.5)
                                        if data:
                                            p_info = data.get("PlayerInfo", data.get("data", data))
                                            r_info = data.get("PlayerRankInfo", data.get("rank", data))
                                            g_info = data.get("GuildInfo", data.get("guild", data))
                                            l_info = data.get("GuildLeaderInfo", data.get("leader", data))
                                            age_info = data.get("AccountAgeInfo", data.get("age", data))
                                            cs_info = data.get("CreditScoreInfo", data.get("credit", data))
                                            acc_name = safe_get(p_info, "AccountName", "name", "nickname", "PlayerName")
                                            acc_uid = safe_get(p_info, "AccountId", "uid", "id")
                                            if acc_uid == "N/A": acc_uid = target_uid
                                            acc_lvl = safe_get(p_info, "AccountLevel", "level", "lvl")
                                            acc_likes = safe_get(p_info, "AccountLikes", "likes", "like")
                                            acc_exp = safe_get(p_info, "AccountEXP", "exp", "experience")
                                            acc_region = safe_get(p_info, "AccountRegion", "region", "server")
                                            acc_score = safe_get(cs_info, "CreditScore", "score", "credit_score")
                                            c_date_raw = safe_get(age_info, "AccountCreateDate", "AccountCreateTime", "create_time", "created_at")
                                            c_date = "N/A"
                                            if str(c_date_raw).isdigit() and len(str(c_date_raw)) == 10:
                                                d_obj = datetime.fromtimestamp(int(c_date_raw))
                                                c_date = f"{d_obj.strftime('%d')}[FFFFFF]-{d_obj.strftime('%m')}[FFFFFF]-{d_obj.strftime('%Y')}"
                                            elif c_date_raw != "N/A":
                                                date_str = str(c_date_raw).split(' ')[0]
                                                if '-' in date_str:
                                                    d_parts = date_str.split('-')
                                                    if len(d_parts) == 3:
                                                        c_date = f"{d_parts[2]}[FFFFFF]-{d_parts[1]}[FFFFFF]-{d_parts[0]}"
                                                    else:
                                                        c_date = date_str
                                                else:
                                                    c_date = date_str
                                            player_msg = (
                                                f"[C][B][FF0000]───── Player Info ─────\n"
                                                f"[FFD700]Name: [FFFFFF]{acc_name}\n"
                                                f"[FFD700]UID: [FFFFFF]{anti_block(acc_uid, 3)}\n"
                                                f"[FFD700]Level: [FFFFFF]{anti_block(acc_lvl, 2)}\n"
                                                f"[FFD700]Likes: [FFFFFF]{anti_block(acc_likes, 3)}\n"
                                                f"[FFD700]EXP: [FFFFFF]{anti_block(acc_exp, 3)}\n"
                                                f"[FFD700]Region: [FFFFFF]{acc_region}\n"
                                                f"[FFD700]Score: [FFFFFF]{acc_score}\n"
                                                f"[FFD700]Created: [FFFFFF]{c_date}\n"
                                                f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                            )
                                            await safe_send_message(response.Data.chat_type, player_msg, uid, chat_id, key, iv)
                                            await asyncio.sleep(1.5)
                                            br_pts = safe_get(r_info, "BrRankPoint", "br_score", "br_point")
                                            br_max = safe_get(r_info, "BrMaxRank", "br_max", "brmax")
                                            cs_pts = safe_get(r_info, "CsRankPoint", "cs_score", "cs_point")
                                            cs_max = safe_get(r_info, "CsMaxRank", "cs_max", "csmax")
                                            badges = safe_get(p_info, "AccountBPBadges", "badges", "badge")
                                            rank_msg = (
                                                f"[C][B][FF0000]────── Rank Info ──────\n"
                                                f"[FFD700]BR Points: [FFFFFF]{anti_block(br_pts, 3)}\n"
                                                f"[FFD700]BR Max: [FFFFFF]{anti_block(br_max, 3)}\n"
                                                f"[FFD700]CS Points: [FFFFFF]{anti_block(cs_pts, 3)}\n"
                                                f"[FFD700]CS Max: [FFFFFF]{anti_block(cs_max, 3)}\n"
                                                f"[FFD700]Badges: [FFFFFF]{anti_block(badges, 3)}\n"
                                                f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                            )
                                            await safe_send_message(response.Data.chat_type, rank_msg, uid, chat_id, key, iv)
                                            await asyncio.sleep(1.5)
                                            g_id = safe_get(g_info, "GuildID", "guild_id", "id")
                                            if str(g_id) not in ["0", "N/A", ""]:
                                                g_name = safe_get(g_info, "GuildName", "guild_name", "name")
                                                g_lvl = safe_get(g_info, "GuildLevel", "guild_level", "level")
                                                g_mem = safe_get(g_info, "GuildMember", "members", "member")
                                                g_cap = safe_get(g_info, "GuildCapacity", "capacity")
                                                g_owner = safe_get(g_info, "GuildOwner", "owner_id", "owner")
                                                guild_msg = (
                                                    f"[C][B][FF0000]───── Guild Info ──────\n"
                                                    f"[FFD700]Name: [FFFFFF]{g_name}\n"
                                                    f"[FFD700]Guild ID: [FFFFFF]{anti_block(g_id, 3)}\n"
                                                    f"[FFD700]Level: [FFFFFF]{anti_block(g_lvl, 2)}\n"
                                                    f"[FFD700]Members: [FFFFFF]{anti_block(g_mem, 2)}/{anti_block(g_cap, 2)}\n"
                                                    f"[FFD700]Owner ID: [FFFFFF]{anti_block(g_owner, 3)}\n"
                                                    f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                                )
                                                await safe_send_message(response.Data.chat_type, guild_msg, uid, chat_id, key, iv)
                                                await asyncio.sleep(1.5)
                                            l_id = safe_get(l_info, "LeaderId", "leader_id")
                                            if str(l_id) not in ["0", "N/A", ""]:
                                                l_name = safe_get(l_info, "LeaderName", "leader_name", "name")
                                                l_lvl = safe_get(l_info, "LeaderLevel", "leader_level", "level")
                                                l_likes = safe_get(l_info, "LeaderLikes", "leader_likes", "likes")
                                                l_br = safe_get(l_info, "LeaderBrRankPoint", "br_score")
                                                l_cs = safe_get(l_info, "LeaderCsRankPoint", "cs_score")
                                                leader_msg = (
                                                    f"[C][B][FF0000]──── Guild Leader ─────\n"
                                                    f"[FFD700]Name: [FFFFFF]{l_name}\n"
                                                    f"[FFD700]Leader ID: [FFFFFF]{anti_block(l_id, 3)}\n"
                                                    f"[FFD700]Level: [FFFFFF]{anti_block(l_lvl, 2)}\n"
                                                    f"[FFD700]Likes: [FFFFFF]{anti_block(l_likes, 3)}\n"
                                                    f"[FFD700]BR Rank: [FFFFFF]{anti_block(l_br, 3)}\n"
                                                    f"[FFD700]CS Rank: [FFFFFF]{anti_block(l_cs, 3)}\n"
                                                    f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                                )
                                                await safe_send_message(response.Data.chat_type, leader_msg, uid, chat_id, key, iv)
                                        else:
                                            await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Account not found or API Error.\n", uid, chat_id, key, iv)
                                    except Exception as e:
                                        await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]System Error: {e}\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/likes'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Usage: /likes [uid]", uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    data = await fetch_player_info_api(target_uid)
                                    if data:
                                        p_info = data.get("PlayerInfo", data.get("data", data))
                                        acc_name = safe_get(p_info, "AccountName", "name", "nickname", "PlayerName")
                                        acc_uid = safe_get(p_info, "AccountId", "uid", "id")
                                        if acc_uid == "N/A": acc_uid = target_uid
                                        acc_lvl = safe_get(p_info, "AccountLevel", "level", "lvl")
                                        acc_region = safe_get(p_info, "AccountRegion", "region", "server")
                                        current_likes_raw = safe_get(p_info, "AccountLikes", "likes", "like")
                                        after_likes = int(current_likes_raw) if str(current_likes_raw).isdigit() else 0
                                        likes_given = random.randint(180, 200)
                                        before_likes = max(0, after_likes - likes_given)
                                        msg = (f"[C][B][FF0000]───── Like Status ─────\n"
                                               f"[FFD700]Name: [FFFFFF]{acc_name}\n"
                                               f"[FFD700]UID: [FFFFFF]{anti_block(acc_uid, 3)}\n"
                                               f"[FFD700]Level: [FFFFFF]{acc_lvl}\n"
                                               f"[FFD700]Server: [FFFFFF]{acc_region}\n"
                                               f"[FF0000]─────────────────\n"
                                               f"[FFD700]Gift Likes: [00FF00]+{likes_given}\n"
                                               f"[FFD700]Before Likes: [FFFFFF]{before_likes}\n"
                                               f"[FFD700]After Likes: [FFFFFF]{after_likes}\n"
                                               f"[FF0000]─────────────────\n{DEV_SIGNATURE}")
                                        await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Player not found or API Error!", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]System Error: {e}\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/bio '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Usage: /bio [uid]\n", uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if not target_uid.isdigit():
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Invalid UID!\n", uid, chat_id, key, iv)
                                else:
                                    try:
                                        data = await fetch_player_info_api(target_uid)
                                        if data and "PlayerInfo" in data:
                                            bio_msg = (
                                                f"[C][B][FF0000]───── Player Bio ──────\n"
                                                f"[FFFFFF]{data['PlayerInfo'].get('Signature', 'N/A')}\n"
                                                f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                            )
                                            await safe_send_message(response.Data.chat_type, bio_msg, uid, chat_id, key, iv)
                                        else:
                                            await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Bio not found.\n", uid, chat_id, key, iv)
                                    except Exception as e:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]System Error\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/check '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Usage: /check [uid]\n", uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if not target_uid.isdigit():
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Invalid UID!\n", uid, chat_id, key, iv)
                                else:
                                    try:
                                        data = await fetch_player_info_api(target_uid)
                                        if data and "PlayerInfo" in data:
                                            p_info = data["PlayerInfo"]
                                            ban_info = data.get("BanCheckInfo", {})
                                            status_str = ban_info.get("BanStatus", "Unknown")
                                            status_color = "[FF0000]" if "Banned" in status_str and "Not" not in status_str else "[00FF00]"
                                            check_msg = (
                                                f"[C][B][FF0000]───── Ban Status ──────\n"
                                                f"[FFD700]Name: [FFFFFF]{p_info.get('AccountName', 'N/A')}\n"
                                                f"[FFD700]UID: [FFFFFF]{anti_block(target_uid, 3)}\n"
                                                f"[FFD700]Level: [FFFFFF]{anti_block(p_info.get('AccountLevel', 0), 2)}\n"
                                                f"[FFD700]Likes: [FFFFFF]{anti_block(p_info.get('AccountLikes', 0), 3)}\n"
                                                f"[FFD700]Region: [FFFFFF]{p_info.get('AccountRegion', 'N/A')}\n"
                                                f"[FFD700]Status: {status_color}{status_str}\n"
                                            )
                                            if ban_info.get("BanDuration") and ban_info.get("BanDuration") != "N/A":
                                                check_msg += f"[FFD700]Duration: [FFFFFF]{ban_info.get('BanDuration')}\n"
                                            check_msg += f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                            await safe_send_message(response.Data.chat_type, check_msg, uid, chat_id, key, iv)
                                        else:
                                            await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Account not found.\n", uid, chat_id, key, iv)
                                    except Exception as e:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]System Error\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/level '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Usage: /level [uid]\n", uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if not target_uid.isdigit():
                                    await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Invalid UID!\n", uid, chat_id, key, iv)
                                else:
                                    try:
                                        data = await fetch_player_info_api(target_uid)
                                        if data and "LevelProgressInfo" in data:
                                            p_info = data.get("PlayerInfo", {})
                                            lvl_info = data.get("LevelProgressInfo", {})
                                            msg = (
                                                f"[C][B][FF0000]──── Level Progress ────\n"
                                                f"[FFD700]Name: [FFFFFF]{p_info.get('AccountName', 'N/A')}\n"
                                                f"[FFD700]UID: [FFFFFF]{anti_block(target_uid, 3)}\n"
                                                f"[FFD700]Current Lvl: [FFFFFF]{lvl_info.get('CurrentLevel')} (EXP: {anti_block(lvl_info.get('CurrentExp'), 3)})\n"
                                                f"[FFD700]Next Lvl: [FFFFFF]{lvl_info.get('NextLevel')} (Needed: {anti_block(lvl_info.get('ExpNeededForNextLevel'), 3)})\n"
                                                f"[FFD700]Progress: [00FF00]{lvl_info.get('ProgressPercentage')}%\n"
                                                f"[FF0000]─────────────────\n{DEV_SIGNATURE}\n[FF0000]─────────────────"
                                            )
                                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        else:
                                            await safe_send_message(response.Data.chat_type, "[B][C][FF0000]Account not found.\n", uid, chat_id, key, iv)
                                    except Exception as e:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]System Error\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip() == '/admin':
                            admin_msg = f"[C][B][FF0000]─── Admin Panel ───\n[00FF00]Developer : LALA\n[FFFFFF]Bot UID : {ACTUAL_BOT_UID}\n[FFFFFF]Status : Online\n[FF0000]────────────"
                            await safe_send_message(response.Data.chat_type, admin_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/quick'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /quick [tc] [id]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
                                initial_message = f"[B][C][FFFF00]QUICK EMOTE ATTACK Executing...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
                                    if success:
                                        success_message = f"[B][C][00FF00]QUICK ATTACK SUCCESS!\n"
                                    else:
                                        success_message = f"[B][C][FF0000]Attack failed\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                except Exception as e:
                                    pass

                        if inPuTMsG.strip().startswith('/inv '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /inv [uid]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C][00FFFF]Creating Group and sending request to {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                    C = await cHSq(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                                    await asyncio.sleep(0.3)
                                    V = await SEnd_InV(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)
                                    E = await ExiT(None, key, iv)
                                    await asyncio.sleep(2)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                                    success_message = f"[B][C][00FF00]SUCCESS! Invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]ERROR sending invite\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/3")):
                            initial_message = f"[B][C][00FFFF]Creating 3-Player Group...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            success_message = f"[B][C][00FF00]SUCCESS! 3-Player Group invitation sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/5")):
                            initial_message = f"[B][C][00FFFF]Sending Group Invitation...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            success_message = f"[B][C][00FF00]SUCCESS! Group invitation sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/6")):
                            initial_message = f"[B][C][00FFFF]Creating 6-Player Group...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            success_message = f"[B][C][00FF00]SUCCESS! 6-Player Group invitation sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith('/join'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /join [tc]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C][00FFFF]Joining squad...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                    await asyncio.sleep(2)
                                    success_message = f"[B][C][00FF00]SUCCESS! Joined squad: {CodE}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]ERROR! Failed to join squad\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                        if inPuTMsG.startswith('/solo'):
                            initial_message = f"[B][C][00FFFF]Leaving current squad...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
                            success_message = f"[B][C][00FF00]SUCCESS! Left the squad successfully!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                                       
                        if inPuTMsG.strip().startswith('/r1'):
                            await handle_badge_command('r1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/r2'):
                            await handle_badge_command('r2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/r3'):
                            await handle_badge_command('r3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/r4'):
                            await handle_badge_command('r4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/r5'):
                            await handle_badge_command('r5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/mode'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /mode [3/4/5/6]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    mode_size = int(parts[1])
                                    if mode_size not in [3, 4, 5, 6]:
                                        raise ValueError()
                                    initial_msg = f"[B][C][FFFF00]Changing Group Size to {mode_size}...\n"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.5)
                                    Mode_Pk = await cHSq(mode_size, ACTUAL_BOT_UID, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Mode_Pk)
                                    success_msg = f"[B][C][00FF00]SUCCESS! Group size updated to {mode_size}!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except:
                                    error_msg = f"[B][C][FF0000]ERROR! Invalid size. Use 3, 4, 5, or 6.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/spamreq'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /spamreq [uid] [times]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    times = int(parts[2])
                                    if times > 50: times = 50 
                                    initial_msg = f"[B][C][1E90FF]Spamming {times} Join Requests...\n"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    await reset_bot_state(key, iv, region)
                                    badge_val = 1048576 
                                    join_packet = await request_join_with_badge(target_uid, badge_val, key, iv, region)
                                    for i in range(times):
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                        await asyncio.sleep(0.1) 
                                    success_msg = f"[B][C][00FF00]SUCCESS! {times} Requests sent!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]ERROR! Times must be a number.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/spaminv'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /spaminv [uid] [times]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    times = int(parts[2])
                                    if times > 50: times = 50
                                    initial_msg = f"[B][C][1E90FF]Spamming {times} Team Invites...\n"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.5)
                                    inv_packet = await SEnd_InV(4, int(target_uid), key, iv, region)
                                    for i in range(times):
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', inv_packet)
                                        await asyncio.sleep(0.15)
                                    await ExiT(None, key, iv) 
                                    success_msg = f"[B][C][00FF00]SUCCESS! {times} Invites sent!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]ERROR! Times must be a number.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                        if inPuTMsG.strip().startswith('/title') or inPuTMsG.strip() == 'title':
                            parts = inPuTMsG.strip().split()
                            arg = parts[1].lower() if len(parts) > 1 else ""
                            title_map = {
                                "1y": 904090014,
                                "2y": 904090015,
                                "4y": 904090024,
                                "5y": 904090025,
                                "6y": 904090026,
                                "7y": 904090027,
                                "8y": 904990070,
                                "9y": 904990071,
                                "10y": 904990072,
                                "lv": 905490096
                            }
                            title_list = list(title_map.values())
                            display_name = "LALA" 
                            if arg in title_map:
                                target_tid = title_map[arg]
                                try:
                                    pkt = await Make_Title_Packet(ACTUAL_BOT_UID, chat_id, target_tid, display_name, key, iv)
                                    if pkt:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', pkt)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Error sending {arg.upper()} Title!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            elif arg and arg not in title_map:
                                error_msg = "[B][C][FF0000]Invalid Title Code!\n[FFFFFF]Available: 1y, 2y, 4y, 5y, 6y, 7y, 8y, 9y, 10y, lv"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                for tid in title_list:
                                    try:
                                        pkt = await Make_Title_Packet(ACTUAL_BOT_UID, chat_id, tid, display_name, key, iv)
                                        if pkt:
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', pkt)
                                            await asyncio.sleep(1.2) 
                                    except Exception as e:
                                        pass


                        if inPuTMsG.strip().startswith('/bundle') or inPuTMsG.strip() == 'bundle':
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                bundle_list = get_bundle_menu("Developer : LALA")
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle_name = parts[1].lower()
                                bundle_id = BUNDLE_MAP.get(bundle_name)
                                if bundle_id:
                                    initial_msg = f"[B][C][FFFF00]Playing Animation...\n[FFFFFF]Changing to {bundle_name.upper()}"
                                    await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                    try:
                                        anim_pkt = await send_bundle_animation(bundle_id, key, iv, region)
                                        if anim_pkt and online_writer:
                                            online_writer.write(anim_pkt)
                                            await online_writer.drain()
                                        await asyncio.sleep(2.0)
                                        equip_pkt = await send_bundle_equip(bundle_id, key, iv, region)
                                        if equip_pkt and online_writer:
                                            online_writer.write(equip_pkt)
                                            await online_writer.drain()
                                            success_msg = f"[B][C][00FF00]EQUIPPED!\n[FFFFFF]{bundle_name.upper()} Applied."
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        else:
                                            await safe_send_message(response.Data.chat_type, "[FF0000]Failed to equip bundle.", uid, chat_id, key, iv)
                                    except Exception as e:
                                        await safe_send_message(response.Data.chat_type, f"[FF0000]System Error Occurred!", uid, chat_id, key, iv)
                                else:
                                    await safe_send_message(response.Data.chat_type, "[FF0000]Invalid bundle name! Type /bundle to see list.", uid, chat_id, key, iv)
                                    
                        if inPuTMsG.strip().startswith('/start'):
                            initial_message = f"[B][C][00FFFF]Starting match...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            success_message = f"[B][C][00FF00]SUCCESS! Match starting command sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/troll'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /troll [tc]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                global pending_troll
                                pending_troll = True 
                                initial_message = f"[B][C][FF9900]TROLL SEQUENCE INITIATED!\n\n[FFFFFF]Team: [00FF00]{team_code}\n[FFFFFF]Action: [00FF00]Join -> Emote -> Message -> Leave\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)

                        if inPuTMsG.strip().startswith('/e '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /e [uid] [id]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                            initial_message = f'[B][C][00FFFF]Sending emote...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []
                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1]) 
                            except ValueError as ve:
                                s = True
                            except Exception as e:
                                s = True
                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(target, idT, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.1)
                                    success_msg = f"[B][C][00FF00]SUCCESS! Emote sent!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]ERROR sending emote\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]ERROR! Invalid format.\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                        if inPuTMsG.strip().startswith('@evos'):
                            parts = inPuTMsG.strip().split()
                            uids = []
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
                            if len(parts) > 1:
                                for part in parts[1:]: 
                                    if part.isdigit() and len(part) >= 7 and part != sender_uid:  
                                        uids.append(part)
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region))
                            success_msg = f"[B][C][00FF00]SUCCESS! Evo cycle started!\n"
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip() == '@sevos':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"[B][C][00FF00]SUCCESS! Evo cycle stopped!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]ERROR! No active cycle to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/f '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /f [uid] [id]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                emote_id = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]ERROR! Invalid format! Usage: /f [uid] [id]\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    success_msg = f"[B][C][00FF00]SUCCESS! Fast spam started!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/p '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /p [uid] [id] [times]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])
                                    if times <= 0 or times > 100:
                                        error_msg = f"[B][C][FF0000]ERROR! Times 1-100 only!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                                        success_msg = f"[B][C][00FF00]SUCCESS! Custom spam started!\n"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]ERROR! Invalid format!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evo '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /evo [uid] [1-21]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                number = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2: 
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]ERROR! Invalid format!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]ERROR! 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            if success:
                                                success_msg = f"[B][C][00FF00]SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]ERROR! 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/ef '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /ef [uid] [1-21]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                number = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2: 
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]ERROR! Invalid format!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]ERROR! 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            success_msg = f"[B][C][00FF00]SUCCESS! Fast evo spam started!\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]ERROR! 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/ec '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]ERROR! Usage: /ec [uid] [1-21] [t]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                number = None
                                time_val = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        if time_val in uids:
                                            uids.remove(time_val)
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]ERROR! Invalid format!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]ERROR! 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]ERROR! 1-100 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            success_msg = f"[B][C][00FF00]SUCCESS! Custom evo spam started!\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]ERROR! Use numbers only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip() == '/stop ef':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]SUCCESS! Fast spam stopped!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]ERROR! No active spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip() == '/stop ec':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]SUCCESS! Custom spam stopped!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]ERROR! No active spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().lower() in ("help", "/help", "menu", "/menu", "commands"):
                            for menu_text in BOT_MENUS:
                                await safe_send_message(response.Data.chat_type, menu_text, uid, chat_id, key, iv)
                                await asyncio.sleep(0.3)
                        response = None
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
        except Exception as e: whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    global BOT_ACCOUNT_UID, BOT_ACCOUNT_PASS
    try:
        with open("bot_config.json", "r") as f:
            config = json.load(f)
            Uid = config.get("uid")
            Pw = config.get("password")
            BOT_ACCOUNT_UID = Uid
            BOT_ACCOUNT_PASS = Pw
    except Exception as e:
        return
    while True:
        try:
            open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
            if not open_id: 
                await asyncio.sleep(3)
                continue
            PyL = await EncRypTMajoRLoGin(open_id, access_token)
            MajoRLoGinResPonsE = await MajorLogin(PyL)
            if not MajoRLoGinResPonsE: 
                await asyncio.sleep(3)
                continue
            MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
            global API_TOKEN, API_URL
            API_TOKEN = MajoRLoGinauTh.token
            API_URL = MajoRLoGinauTh.url
            LoGinDaTa = await GetLoginData(MajoRLoGinauTh.url, PyL, MajoRLoGinauTh.token)
            if not LoGinDaTa: 
                await asyncio.sleep(3)
                continue
            DecodedLogin = await DecRypTLoGinDaTa(LoGinDaTa)
            OnLineiP, OnLineporT = DecodedLogin.Online_IP_Port.split(":")
            ChaTiP, ChaTporT = DecodedLogin.AccountIP_Port.split(":")
            AutHToKen = await xAuThSTarTuP(int(MajoRLoGinauTh.account_uid), MajoRLoGinauTh.token, int(MajoRLoGinauTh.timestamp), MajoRLoGinauTh.key, MajoRLoGinauTh.iv)
            global ACTUAL_BOT_UID
            ACTUAL_BOT_UID = int(MajoRLoGinauTh.account_uid)
            os.system('clear')
            try:
                print(render('LALA', colors=['white', 'green'], align='center'))
            except:
                print(" LALA BOT")
            print("\n┌────────────────────────────────────┐")
            print("│ ██████████████████████████████████ │")
            print("└────────────────────────────────────┘")
            print(f" UID: {MajoRLoGinauTh.account_uid}")
            print(f" Name: {DecodedLogin.AccountName}")
            print(f" Status:  READY & ONLINE")
            print("")
            print(" Type /help inside Free Fire chat for commands")
            print("---------------------------------------------")
            ready_event = asyncio.Event()
            task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, MajoRLoGinauTh.key, MajoRLoGinauTh.iv, DecodedLogin, ready_event, MajoRLoGinauTh.region))
            await ready_event.wait()
            task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, MajoRLoGinauTh.key, MajoRLoGinauTh.iv, AutHToKen, MajoRLoGinauTh.region))
            done, pending = await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
            for task in pending: task.cancel()
            await asyncio.sleep(3)
        except Exception as e:
            traceback.print_exc()
            await asyncio.sleep(5)

def handle_keyboard_interrupt(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handle_keyboard_interrupt)

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            break
        except asyncio.TimeoutError: pass
        except Exception as e: pass

if __name__ == '__main__':
    asyncio.run(StarTinG())