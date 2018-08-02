//
//  feed(视频,社交数据)
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

feed(视频,社交数据)
*/
@interface FeedAPI : ApiRequest

/// 点赞
- (void)feedLikeLikeId:(NSString *)likeId;

/// 查询feed详情
- (void)feedInvite_code:(NSString *)invite_code feedId:(NSString *)feedId;

/// 播放数统计
- (void)feedPlayPlayId:(NSString *)playId;

/// 查询feed详情 copy
- (void)feedInvite_code:(NSString *)invite_code feedId:(NSString *)feedId;

@end
