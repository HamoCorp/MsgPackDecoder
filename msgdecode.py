import base64
import msgpack
import re
#https://github.com/HamoCorp/MsgPackDecoder
def decode_blob(b: bytes):
    text = b.decode("utf-8", errors="ignore")

    match = re.search(r"(\{.*\})", text)
    if match:
        return {
            "raw": text,
            "json": match.group(1)
        }

    return {"raw": text}


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [walk(v) for v in obj]

    elif isinstance(obj, bytes):
        return decode_blob(obj)

    else:
        return obj


def decode(b64):
    raw = base64.b64decode(b64)
    decoded = msgpack.unpackb(raw, raw=False)
    return walk(decoded)


b64 = input("Base64: ").strip()

print(decode(b64))