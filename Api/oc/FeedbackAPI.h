//
//  feedback （用户反馈）
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

feedback （用户反馈）
*/
@interface FeedbackAPI : ApiRequest

/// 用户反馈
- (void)feedbackContent:(NSString *)content contact:(NSString *)contact;

@end
