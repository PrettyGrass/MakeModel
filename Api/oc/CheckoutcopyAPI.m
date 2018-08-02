//
//  checkout（出帐台） copy
//  ____
//
//  Created by ylin on 2018-08-02 14:56:24.
//  Copyright © 2018年 QuTui Science and Technology Co., Ltd. All rights
//  reserved.
//
//  MARK: 此文件由脚本自动生成, 手动修改文件内容, 将会被覆盖, 如需修改,
//  可在派生类进行!

#import "CheckoutcopyAPI.h"

/**

checkout（出帐台） copy
*/
@implementation CheckoutcopyAPI

/// 获取我的历史消费记录(模板等)
- (void)checkoutHistoryPurchaseDeviceType:(NSString *)deviceType
                              deviceToken:(NSString *)deviceToken
                                    model:(NSString *)model
                                 timeZone:(NSString *)timeZone
                                osVersion:(NSString *)osVersion
                               deviceInfo:(NSString *)deviceInfo {
}

/// 充值购买记录
- (void)checkoutHistoryChargeType:(NSString *)type
                       deviceType:(NSString *)deviceType
                      deviceToken:(NSString *)deviceToken
                            model:(NSString *)model
                         timeZone:(NSString *)timeZone
                        osVersion:(NSString *)osVersion
                       deviceInfo:(NSString *)deviceInfo {
}

/// 其他账单
- (void)checkoutHistoryOtherType:(NSString *)type
                      deviceType:(NSString *)deviceType
                     deviceToken:(NSString *)deviceToken
                           model:(NSString *)model
                        timeZone:(NSString *)timeZone
                       osVersion:(NSString *)osVersion
                      deviceInfo:(NSString *)deviceInfo {
}

/// 内购支付凭证验证
- (void)checkoutVerifyReceiptOrderNo:(NSString *)orderNo
                         receiptData:(NSString *)receiptData
                           signature:(NSString *)signature {
}

/// 下订单, 或内购购买
- (void)checkoutOrderType:(NSString *)type
                coinPrice:(NSString *)coinPrice
               inviteCode:(NSString *)inviteCode
                  channel:(NSString *)channel
                  goodsId:(NSString *)goodsId {
}

/// 支付成功后，发送短信通知
- (void)checkoutNotificationCharge_succeedOrderNo:(NSString *)orderNo
                                          orderNo:(NSString *)orderNo
                                      receiptData:(NSString *)receiptData
                                        signature:(NSString *)signature
                                         timeZone:(NSString *)timeZone
                                        osVersion:(NSString *)osVersion
                                       deviceInfo:(NSString *)deviceInfo {
}

/// 获取未完成订单
- (void)checkoutHistoryUnfinishedType:(NSString *)type
                              orderNo:(NSString *)orderNo
                          receiptData:(NSString *)receiptData
                            signature:(NSString *)signature
                             timeZone:(NSString *)timeZone
                            osVersion:(NSString *)osVersion
                           deviceInfo:(NSString *)deviceInfo {
}

/// 校验邀请码是否有效
- (void)checkoutCheck_invite_codeInviteCode:(NSString *)inviteCode
                                    orderNo:(NSString *)orderNo
                                receiptData:(NSString *)receiptData
                                  signature:(NSString *)signature
                                   timeZone:(NSString *)timeZone
                                  osVersion:(NSString *)osVersion
                                 deviceInfo:(NSString *)deviceInfo {
}

/// 订单详情
- (void)checkoutHistoryDeviceType:(NSString *)deviceType
                      deviceToken:(NSString *)deviceToken
                            model:(NSString *)model
                         timeZone:(NSString *)timeZone
                        osVersion:(NSString *)osVersion
                       deviceInfo:(NSString *)deviceInfo
                        historyId:(NSString *)historyId {
}

/// 快捷服务
- (void)goodsQuick_serviceDeviceType:(NSString *)deviceType
                         deviceToken:(NSString *)deviceToken
                               model:(NSString *)model
                            timeZone:(NSString *)timeZone
                           osVersion:(NSString *)osVersion
                          deviceInfo:(NSString *)deviceInfo {
}

/// 使用现金购买记录
- (void)checkoutHistoryCashDeviceType:(NSString *)deviceType
                          deviceToken:(NSString *)deviceToken
                                model:(NSString *)model
                             timeZone:(NSString *)timeZone
                            osVersion:(NSString *)osVersion
                           deviceInfo:(NSString *)deviceInfo {
}

@end
