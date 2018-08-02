//
//  topic（主题）
//  ____
//
//  Created by ylin on 2018-08-02 14:56:24.
//  Copyright © 2018年 QuTui Science and Technology Co., Ltd. All rights
//  reserved.
//
//  MARK: 此文件由脚本自动生成, 手动修改文件内容, 将会被覆盖, 如需修改,
//  可在派生类进行!

#import "TopicAPI.h"

/**

topic（主题）
*/
@implementation TopicAPI

/// 获取收藏的主题
- (void)topicFavorite {
}

/// 用户收藏该主题
- (void)topicFavoriteFavoriteId:(NSString *)favoriteId {
}

/// 移除收藏的主题
- (void)topicFavoriteDeleteFavoriteId:(NSString *)favoriteId {
}

/// 获取主题菜单，推荐
- (void)menuTopicsIntro {
}

/// 获取设计师的主题
- (void)userTopicPage:(NSString *)page
             pagesize:(NSString *)pagesize
              topicId:(NSString *)topicId {
}

/// 获取主题详情
- (void)topicType:(NSString *)type topicId:(NSString *)topicId {
}

/// 获取推荐主题
- (void)topicIntroType:(NSString *)type {
}

/// 获取主题标签分类
- (void)topicCategoryTagType:(NSString *)type {
}

/// 主题搜索
- (void)topicSearchKeyword:(NSString *)keyword {
}

/// 获取推荐音乐
- (void)topicCommentCommentId:(NSString *)commentId {
}

/// 根据标签ID,获取主题列表
- (void)topicTagTagId:(NSString *)tagId {
}

/// 根据标签名获取主题列表
- (void)topicTag_nameMV {
}

/// 获取主题搜索热门关键字
- (void)topicKeywordHotType:(NSString *)type {
}

/// 获取最新主题
- (void)topic {
}

/// 获取热门主题
- (void)topicHot {
}

/// 制作数自增
- (void)topicFeedFeedId:(NSString *)feedId {
}

/// 获取推荐水印
- (void)watermarkIntro {
}

/// 获取主题分类(目前，仅music)
- (void)topicCategory {
}

/// 获取主题专辑列表
- (void)topicSpecialsType:(NSString *)type {
}

/// 获取主题专辑的主题列表
- (void)topicSpecialItemsSpecialId:(NSString *)specialId {
}

/// 获取主题专辑详情
- (void)topicSpecialSpecialId:(NSString *)specialId {
}

/// 热搜词
- (void)topicKeywordHotKeyword:(NSString *)keyword {
}

/// 获取推荐贴纸
- (void)stickerDynamicIntroPagesize:(NSString *)pagesize {
}

/// 获取推荐滤镜
- (void)filterIntro {
}

/// 获取主题标签分类(国际版)
- (void)topicCategoryListType:(NSString *)type {
}

/// 购买主题(国际版)
- (void)topicBuyAction:(NSString *)action buyId:(NSString *)buyId {
}

/// 获取已购买主题列表（国际版）
- (void)topicBoughtList {
}

/// 获取主题集合
- (void)topicSetSetId:(NSString *)setId {
}

/// 获取主题集合列表
- (void)topicSet_listAllType:(NSString *)type {
}

/// 获取推荐集合列表
- (void)topicSet_listIntroType:(NSString *)type {
}

@end
