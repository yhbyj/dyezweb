# encoding: utf-8
__author__ = 'mtianyan'
__date__ = '2018/3/15 0015 14:46'


def get_auth_url():
    """
    client_id	必填	string	申请应用时分配的AppKey。
    redirect_uri	必填	string	授权回调地址，站外应用需与设置的回调地址一致。
    """
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = "http://127.0.0.1:8000/complete/weibo/"
    client_id = "478178675"
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={re_url}".format(client_id=client_id,
                                                                                      re_url=redirect_uri)

    print(auth_url)


def get_access_token(code):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": "478178675",
        "client_secret": "78a7e4529bd716e36ad12f1680d426fc",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/complete/weibo/",

    })
    # '{"access_token":"2.009HzSZB0RH53W659ff36ad60UsK73","remind_in":"157679999","expires_in":157679999,"uid":"1437829442","isRealName":"false"}'
    pass


def get_user_info(access_token):
    user_url = "https://api.weibo.com/2/users/show.json"
    uid = "1437829442"
    get_url = user_url + "?access_token={at}&uid={uid}".format(at=access_token, uid=uid)
    print(get_url)


if __name__ == "__main__":
    # get_auth_url()
    # get_access_token("87cb201c3b9b029049a7787f44707a1a")
    get_user_info("2.009HzSZB0RH53W659ff36ad60UsK73")
