from typing import Dict, List, Optional
from pydantic import BaseModel


class ApiResultHandler(BaseModel):
    """
    API返回的数据处理器
    """

    code: int = -1
    """返回码"""
    success: bool = False
    """成功"""
    data: Optional[dict] = None
    """返回数据"""
    need_verify: bool = False
    """需要进行人机验证"""

    def __bool__(self):
        return self.success and self.code == 200

    @property
    def login_expired(self):
        """
        登录过期
        """
        return self.code == 220


class GetSmsCodeResultHandler(ApiResultHandler):
    """
    获取短信验证码数据处理器
    """

    class DataModel(BaseModel):
        geeTest: bool
        """是否需要人机验证"""

    data: DataModel

    def __init__(self, **data):
        super().__init__(**data)
        if not self.data.geeTest and self.code == 200:
            self.success = True
        else:
            self.success = False
            self.need_verify = True


class GeetestResultHandler(ApiResultHandler):
    """
    人机验证数据处理器
    """

    class DataModel(BaseModel):
        lot_number: str
        """验证标识"""
        result: str
        """验证结果"""
        fail_count: int
        """失败次数"""
        seccode: dict
        """验证数据"""
        score: str
        """验证分数"""
        payload: str
        """验证数据"""
        process_token: str
        """验证标识"""
        payload_protocol: int
        """验证数据"""

    status: str
    """状态"""
    data: DataModel

    def __init__(self, **data):
        super().__init__(**data)
        if self.status == "success" and self.data.result == "success":
            self.success = True
        else:
            self.success = False

    def __bool__(self):
        return self.success


class LoginResultHandler(ApiResultHandler):
    """
    登录数据处理器
    """

    class DataModel(BaseModel):
        enableChildMode: bool
        """是否启用儿童模式"""
        gender: int
        """性别"""
        signature: str
        """签名"""
        headUrl: str
        """头像链接"""
        headCode: str
        """头像编号"""
        userName: str
        """用户名"""
        userId: str
        """用户ID"""
        isRegister: int
        """是否注册"""
        isOfficial: int
        """是否官方"""
        status: int
        """状态"""
        unRegistering: bool
        """是否注销"""
        token: str
        """登录凭证"""

    msg: str
    data: Optional[DataModel] = None

    def __init__(self, **data):
        super().__init__(**data)

    @property
    def code_error(self):
        """
        验证码错误
        """
        return self.code == 130


class GetRewardsResultHandler(ApiResultHandler):
    """
    获取签到数据处理器
    """

    class GoodsConfigModel(BaseModel):
        goodsId: int
        """奖励ID"""
        goodsName: str
        """奖励名称"""
        goodsNum: int
        """奖励数量"""
        goodsUrl: str
        """奖励链接"""

    class DataModel(BaseModel):
        disposableGoodsList: List["GetRewardsResultHandler.GoodsConfigModel"]
        """一次性奖励列表"""
        disposableSignNum: int
        """一次性签到次数"""
        eventEndTimes: str
        """活动结束时间"""
        eventStartTimes: str
        """活动开始时间"""
        expendGold: int
        """消耗金币"""
        expendNum: int
        """消耗次数"""
        isSigIn: bool
        """是否签到"""
        nowServerTimes: str
        """当前服务器时间"""
        omissionNnm: int
        """漏签次数"""
        openNotifica: bool
        """打开通知"""
        redirectContent: str
        """重定向内容"""
        redirectText: str
        """重定向文本"""
        redirectType: int
        """重定向类型"""
        repleNum: int
        """补签次数"""
        sigInNum: int
        """签到次数"""
        signInGoodsConfigs: List["GetRewardsResultHandler.GoodsConfigModel"]
        """签到奖励列表"""
        signLoopGoodsList: list
        """循环签到奖励列表"""

    msg: str
    data: Optional[DataModel] = None
    goods_config: Optional[Dict[int, GoodsConfigModel]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.code == 200:
            self.success = True
            self.goods_config = {
                item.goodsId: item for item in self.data.signInGoodsConfigs
            }
            for item in self.data.disposableGoodsList:
                self.goods_config[item.goodsId] = item
        else:
            self.success = False


class SignResultHandler(ApiResultHandler):
    """
    签到数据处理器
    """

    class GoodsModel(BaseModel):
        goodsId: int
        """奖励ID"""
        goodsNum: int
        """奖励数量"""
        goodsUrl: str
        """奖励链接"""
        type: int
        """类型"""

    class DataModel(BaseModel):
        todayList: List["SignResultHandler.GoodsModel"]
        """今日奖励列表"""
        tomorrowList: List["SignResultHandler.GoodsModel"]
        """明日奖励列表"""

    msg: str
    data: Optional[DataModel] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.code == 200:
            self.success = True
        else:
            self.success = False

    @property
    def is_signed_in(self):
        return self.code == 1511
