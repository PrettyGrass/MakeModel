//
//  affiliate 分销（客户端不可调用）
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

affiliate 分销（客户端不可调用）
*/
@interface AffiliateAPI : ApiRequest

/// 添加奖励\返现\推荐消息
- (void)messageChargeMessages:(NSString *)messages;

/// 同步账户信息
- (void)affiliateUserAccountAffUserId:(NSString *)affUserId
                        alipayAccount:(NSString *)alipayAccount
                       alipayUsername:(NSString *)alipayUsername;

/// 获取用户的sessionToken
- (void)affiliateUserSession_tokenAffUserId:(NSString *)affUserId
                              alipayAccount:(NSString *)alipayAccount
                             alipayUsername:(NSString *)alipayUsername
                                     userId:(NSString *)userId;

/// 同步用户信息
- (void)affiliateUserAccountAffUserId:(NSString *)affUserId
                        alipayAccount:(NSString *)alipayAccount
                       alipayUsername:(NSString *)alipayUsername;

@end
