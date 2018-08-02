//
//  activity(活动)
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

activity(活动)
*/
@interface ActivityAPI : ApiRequest

/// 获取邀请排行榜
- (void)activityInvite_setMobilePhoneNumber:(NSString *)mobilePhoneNumber
                                   password:(NSString *)password
                                    smsCode:(NSString *)smsCode
                                 inviteCode:(NSString *)inviteCode;

@end
