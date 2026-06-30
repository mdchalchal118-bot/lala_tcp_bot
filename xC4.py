import requests , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading , random , os , asyncio
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
Key , Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]) , bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

async def EnC_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
async def DEc_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()
async def EnC_PacKeT(HeX , K , V): 
    return AES.new(K , AES.MODE_CBC , V).encrypt(pad(bytes.fromhex(HeX) ,16)).hex()
async def DEc_PacKeT(HeX , K , V):
    return unpad(AES.new(K , AES.MODE_CBC , V).decrypt(bytes.fromhex(HeX)) , 16).hex()  
async def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None
async def EnC_Vr(N):
    if N < 0: ''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n
async def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return await EnC_Vr(field_header) + await EnC_Vr(value)
async def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return await EnC_Vr(field_header) + await EnC_Vr(len(encoded_value)) + encoded_value
async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await CrEaTe_ProTo(value)
            packet.extend(await CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet
async def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    if len(F) == 1: F = "0" + F ; return F
    else: return F
async def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = await Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict
async def redzed(uid,code,K,V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
            2: 161,
            4: "y[WW",
            6: 11,
            8: "1.114.18",
            9: 3,
            10: 1
            },
            10: str(code),
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
async def RejectMSGtaxt(squad_owner, uid, key, iv):
    random_banner = f"""[00FF00]WELCOME_TO_RIDUAN_TCP_BOT
    [FF0000]HOW_ARE_YOU?"""
    fields = {
        1: 5,
        2: {
            1: int(squad_owner),
            2: 1,
            3: int(uid),
            4: random_banner
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', key, iv)
async def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = await Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        return None
def xMsGFixinG(uid):
    uid_str = str(uid)
    parts = [uid_str[i:i+3] for i in range(0, len(uid_str), 3)]
    return ''.join('[C]' + part for part in parts)
async def Ua():
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"
async def ArA_CoLor():
    Tp = ["32CD32" , "00BFFF" , "00FA9A" , "90EE90" , "FF4500" , "FF6347" , "FF69B4" , "FF8C00" , "FF6347" , "FFD700" , "FFDAB9" , "F0F0F0" , "F0E68C" , "D3D3D3" , "A9A9A9" , "D2691E" , "CD853F" , "BC8F8F" , "6A5ACD" , "483D8B" , "4682B4", "9370DB" , "C71585" , "FF8C00" , "FFA07A"]
    return random.choice(Tp)
async def get_random_avatar():
    avatar_list = [
        902042010, 902049003
    ]
    return random.choice(avatar_list)
async def xSEndMsg(Msg, Tp, Tp2, id, K, V, region="BD"):
    feilds = {
        1: id, 
        2: Tp2, 
        3: Tp, 
        4: Msg, 
        5: 1735129800, 
        7: 2, 
        9: {
            1: "xBesTo - C4", 
            2: int(await get_random_avatar()), 
            3: 901027027, 
            4: 330, 
            5: 801046529, 
            8: "xBesTo - C4", 
            10: 1, 
            11: 1, 
            13: {1: 2}, 
            14: {
                1: 12484827014, 
                2: 8, 
                3: "\x10\x15\x08\n\x0b\x13\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
            }, 
            12: 0
        }, 
        10: "en", 
        13: {3: 1},
        14: {
            1: {
                1: 3,
                2: 7,
                3: 170,
                4: 1,
                5: 1740196800,
                6: region
            }
        }
    }
    Pk = (await CrEaTe_ProTo(feilds)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
async def xSEndMsgsQ(Msg , id , K , V, region="BD"):
    avatar = await get_random_avatar()
    fields = {
        1: id, 2: id, 4: Msg, 5: int(time.time()), 8: 904990072, 
        9: {
            1: "[FFFFFF]Riduan Bot", 2: avatar, 3: 2, 4: 329, 5: 1001000001, 6: 66, 7: 66, 8: "xBesTo - C4", 
            9: 66, 10: 66, 11: 66, 12: 66, 13: {1: 68, 2:67}, 
            14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"}
        }, 
        10: "en", 13: {66: 66}, 14: {11: {1: 3, 2: 7, 3: 170, 4: 999, 5: 1, 6: region, 8: 2, 9: 2}}
    }
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
async def AuthClan(CLan_Uid, AuTh, K, V):
    fields = {1: 3, 2: {1: int(CLan_Uid), 2: 1, 4: str(AuTh)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1201' , K , V)
async def AutH_GlobAl(K, V):
    fields = {
    1: 3,
    2: {
        2: 5,
        3: "en"
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)
async def LagSquad(K,V):
    fields = {
    1: 15,
    2: {
        1: 1124759936,
        2: 1
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
async def new_lag(K, I):
    fields = {
        1: 15,
        2: {
            1: 804266360,
            2: 1
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, I)
async def KickTarget(target_uid, K, I):
    fields = {
        1: 35,
        2: {
            1: int(target_uid)
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, I)
async def GeT_Status(PLayer_Uid , K , V):
    PLayer_Uid = await EnC_Uid(PLayer_Uid , Tp = 'Uid')
    if len(PLayer_Uid) == 8: Pk = f'080112080a04{PLayer_Uid}1005'
    elif len(PLayer_Uid) == 10: Pk = f"080112090a05{PLayer_Uid}1005"
    return await GeneRaTePk(Pk , '0f15' , K , V)
async def SPam_Room(Uid , Rm , Nm , K , V):
    fields = {1: 78, 2: {1: int(Rm), 2: f"[{ArA_CoLor()}]{Nm}", 3: {2: 1, 3: 1}, 4: 330, 5: 1, 6: 201, 10: await get_random_avatar(), 11: int(Uid), 12: 1}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0e15' , K , V)
async def GenJoinSquadsPacket(code,  K , V):
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][4] = bytes.fromhex("01090a0b121920")
    fields[2][5] = str(code)
    fields[2][6] = 6
    fields[2][8] = 1
    fields[2][9] = {}
    fields[2][9][2] = 800
    fields[2][9][6] = 11
    fields[2][9][8] = "1.111.1"
    fields[2][9][9] = 5
    fields[2][9][10] = 1
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)   
async def GenJoinGlobaL(owner , code , K, V):
    fields = {
    1: 4,
    2: {
        1: owner,
        6: 1,
        8: 1,
        13: "en",
        15: code,
        16: "OR",
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
async def FS(K,V):
    fields = {
            1: 9,
            2: {
                1: 13256361202
            }
            }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
async def Emote_k(TarGeT , idT, K, V,region):
    fields = {
        1: 21,
        2: {
            1: 804266360,
            2: 909000001,
            5: {
                1: TarGeT,
                3: idT,
            }
        }
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)
async def GeTSQDaTa(D):
    uid = D['5']['data']['1']['data']
    chat_code = D["5"]["data"]["17"]["data"]
    squad_code = D["5"]["data"]["31"]["data"]
    return uid, chat_code , squad_code
async def AutH_Chat(T , uid, code , K, V):
    fields = {
  1: T,
  2: {
    1: uid,
    3: "en",
    4: str(code)
  }
}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)
async def Msg_Sq(msg, owner, bot, K, V, region="BD"):
    fields = {
        1: 1,
        2: {
            1: bot, 2: owner, 4: msg, 5: 14124002113, 7: 2,
            9: {
                1: "Fun1w5a2", 2: await get_random_avatar(), 3: 909000024, 4: 330, 10: 1,
                14: { 1: bot, 2: 8, 3: "\x10\x15\x08\n\x0b\x13\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06" }
            },
            10: "ar", 13: {3: 1},
            14: {
                1: { 1: 3, 2: 7, 3: 170, 4: 999, 5: 1740196800, 6: region }
            }
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', K, V)
async def ghost_pakcet(player_id , secret_code ,K , V):
    fields = {
        1: 61,
        2: {
            1: int(player_id),  
            2: {
                1: int(player_id),  
                2: int(time.time()),  
                3: "MR3SKR",
                5: 12,  
                6: 9999999,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: secret_code,},}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
async def GeneRaTePk(Pk , N , K , V):
    PkEnc = await EnC_PacKeT(Pk , K , V)
    _ = await DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    else: return bytes.fromhex(N + "0000" + _ + PkEnc)
    return bytes.fromhex(HeadEr + _ + PkEnc)
async def OpEnSq(K , V,region):
    fields = {1: 1, 2: {2: "\u0001", 3: 1, 4: 1, 5: "en", 9: 1, 11: 1, 13: 1, 14: {2: 5756, 6: 11, 8: "1.111.5", 9: 2, 10: 4}}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)
async def cHSq(Nu , Uid , K , V,region):
    fields = {1: 17, 2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)
async def SEnd_InV(Nu , Uid , K , V,region):
    fields = {1: 2 , 2: {1: int(Uid) , 2: region , 4: int(Nu)}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)
async def ExiT(idT , K , V):
    fields = {
        1: 7,
        2: {
            1: idT,
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V) 
async def send_bundle_animation(bundle_id, key, iv, region):
    fields = {
        1: 88, 
        2: {
            1: {1: int(bundle_id)}
        }
    }
    if region.lower() == "ind": packet = '0514'
    elif region.lower() == "bd": packet = "0519"
    else: packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, key, iv)
async def send_bundle_equip(bundle_id, key, iv, region):
    fields = {
        1: 88, 
        2: {
            1: {1: int(bundle_id), 2: 1}, 
            2: 2
        }
    }
    if region.lower() == "ind": packet = '0514'
    elif region.lower() == "bd": packet = "0519"
    else: packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, key, iv)
async def Make_Title_Packet(target_uid, chat_id, title_id, nickname, K, V):
    timestamp = int(time.time())
    title_json = f'{{"TitleID":{title_id},"type":"Title"}}'
    fields = {
        1: 1, 
        2: {
            1: int(target_uid), 2: int(chat_id), 5: timestamp, 8: title_json, 
            9: {
                1: f"[C][B][FF0000]{nickname}", 2: int(await get_random_avatar()), 4: 330, 5: 801046529, 
                8: "BOT TEAM", 10: 1, 11: 1, 13: {1: 2}, 
                14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"}
            }, 
            10: "en", 13: {2: 2, 3: 1}, 14: {}
        }
    }
    proto_hex = (await CrEaTe_ProTo(fields)).hex()
    return await GeneRaTePk(proto_hex, '1215', K, V)