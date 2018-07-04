package com.qutui360.app.model;

import com.qutui360.app.modul.template.entity.MTopicEntity;
import com.qutui360.app.modul.userinfo.entity.UserInfoEntity;

import java.io.Serializable;

/**
 * Fixme:该类暂不支持任何调整 因序列化问题调整后可能导致旧数据无法读取
 * <p>
 * 视频
 * Created by Administrator on 2015/7/14.
 */
public class Feeds implements Serializable {

    private static final long serialVersionUID = 7477158916272482619L;
    public String id;
    public String content = "";
    public String brief = "";
    public String imageUrl = "";
    public String videoUrl = "";
    public int likes;
    public int comments;
    public int plays;
    public String createdAt;
    public boolean isLiked;
    public UserInfoEntity userId;
    public MTopicEntity topicId;

}
