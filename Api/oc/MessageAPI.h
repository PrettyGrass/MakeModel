//
//  message （消息）
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

message （消息）
*/
@interface MessageAPI : ApiRequest

/// 获取消息列表
- (void)messageListType:(NSString *)type
                   name:(NSString *)name
                 avatar:(NSString *)avatar
                 gender:(NSString *)gender
                   sign:(NSString *)sign
                 wechat:(NSString *)wechat;

/// 获取未读消息数量
- (void)messageUnreadCountType:(NSString *)type
                          name:(NSString *)name
                        avatar:(NSString *)avatar
                        gender:(NSString *)gender
                          sign:(NSString *)sign
                        wechat:(NSString *)wechat;

/// 获取续费提醒消息
- (void)messageReminderType:(NSString *)type
                       name:(NSString *)name
                     avatar:(NSString *)avatar
                     gender:(NSString *)gender
                       sign:(NSString *)sign
                     wechat:(NSString *)wechat;

@end
