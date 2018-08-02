//
//  user （用户）
//  ____
//
//  Created by ylin on 2018-08-02 14:56:24.
//  Copyright © 2018年 QuTui Science and Technology Co., Ltd. All rights
//  reserved.
//
//  MARK: 此文件由脚本自动生成, 手动修改文件内容, 将会被覆盖, 如需修改,
//  可在派生类进行!

#import "ApiRequest.h"

/**

user （用户）
*/
@interface UserAPI : ApiRequest

/// 登录
- (void)userLogin_with_smsMobilePhoneNumber:(NSString *)mobilePhoneNumber
                                    smsCode:(NSString *)smsCode;

/// 分享海报
- (void)userShare_poster;

/// 发送注册短信
- (void)userRegisterSmsMobilePhoneNumber:(NSString *)mobilePhoneNumber
                              inviteCode:(NSString *)inviteCode;

/// 发送更换手机号码的验证短信
- (void)userMobilePhoneNumber:(NSString *)mobilePhoneNumber
                       userId:(NSString *)userId;

///  修改个人资料
- (void)userName:(NSString *)name
          avatar:(NSString *)avatar
          gender:(NSString *)gender;

/// 更换手机号码
- (void)userMobilePhoneNumber:(NSString *)mobilePhoneNumber
                      smsCode:(NSString *)smsCode
                       userId:(NSString *)userId;

/// 修改密码
- (void)userPasswordOldPassword:(NSString *)oldPassword
                    newPassword:(NSString *)newPassword;

/// 重置密码
- (void)userReset_passwordMobilePhoneNumber:(NSString *)mobilePhoneNumber
                                    smsCode:(NSString *)smsCode
                                   password:(NSString *)password
                                oldPassword:(NSString *)oldPassword
                                newPassword:(NSString *)newPassword;

/// 获取用户信息
- (void)userInfo;

/// 修改用户设置
- (void)userConfig;

/// 用户设置
- (void)userConfigName:(NSString *)name
                avatar:(NSString *)avatar
                gender:(NSString *)gender
                  sign:(NSString *)sign
                wechat:(NSString *)wechat;

/// 通用短信验证接口
- (void)userSmsVerifyType:(NSString *)type
        mobilePhoneNumber:(NSString *)mobilePhoneNumber
                  smsCode:(NSString *)smsCode;

/// 注册用户
- (void)userRegisterMobileMobilePhoneNumber:(NSString *)mobilePhoneNumber
                                   password:(NSString *)password
                                    smsCode:(NSString *)smsCode
                                 inviteCode:(NSString *)inviteCode;

/// 发送找回密码短信
- (void)userMobilePhoneNumber:(NSString *)mobilePhoneNumber
                       userId:(NSString *)userId;

/// 发送手机短信，获取权限
- (void)userRegisterSmsMobilePhoneNumber:(NSString *)mobilePhoneNumber
                              inviteCode:(NSString *)inviteCode;

/// 发送登录短信
- (void)userSend_login_smsMobilePhoneNumber:(NSString *)mobilePhoneNumber;

/// 登录通过手机验证码
- (void)userLogin_with_smsMobilePhoneNumber:(NSString *)mobilePhoneNumber
                                    smsCode:(NSString *)smsCode;

/// 设置密码
- (void)userSet_passwordPassword:(NSString *)password
                         smsCode:(NSString *)smsCode;

/// 发送更换手机号码的验证短信 copy
- (void)userUserId:(NSString *)userId;

/// 发送短信登录验证码
- (void)userSend_login_smsMobilePhoneNumber:(NSString *)mobilePhoneNumber;

/// 设置定制服务的lastNO
- (void)userCustomServiceMenuNo:(NSString *)customServiceMenuNo
                         userId:(NSString *)userId;

/// 用户注册补全
- (void)userRegisterMake_finishMobilePhoneNumbers:
    (NSString *)mobilePhoneNumbers;

/// 获取用户信息(通过邀请码
- (void)userBy_invite_codeInvite_code:(NSString *)invite_code;

/// 获取用户鸡汤文
- (void)userWelcome;

/// 获取用户收货地址信息
- (void)userShipping_addressMobilePhoneNumber:(NSString *)mobilePhoneNumber
                                      smsCode:(NSString *)smsCode;

/// 更新用户收货地址信息
- (void)userShipping_addressShippingAddress:(NSString *)shippingAddress;

/// facebook登录
- (void)userLogin_with_facebookAccessToken:(NSString *)accessToken;

/// google登录
- (void)userLogin_with_googleIdToken:(NSString *)idToken;

/// 获取消费记录
- (void)userPurchaseHistory;

/// 获取充值记录
- (void)userChargeHistoryPagesize:(NSString *)pagesize;

/// 注销
- (void)userLogoutMobilePhoneNumber:(NSString *)mobilePhoneNumber
                            smsCode:(NSString *)smsCode;

/// 密码登录
- (void)userLoginMobilePhoneNumber:(NSString *)mobilePhoneNumber
                          password:(NSString *)password;

/// 编辑用户的wechatOpenid
- (void)userWechat_openidOpenid:(NSString *)openid;

/// 创建用户主题制作
- (void)userTopic_makeTopicId:(NSString *)topicId;

/// 获取用户主题制作列表
- (void)userTopic_makesTopicId:(NSString *)topicId;

/// 获取用户收货账户信息
- (void)userReceiving_account;

/// 更新用户收货账户信息
- (void)userReceiving_accountReceivingAccount:(NSString *)receivingAccount;

/// 判断邀请码是否可用
- (void)userInvite_codeValidInviteCode:(NSString *)inviteCode;

/// 设置分销宝入口迁移已读
- (void)userRemindFxb;

@end
