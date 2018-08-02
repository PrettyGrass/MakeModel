//
//  install（安装）
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

install（安装）
*/
@interface InstallAPI : ApiRequest

/// 上传安装数据
- (void)installDeviceType:(NSString *)deviceType
              deviceToken:(NSString *)deviceToken
                    model:(NSString *)model
                 timeZone:(NSString *)timeZone
                osVersion:(NSString *)osVersion
               deviceInfo:(NSString *)deviceInfo;

/// 更新安装数据
- (void)installDeviceType:(NSString *)deviceType
              deviceToken:(NSString *)deviceToken
                    model:(NSString *)model
                 timeZone:(NSString *)timeZone
                osVersion:(NSString *)osVersion
               deviceInfo:(NSString *)deviceInfo
                installId:(NSString *)installId;

@end
