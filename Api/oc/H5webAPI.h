//
//  h5（web端使用）
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

h5（web端使用）
*/
@interface H5webAPI : ApiRequest

/// 查询课程列表
- (void)apiGoodsCourse;

/// 查询是否存在此用户（手机号码）
- (void)apiUserExistsMobilePhoneNumber:(NSString *)mobilePhoneNumber;

/// 登录
- (void)apiUserLoginMobilePhoneNumber:(NSString *)mobilePhoneNumber
                             password:(NSString *)password;

@end
