import datetime
import hashlib
import base64
import secrets
import bcrypt


def get_app_device():
    aid = secrets.token_hex(16)
    mac = "0A:00:27:00:00:00"
    manufactor = "Xiaomi"
    brand = "Xiaomi"
    model = "MI 6"
    buildNumber = "MIUI-12.0.1"
    fp = " ;".join([aid, "", "", mac, manufactor, brand, model, buildNumber])
    b64_device_token = base64.standard_b64encode(fp.encode("utf-8")).rstrip(b"=")
    return b64_device_token[::-1].decode("utf-8")


def get_app_token_v2(x_app_device):
    md5_device_code = hashlib.md5(x_app_device.encode("utf-8")).hexdigest()
    timestamp = str(int(datetime.datetime.now().timestamp()))
    base64_timestamp = base64.standard_b64encode(timestamp.encode("utf-8")).rstrip(b"=")
    md5_timestamp = hashlib.md5(timestamp.encode("utf-8")).hexdigest()
    token = (
        "token://com.coolapk.market/dcf01e569c1e3db93a3d0fcf191a622c?"
        + md5_timestamp
        + "$"
        + md5_device_code
        + "&com.coolapk.market"
    )
    base64_token = base64.standard_b64encode(token.encode("utf-8")).rstrip(b"=")
    md5_base64_token = hashlib.md5(base64_token).hexdigest()
    md5_token = hashlib.md5(token.encode("utf-8")).hexdigest().encode("utf-8")
    bcrypt_salt = b"$2y$10$" + base64_timestamp + b"/" + md5_token[:6] + b"u"
    crypt = bcrypt.hashpw(md5_base64_token.encode("utf-8"), bcrypt_salt)
    x_app_token = "v2" + base64.standard_b64encode(crypt).rstrip(b"=").decode("utf-8")
    return x_app_token


if __name__ == "__main__":
    x_app_device = get_app_device()
    print(x_app_device)
    token = get_app_token_v2(x_app_device)
    print(token)
