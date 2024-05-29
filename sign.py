from api import game_sign
if __name__ == '__main__':
    message = ""
    cookie_file = open("mc_users.txt", "r+", encoding="utf8")
    cookie_lines = cookie_file.readlines()
    for cookie_line in cookie_lines:
        # kuro_street_id
        id = cookie_line.split("#")[0]
        # mc_uid
        role_id = cookie_line.split("#")[1]
        # token
        token = cookie_line.split("#")[2]
        user_data = {
            "token": token,
            "id": id
        }
        game_sign.WutheringWaves.role_id = role_id
        print("开始执行签到")
        if user_data:
            for class_type in game_sign.AVAILABLE_GAME_SIGNS:
                message += f"开始签到{class_type.name}\n\n"
                signer = class_type(token=user_data["token"], user_id=user_data["id"])
                rewards = signer.get_rewards()
                sign_result = signer.sign()
                if sign_result:
                    for today in sign_result.data.todayList:
                        name = rewards.goods_config[today.goodsId].goodsName
                        num = today.goodsNum
                        message += f"签到成功，获得{name}x{num}\n"
                elif sign_result.is_signed_in:
                    message += "今日已签到\n"
                elif sign_result.login_expired:
                    message += "登录过期\n"
                else:
                    print(sign_result.msg)
                    message += f"签到失败，{sign_result.msg}\n"
            print(message[:-1])
        else:
            print("签到 - 无用户信息")
            print("无用户信息，请先登录")