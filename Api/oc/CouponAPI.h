//
//  coupon(优惠券)
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

coupon(优惠券)
*/
@interface CouponAPI : ApiRequest

/// 兑换优惠券
- (void)couponByCouponCodeCouponCode:(NSString *)couponCode;

/// 获取用户指定商品可用优惠券
- (void)userCouponAvailableByGoodsIdGoodsId:(NSString *)goodsId
                                 couponCode:(NSString *)couponCode;

/// 用户是否有指定商品可用优惠券
- (void)userHasCouponAvailableByGoodsIdGoodsId:(NSString *)goodsId
                                    couponCode:(NSString *)couponCode;

/// 获取用户可用优惠券
- (void)userCouponValidCouponCode:(NSString *)couponCode;

/// 获取用户不可用优惠券
- (void)userCouponInvalidCouponCode:(NSString *)couponCode;

/// 领取优惠券
- (void)couponByReceiveCouponTemplateId:(NSString *)couponTemplateId;

/// 获取用户可领取的优惠券
- (void)userCouponReceivableCouponCode:(NSString *)couponCode;

/// 查询优惠码是否可用
- (void)couponCodeUsableA0f0f385b2fd4bCouponCode:(NSString *)couponCode;

@end
