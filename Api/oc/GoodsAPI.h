//
//  goods（商品）
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

goods（商品）
*/
@interface GoodsAPI : ApiRequest

/// 获取店主服务商品详情
- (void)goodsMerchant_service;

/// 获取VIP会员商品详情
- (void)goodsService;

/// 获取金币商品列表
- (void)goodsCoin;

/// 获取推荐商品列表
- (void)goodsRecommendType:(NSString *)type
                  pagesize:(NSString *)pagesize
                       sid:(NSString *)sid;

/// 获取营销课程列表
- (void)goodsCourse;

/// 获取营销软件列表
- (void)goodsSoftware;

/// 获取定制商品列表
- (void)goodsCustom_servicePagesize:(NSString *)pagesize sid:(NSString *)sid;

/// 定制服务是否有小红点
- (void)userUserId:(NSString *)userId;

/// 获取快捷购买商品列表
- (void)goodsQuick_service;

/// 获取店主服务商品（新）
- (void)goodsMerchant;

/// 快捷金币
- (void)goodsQuick_coinDeviceType:(NSString *)deviceType
                      deviceToken:(NSString *)deviceToken
                            model:(NSString *)model
                         timeZone:(NSString *)timeZone
                        osVersion:(NSString *)osVersion
                       deviceInfo:(NSString *)deviceInfo;

/// 商品组列表
- (void)goodsGroupsTypes:(NSString *)types
              deviceType:(NSString *)deviceType
             deviceToken:(NSString *)deviceToken
                   model:(NSString *)model
                timeZone:(NSString *)timeZone
               osVersion:(NSString *)osVersion
              deviceInfo:(NSString *)deviceInfo;

/// 获取定制商品列表 copy
- (void)goodsCustom_servicePagesize:(NSString *)pagesize sid:(NSString *)sid;

@end
