from ast import main
import hashlib
import base64


class Crypto:
    
    @staticmethod
    def encrypt(password: str, salt: str = "store") -> str:

        # 1. salt -> Base64
        base64_salt = base64.b64encode(salt.encode("utf-8")).decode("utf-8")

        # 2. 拼接（salt 在前，password 在后）
        combined = base64_salt + password

        # 3. SHA-512 第一轮
        hash_bytes = hashlib.sha512(combined.encode("utf-8")).digest()

        # 4. SHA-512 第二轮
        hash_bytes = hashlib.sha512(hash_bytes).digest()

        # 5. 转 hex（小写）
        return hash_bytes.hex()