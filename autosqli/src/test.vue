<template>
  <section class="newvip april" :style="{backgroundColor:pageConfig.color||''}">
    <!--风控滑动验证-->
    <div data-bind="get_red" data-callback="onSuccess" id="tcwireless_net_activityplatform" class="grecaptcha-badge"
      data-badge="inline" data-size="invisible" data-appid="bc4b3ca6ae27747981b43e9f4a6aa769" data-qq_007="2038384939">
    </div>
    <div class="top-header">
      <img class="header-banner" v-if="pageConfig.image" :src="pageConfig.image" />
      <img class="header-banner" v-else
        src="https://file.40017.cn/appresource/image/h5/newvipapril/bg_newvip_april_header.png" />
      <p class="red-tit" v-if="redList.length>0" v-text="redList[0].projectName+redList[0].parValue+'元红包'"></p>
      <p class="rule-tag" @click="showRule(true)">活动规则</p>
    </div>
    <div class="container">
      <!--领红包模块-->
      <div :class="isShowRedList ? 'newvip-content high' : 'newvip-content'">
        <!--首页接口红包列表空（未登录/已登录未手动领取/已登录老客已领取）-->
        <div class="unclaimed-content" v-show="!isShowRedList">
        <div v-iff="test">
          <!-- 未登录未领取（H5）-->
          <div class="wx-login" v-if="hasRetrieved==0">
            <img src="https://file.40017.cn/appresource/image/h5/newvipapril/bg_888_april_input.png?1" />
            <div class="login-box">
              <div class="red-info" v-if="redList.length>0">
                <p class="project">{{redList[0].projectName}} 大额红包</p>
                <p class="most"><span>最高</span>{{redList[0].parValue}}<em>元</em></p>
                <p class="minstart">{{redList[0].minConsume>0?'满¥'+redList[0].minConsume+'可用':'无门槛'}}</p>
              </div>
              <div class="input-box">
                <div class="input-item">
                  <input id="tel-input" v-model="mobilePhone" v-on:blur="phoneNumberCheck()" type="text" maxlength="11"
                    placeholder="输入手机号" />
                </div>
                <div class="input-item">
                  <input id="code-input" v-model="verifyCode" type="text" maxlength="6" placeholder="输入验证码" />
                  <p v-show="isShowGetCode" id="get_red" class="get-code-txt">
                    获取验证码
                  </p>
                  <p v-show="!isShowGetCode" class="get-code-txt">
                    {{verifyStr}}
                  </p>
                </div>
              </div>
              <div class="user-rule">
                <img
                  :src="getService?'//file.40017.cn/appresource/image/newvip/get_service.png':'//file.40017.cn/appresource/image/newvip/no_service.png'"
                  @click="clickService()">
                <p>点击领取即表示您已阅读并同意<span class="two"
                    @click="openNewUrl('https://app.ly.com/lion/tcServiceList?wvc3=1&tcwvcnew')">《同程旅行服务协议》</span>如您未注册同程会员，本次将为您自动注册
                </p>
              </div>
            </div>
            <div class="receive-btn" @click="getAcceptRed()">
              <img src="https://file.40017.cn/appresource/image/h5/newvipapril/btn_get.png" />
            </div>
          </div>
          <!-- 已领取（H5）-->
          <div class="received" v-else>
            <img class="receive-bg" src="https://file.40017.cn/appresource/image/h5/newvipapril/bg_red_get.png" />
            <div class="content">
              <div class="left">10<span>元</span></div>
              <div class="center">
                <p class="tit" v-text="redList[0].projectName"></p>
                <p class="min" v-text="redList[0].minConsume"></p>
              </div>
              <div class="right" @click="gotoUseRed(useUrl,'火车票')">
                <p>去使用</p>
              </div>
            </div>
          </div>
        </div>
        <!--首页红包列表非空 已领取-->
        <!--红包状态 statusId=1 未过期，3：已使用，4：已过期-->
        <div class="received-content" v-show="isShowRedList">
          <img class="right-shadow" v-if="redList.length>=3"
            src="https://file.40017.cn/appresource/image/h5/newvip/img_right_shadow.png">
          <div class="red-list" :class="{'red-list-less':redList.length < 3}">
            <div class="red-item" :class="{'red-item-gary':item.statusId!=1}" v-for="(item, index) in redList"
              :key="index" @click="
                                gotoUseRed(item.redirectUrl, item.projectName)">
              <img v-show="item.statusId==1" class="red-img"
                src="https://file.40017.cn/appresource/image/h5/newvip/bg_ylhb_new.png" />
              <img v-show="item.statusId==3||item.statusId==4" class="red-img"
                src="//file.40017.cn/appresource/image/h5/newvip/bg_ylhb_new_dis.png" />
              <div class="red-content">
                <div class="red-top">
                  <p class="title" :class="item.projectName.length > 5? 'small': ''">
                    {{item.projectName}}
                  </p>
                  <p class="price">¥{{item.parValue}}</p>
                  <p class="end-time">{{item.expireDesc}}</p>
                </div>
                <div class="red-bottom">
                  <p class="use-rule">{{item.minConsume}}</p>
                  <div class="use-btn">{{item.statusId==1?'去使用':item.statusId==3?'已使用':'已过期'}}</div>
                </div>
              </div>
            </div>
            <div style="width:15px;" v-if="redList.length>=3"></div>
            <!-- <div class="more-red-txt" @click="getMoreRed(true)">
              领取更多红包
            </div> -->
          </div>
        </div>
      </div>
      <!-- 首单领现金及项目入口 -->
      <div class="first-task-box" :class="{oneRow:!taskInfo}" v-if="!isAudit&&enterList.length>0">
        <div class="task-box" v-if="taskInfo">
          <div class="head"><img
              src="https://file.40017.cn/appresource/image/h5/newvip/img_task_yb.png"><span>首单领现金</span></div>
          <div class="card">
            <img :src="taskInfo.imageUrl">
            <!-- <p class="price"><span>¥</span>188</p>
            <p class="name">现金</p> -->
          </div>
          <div class="progress-box">
            <div class="progress">
              <p :style="{width:Math.floor(taskInfo.remainCount/(taskInfo.remainCount+taskInfo.sendCount)*100)+'%'}">
              </p>
            </div>
            <p class="progress-txt">
              还剩{{Math.floor(taskInfo.remainCount/(taskInfo.remainCount+taskInfo.sendCount)*100)}}%</p>
          </div>
          <div class="time-box">倒计时:
            <span>{{timeInfo.days}}</span>天<span>{{timeInfo.hours}}</span>时<span>{{timeInfo.minute}}</span>分<span>{{timeInfo.seconds}}</span>秒
          </div>
          <div class="get-free" @click="clickChallenge(taskInfo)">免费领</div>
        </div>
        <div class="enter-box">
          <div class="enter" v-for="(item,idx) in enterList" @click="toAppUrl(item)" :key="idx"
            style="background-size:contain" :style="{color:item.color}">
            <img class="enter-img" :src="!taskInfo?item.bgOneUrl:item.bgUrl">
            <p class="tit" v-text="item.tit"></p>
            <p class="desc" v-text="item.desc"></p>
          </div>
        </div>
      </div>

      <!--吸顶资源模块tap栏-->
      <div class="resource-tap resource-hidden">
        <resourceTypeSegmentView :resourceTypeList="resourceTypeList" :resourceType="resourceType" :isTop="true"
          v-on:changeTap="changeTap"></resourceTypeSegmentView>
      </div>

      <!--资源模块-->
      <img class="block-title-resource" src="https://file.40017.cn/appresource/image/h5/newvip/img_tit_product.png" />
      <div class="resource-content" v-show="isShowResource">

        <!-- 资源头部的选择栏控件 -->
        <resourceTypeSegmentView id="segmentView_inView" :resourceTypeList="resourceTypeList"
          :resourceType="resourceType" :isTop="false" v-on:changeTap="changeTap"></resourceTypeSegmentView>

        <div class="resource-box">
          <!-- 城市/省份选择 -->
          <div class="areaInfo " v-show="resourceType!=2">
            <div class="letfArea">
              <div class="areaChooseView" @click="changeCity()" v-show="resourceType!=4">
                <span class="city-name">{{
                                    selectCity.cityName
                               }}</span>
                <img class="tocity" src="https://file.40017.cn/appresource/image/newvip/930/icon_arrow.png" />
              </div>
              <div class="areaChooseView" @click="changeProvince()" v-show="
                                    resourceType==4&&provinceList.length
                                ">
                <span class="city-name">{{
                                    selectCity.province
                               }}</span>
                <img class="tocity" src="https://file.40017.cn/appresource/image/newvip/930/icon_arrow.png" />
              </div>
            </div>
            <div class="rightArea">
              <hotelFilterTagsView v-show="
                                    resourceType==1 &&
                                        hotel.hotelSimpleFilterInfos.length > 0
                                " :tagList="hotel.hotelSimpleFilterInfos" :hotelFilterInfo="hotel.hotelFilterInfo"
                v-on:tagClicked="hotelFilterTagClicked"></hotelFilterTagsView>
            </div>
          </div>

          <!--资源加载模态框-->
          <resourceLoadingView v-show="
                            (resourceType==1&&isHotelResourceLoading) ||
                                ((resourceType==2||resourceType==3) &&
                                    isShowDoing) ||
                                (resourceType==4&&isScenicResourceLoading)
                        ">
          </resourceLoadingView>

          <!-- 酒店资源展示 TODO：-->
          <hotelResource v-show="resourceType==1" :hotel="hotel" isShowMore: v-on:itemClicked="clickHotelItemDetail"
            v-on:redPackClicked="projectRedBtn" v-on:moreResourceBtnClicked="getMoreResource"
            v-on:noDataBtnClicked="openNewUrl"></hotelResource>

          <!-- 机票资源 -->
          <flightResource v-show="resourceType==2" :air="air" :hotResList="hotResList" :selectItem="selectItem"
            v-on:airItemClicked="airItemClicked" v-on:airHotIndexChanged="airHotIndexChanged"
            v-on:airHotSourceClicked="airHotSourceClicked" v-on:redPackClicked="projectRedBtn"
            v-on:moreResourceBtnClicked="getMoreResource" v-on:noDataBtnClicked="openNewUrl">
            <div class="flight-change" @click="changeCity()">
              <span class="city-name">{{
                                    selectCity.cityName
                               }}</span>
              <img class="tocity" src="https://file.40017.cn/appresource/image/h5/newvip/icon_arrow.png" />
            </div>
          </flightResource>

          <!--火车票资源-->
          <trainResource v-show="resourceType==3" :train="train" v-on:trainWayItemClicked="trainWayItemClicked"
            v-on:trainScenicItemClicked="trainScenicItemClicked" v-on:redPackClicked="projectRedBtn"
            v-on:moreResourceBtnClicked="getMoreResource" v-on:noDataBtnClicked="openNewUrl"></trainResource>

          <!--景区资源-->
          <div class="scenicResource" v-show="resourceType==4">
            <scenicResource :scenery="scenery" v-on:itemClicked="clickSceneryDetail"
              v-on:moreResourceBtnClicked="getMoreResource" v-on:noDataBtnClicked="openNewUrl"></scenicResource>
          </div>
        </div>
      </div>
      <!-- 项目入口 -->
      <ul class="project-enter">
        <li class="pro-enter" v-for="(item,idx) in proList" :key="idx" @click="toProject(item)">
          <p class="tit">{{item.tit}}</p>
          <p class="desc">{{item.desc}}</p>
          <img :src="item.bgUrl">
        </li>
      </ul>
      <!--底部copyright-->
      <div class="copyright-content">
        <div class="copyright-banner">
          <p>同程旅行</p>
        </div>
        <div class="icon-box">
          <div class="copyright-item">
            <img src="https://file.40017.cn/appresource/image/h5/newvip/new_user_new.png?v=20200422" />
            <p>2亿用户选择</p>
          </div>
          <div class="copyright-item">
            <img src="https://file.40017.cn/appresource/image/h5/newvip/new_b_new.png?v=20200422" />
            <p>香港上市公司</p>
          </div>
          <div class="copyright-item">
            <img src="https://file.40017.cn/appresource/image/h5/newvip/new_c_new.png?v=20200422" />
            <p>7*24全天服务</p>
          </div>
        </div>
      </div>

      <!--回到顶部按钮-->
      <div class="goto-top-btn hidden" @click="gotoTop()">
        <!-- <p class="goto-top-text">回到顶部</p> -->
        <img src="https://file.40017.cn/appresource/image/h5/newvip/img_back_to_top.png">
      </div>

      <!--分享组件-->
      <wxShareLayer v-if="shareInfo.jumpUrl != ''" v-model="isShowShare" @shareTo="shareToWhere"
        :shareEntity="shareInfo"></wxShareLayer>
      <!--城市选择组件-->
      <div class="citylist-content" v-if="isShowCity">
        <fed-city :title="title" :sName="sName" :dbList="dbList" :hasLocation="0" :extendCities="extendCities"
          :defaultData="defaultCity" :cities="cities" :clickFn="clickFn"></fed-city>
      </div>
      <!--城市省份组件-->
      <div class="citylist-content" v-if="isShowProvince">
        <fed-city :title="title" :sName="sName" :dbList="dbList" :hasLocation="0" :extendCities="provinceNull"
          :defaultData="defaultCity" :cities="provinceDatas" :clickFn="clickCFn"></fed-city>
      </div>
      <!--活动规则-->
      <div class="rule-dialog" v-show="isShowRule">
        <div class="rule-content" ontouchmove="">
          <div class="text-box">
            <p class="rule-title">活动规则</p>
            <p class="rule-txt">
              1.本活动仅支持同程旅行APP新用户参与，最高10元，最低3元；
            </p>
            <p class="rule-txt">
              2.红包规则：①领取规则：活动期间每个用户限领取一次，同一账号/手机号/设备号均视为同一用户；②有效期及使用规则：可前往“同程旅行app-我的-红包优惠券”查看；③使用规则：红包可用于预订带有红包标识产品，或订单填写页提示有可以使用红包的产品；
            </p>
            <p class="rule-txt">
              3.新人挑战：挑战任务活动规则以“挑战任务信息页-活动规则”为准；
            </p>
            <p class="rule-txt">
              4.17&16开头的手机号暂时无法参与该活动；
            </p>
            <p class="rule-txt">
              5.如果用户存在违规行为（包括但不限于洗钱、虚假交易、赌博、恶意套现、作弊、刷里程、刷红包），主办方将取消用户的活动资格，并有权撤销相关违规交易，同时依照相关规则进行处罚；
            </p>
            <p class="rule-txt">
              6.在法律允许范围内，同程旅行有权对活动规则进行适当的调整/修改。
            </p>
          </div>
        </div>
        <img class="rule-dialog-close" @click="showRule(false)"
          src="//file.40017.cn/appresource/image/h5/newvip914/close.png" />
      </div>
      <!--&lt;!&ndash;抽中里程弹框&ndash;&gt;-->
      <div class="mileage-dialog" v-show="isShowMileageDialog" ontouchmove="return false;">
        <div class="mileage-result-content">
          <img src="//file.40017.cn/appresource/image/h5/newvip914/bg.png" />
          <div class="mileage-txt-content">
            <p class="title">恭喜抽到里程啦</p>
            <p class="tips">里程可抵现可兑换好礼</p>
            <div class="red-mileage">
              <img src="//file.40017.cn/appresource/image/h5/newvip914/bg-white.png" />
              <p class="price">{{mileagePrice + "里程"}}</p>
            </div>
            <div class="btn-box">
              <img src="//file.40017.cn/appresource/image/h5/newvip914/btn_yellow.png" />
              <div class="goto-use" @click="goToUseMileage()">
                <p class="use-txt">去使用</p>
              </div>
            </div>
          </div>
        </div>
        <img class="mileage-dialog-close" @click="isShowMileageDialog = false"
          src="//file.40017.cn/appresource/image/h5/newvip914/close.png" />
      </div>
      <!--升级提示-->
      <div class="go-up-dialog" v-show="isShowGoUpDialog" ontouchmove="return false;">
        <div class="goup-content">
          <p class="title">您是游币用户，</p>
          <p class="tips">参与抽奖需先升级为里程用户哦~</p>
          <div class="btn-box">
            <img src="//file.40017.cn/appresource/image/h5/newvip914/btn_yellow.png" />
            <div class="goto-use" @click="goUpToMileageShop()">
              <p class="use-txt">去升级为里程用户</p>
            </div>
          </div>
        </div>
        <img class="goup-dialog-close" @click="isShowGoUpDialog = false"
          src="//file.40017.cn/appresource/image/h5/newvip914/close.png" />
      </div>
      <skeleton v-if="isShowLoading"></skeleton>
      <!--吐司弹框-->
      <toast ref="toastV"></toast>
      <!--网络错误-->
      <netWorkErr v-show="isNoNetWork"></netWorkErr>
      <doing v-show="isShowDoing2" :text="doingText"></doing>
      <show-dialog v-show="isShowDialog" :dialogInfo="dialogInfo" @handleLeft="h5GuideRedCenter()"
        @handleRight="h5Hide()" />
    </div>
  </section>
</template>

<script>
import "@/untils/bridge.3.1.2.js";
import bridgeFnc from "bridgefnc";
import commonFnc from "@/untils/commonFnc.js";
import commonlyFnc from "@/untils/commonlyFnc.js";
import tcLoading from "@/components/common/tcLoading";
import doing from "@/components/common/doing";
import netWorkErr from "@/components/common/netWorkErr";
import toast from "@/views/newvip_zy/toastNew";
import wxShareLayer from "@/views/newvip_zy/wxShareLayer";
import skeleton from "@/components/common/newvipskeleton";
import resourceTypeSegmentView from "@/components/newvip/resourceTypeSegmentView";
import resourceLoadingView from "@/components/newvip/resourceLoadingView";
import scenicResource from "@/components/newvip/scenicResource";
import hotelResource from "@/components/newvip/hotelResource";
import hotelFilterTagsView from "@/components/newvip/hotelFilterTagsView";
import trainResource from "@/components/newvip/trainResource";
import flightResource from "@/components/newvip/flightResource";
import showDialog from '@/components/common/showDialog'


// let serviceBase = "//servicegw.t.ly.com/gateway/as/v1/dsf/wireless/front/activityservice/",//预发
// serviceToken = "?Labrador-Token=09be6d59-2b3e-49fc-9fda-2c9ecd260329",//预发token
let serviceBase = "//servicegw.ly.com/gateway/as/v1/dsf/wireless/front/activityservice/", //线上
  serviceToken = "?Labrador-Token=c2167576-9a81-4eb3-ad29-67c1fd724cf1", //线上token
  // 新接口
  baseUrl = 'https://tcmobileapi.17usoft.com',
  // baseUrl = 'https://tcmobileapitest1.17usoft.com',
  cityService = serviceBase + "cityarea/getcityarealist/" + serviceToken, //城市列表
  tranTabService =
    serviceBase + "newexclusiveapi/querytablist/" + serviceToken, //酒店火车票机票资源
  sceneryTabService =
    serviceBase + "newexclusiveapi/QuerySceneryList/" + serviceToken,
  drawMileageService = serviceBase + "newmember/DrawMileage/" + serviceToken, //抽里程
  queryStatusService =
    serviceBase + "newmember/QueryMemberStatus/" + serviceToken, //查询抽奖状态
  hotelService = serviceBase + "/newmember/queryresource/" + serviceToken,
  airService = "https://tcmobileapi.17usoft.com/activityservice/newMember/getFlightList"; //酒店资源接口

let refid = commonFnc.getQueryString("refid") ||
  commonFnc.getHashString("refid") ||
  "",
  activityNo = commonFnc.getQueryString('activityNo') || commonFnc.getHashString('activityNo') || "";
export default {
  components: {
    toast,
    wxShareLayer,
    netWorkErr,
    tcLoading,
    doing,
    skeleton,
    resourceTypeSegmentView,
    resourceLoadingView,
    scenicResource,
    hotelResource,
    hotelFilterTagsView,
    trainResource,
    flightResource,
    showDialog
  },
  data() {
    return {
      isTC: commonFnc.isTC(),
      isAudit: false, // 是否是审核模式，"0" 否；"1" 是。 隐藏部分模块
      timeInfo: {},
      taskInfo: "",
      pageConfig: {
      },
      heightApp: $(window).height(),
      wWidth: $(window).width() / 4,
      hasLoacate: false,
      isShowCity: false,
      isShowProvince: false,
      isShowShare: false,
      isShowLoading: true,
      isShowDoing: true, //机票、火车资源加载loading
      isHotelResourceLoading: true, //酒店资源加载loading
      isScenicResourceLoading: true, //景点资源加载loading
      isShowDoing2: false,
      doingText: "抽取中..",
      isNoNetWork: false, //
      isShowRedList: false, //是否显示红包列表
      // isShowCodeDialog: false, //app内短信验证
      vericodeType: 1,
      isShowRule: false, //规则弹屏
      isShowGetCode: true, //验证
      isShowMileageDialog: false, //抽中里程弹框
      isShowGoUpDialog: false, //引导升级里程商城
      isShowResource: true, //展示资源页面
      defaultimg:
        "//file.40017.cn/appresource/image/common/default2-1.jpg",
      shareId: this.getParams("shareId") || "",
      trackId: this.getTrackId(),
      memberId: "",
      deviceId: "",
      selectItem: 0,
      resourceType: 1, //1:酒店资源，2：机票 ，3：火车票，4：景区
      enterList: [],
      proList: [],
      selectCity: {
        cityId: "321",
        cityName: "上海",
        lon: "121.47", //经度
        lat: "31.23", //纬度
        province: "上海"
      },
      2: "",
      resource: {},
      //资源类型列表
      resourceTypeList: [
        {
          title: "特惠住",
          name: "酒店"
        },
        {
          title: "特价飞",
          name: "机票"
        },
        {
          title: "快速买",
          name: "火车"
        },
        {
          title: "限时惠",
          name: "景区"
        }
      ],
      air: {
        airList: [],
        airRed: [],
        airUrl: ""
      }, //机票资源
      train: {
        trainList: [],
        trainRed: [],
        trainUrl: ""
      }, //火车票
      hotel: {
        hotelRed: [],
        hotelUrl: "",
        hotelFilterInfo: {
          filterId: 0,
          filterName: "4.5分以上",
          filterParamId: 0,
          filterTypeId: 1020
        }, //酒店过滤信息
        hotelSimpleFilterInfos: [], //过滤标签
        hotelList: []
      },
      scenery: {
        sceneryList: [],
        sceneryUrl: ""
      },
      taskList: [],
      provinceList: [],
      memberRightList: [],
      dotList: [],
      dotPage: 0,
      hotResList: [],
      sortCityList: {},
      //app外部
      verifyStr: "获取验证码",
      timeCount: 60,
      mobilePhone: "", //用户输入的手机号
      verifyCode: "", //验证码

      //app内
      redMobile: "",
      // redCode: "", //短信验证码
      redCodeBtn: false,
      hasRetrieved: 0, //是否领取过红包，默认是未领取 0：未领取，1：已领取
      isNewMember: 1, //是否是新人，默认是1 ，0：不新客，1：新客
      redList: [], //红包列表

      mileageType: 0, //0是未升级 1是真实里程 2虚拟 3不可升级

      mileageStatus: 1, //1未领取新人红包 2已领新人红包未下单  3已领已下 4已抽 5不满足条件 6需要升级里程账户 7非指定项目
      mileagePrice: "", //抽取得的里程数

      jy_response: "", //滑动验证
      jy_type: "", //滑动验证
      //城市选择组件
      title: "请输入城市名称(如北京,bj,Beijing)",
      sName: "",
      dbList: false,
      extendCities: [],
      defaultCity: [],
      cities: [],
      provinceDatas: [],
      provinceNull: [],
      useUrl: `https://m.17u.cn/app/links/react/page?trnLogin=1&projectId=110004&immersive=1&wakeRefid=${refid}&wakePwdId=0`,
      clickFn: data => {
        var cityInfo = data && JSON.parse(data.CBData);
        this.isShowCity = false;
        if (this.selectCity.cityId != cityInfo.cityInfo.cityId) {
          this.selectCity.cityName = cityInfo.cityInfo.cityName;
          this.selectCity.cityId = cityInfo.cityInfo.extend;
          this.trackData(
            "^定位^h5^" +
            this.selectCity.cityName +
            "^"
          );
          this.getQueryTabList(1);

          setTimeout(function () {
            var scrollTop = $(window).scrollTop();
            window.scrollTo(0, scrollTop);
          }, 100);
        }
      },
      clickCFn: data => {
        var info = data && JSON.parse(data.CBData);
        this.isShowProvince = false;
        this.selectCity.province = info.cityInfo.cityName;
        this.trackData(
          "^定位^h5^" +
          this.selectCity.province +
          "^"
        );
        this.getSceneryList(true);
      },
      shareTo: "", //分享至朋友圈、微信好友
      shareInfo: {
        jumpUrl: "",
        sharetxt: "数量有限，先到先得",
        title: "10元火车票红包，速抢",
        img:
          "https://file.40017.cn/appresource/image/activityPlatform/oldBeltNew/fenxiang.png"
      },
      flag: true,
      needReload: false,
      getService: false,//勾选服务协议
      isShowDialog: false,
      dialogInfo: {
        title: '',
        subtitle: '您已经是尊贵的老用户啦，更多超值会员福利等你领',
        left: '放弃福利',
        right: '去看看',
        isDouble: true,
      },
    };
  },
  watch: {
    // redCode: function(newval) {
    //     if (newval.length >= 4) {
    //         this.redCodeBtn = true;
    //     }
    // }
  },
  created() {
    let that = this;
    this.init();
    this.configTrackInfo();
    _tc_bridge_util.set_webview_info({
      param: {
        webview: {
          dragAble: "false"
        }
      },
      callback: function (data) { }
    });
    window.onSuccess = (response, type) => {
      that.jy_response = response;
      that.jy_type = type;
      //    别的回调
      that.sendMessageCode();
    };
    window._tc_web_bar = {
      //头部
      tag_isStop: data => {
        if (data.isStop == "true" || data.isStop === true) {
          //失活
        } else {
          //激活..
          if (that.needReload) {
            window.location.reload();
            this.needReload = false;
          }
        }
      }
    };
  },
  mounted() {
    var that = this;
    that.isShowGotoTop();
    that.configWxShare();
    commonFnc.remHandle();
    setTimeout(() => {
      commonFnc.remHandle();
    }, 1000)
  },
  methods: {
    toAppUrl(item) {
      let that = this;
      location.href = item.jumpWxUrl
      that.trackData(`^常规活动^h5^${that.memberId ? 'Y' : 'N'}^${item.track || item.tit}^${refid}^`);
    },
    jump(url) {
      this.openNewUrl(url)
    },
    toProject(item) {
      let that = this;
      that.jump(item.jumpUrl);
      that.trackData(`^底部推荐h5^${that.memberId ? 'Y' : 'N'}^${item.tit}^${refid}^`);
    },
    back() {
      let that = this;
      that.trackData(
        `^backbutton^app^${that.memberId == "" ? "N" : "Y"
        }^${that.hasRetrieved}^`
      );
      that.trackData(`^挽留弹框^app^${that.memberId ? 'Y' : 'N'}^放弃福利^${refid}^`);
      _tc_bridge_util.set_webview_back();
    },
    init() {
      let that = this;
      this.configVerify();
      this.getCityList();
      that.getTcMid().then(resolve => {
        commonFnc.weixinTitle("同程旅行新人专区");
        that.isShowLoading = false;
        that.getQueryIndexInfo();
        that.getQueryTabList();
        that.getSceneryList();
        that.getTaskList();
      })
      that.getMemberRights();
    },
    getTcMid() {
      let that = this,
        openId = that.getParams("openId");
      return new Promise((resolve) => {
        if (openId) {
          $.ajax({
            type: "post",
            dataType: "json",
            contentType: "application/json",
            url: serviceBase + "common/querybind/" + serviceToken,
            data: JSON.stringify({
              openId: openId
            }),
            success: function (data) {
              if (data.data.ResCode == '0000') {
                that.memberId = data.data.Body || '0';
              } else {
                that.memberId = '0';
              }
              resolve()
            },
            error: function (data) {
              resolve();
            }
          });
        } else {
          resolve();
        }
      })
    },
    /**
     * 引入滑动验证js
     * */
    configVerify() {
      let new_element = document.createElement("script");
      new_element.async = true;
      new_element.setAttribute("type", "text/javascript");
      new_element.setAttribute(
        "src",
        "//jy.17u.cn/recaptcha/api.js?project_id=tcwireless_net_activityplatform&timestamp=" +
        new Date()
      );
      document.body.appendChild(new_element);
      new_element.onload = () => {
        console.log(233333)
      };
    },
    /**
     * 配置微信分享
     * */
    configWxShare() {
      let that = this;
      commonlyFnc.configWXShare({
        img:
          "https://pic5.40017.cn/i/ori/XAlPtwxKzS.png",
        jumpUrl: location.origin + "/h5/Vue/" + location.hash,
        title: "10元火车票红包，速抢",
        sharetxt: "数量有限，先到先得"
      });
    },
    /**
     * 分享路径
     * */
    shareToWhere(data) {
      this.shareTo = data;
      this.trackData(
        `^share^app^${this.memberId != "" ? "Y" : "N"}^${this.shareTo
        }^`
      );
    },
    /**
     * 进主页面请求
     * */
    getQueryIndexInfo() {
      let that = this,
        reqBody = {};
      return new Promise((resolve, reject) => {

        $.ajax({
          type: "post",
          dataType: "json",
          contentType: "application/json",
          url:
            baseUrl + "/activityservice/marketTemplate/activityInfo",
          data: JSON.stringify({
            refid,
            activityNo
          }),
          success: function (data) {
            let resCode = data && data.statusCode;
            if (resCode === 0) {
              let body = data && data.data;

              /******** 测试数据 ********/
              // body.redList = [{
              //   endTime: "2020-08-08",
              //   projectName: "火车票",
              //   minConsume: "满5",
              //   statusId: "1",
              //   parValue: "5",
              //   redirectUrl: "http://m.ly.com"
              // }, {
              //   endTime: "2020-08-08",
              //   projectName: "火车票",
              //   minConsume: "满5",
              //   statusId: "1",
              //   parValue: "5",
              //   redirectUrl: "http://m.ly.com"
              // }, {
              //   endTime: "2020-08-08",
              //   projectName: "火车票",
              //   minConsume: "满5",
              //   statusId: "1",
              //   parValue: "5",
              //   redirectUrl: "http://m.ly.com"
              // }, {
              //   endTime: "2020-08-08",
              //   projectName: "火车票",
              //   minConsume: "满5",
              //   statusId: "1",
              //   parValue: "5",
              //   redirectUrl: "http://m.ly.com"
              // }, {
              //   endTime: "2020-08-08",
              //   projectName: "火车票",
              //   minConsume: "满5",
              //   statusId: "3",
              //   parValue: "5",
              //   redirectUrl: "http://m.ly.com"
              // }]


              /******** 测试数据 ********/


              that.redList = body.redList;//redList非空即为新客且存在有效新人礼包直接展示
              that.pageConfig = body.activityInfo || {};
              if (body.middleAdv && body.middleAdv.length > 0) {
                body.middleAdv.forEach(item => {
                  item.jumpWxUrl = that.$linkUrl(item.jumpUrl, { wakeRefid: refid })
                });
                that.enterList = body.middleAdv;
              }
              console.log(that.enterList)
              that.proList = body.bottomAdv || [];
              if (that.redList.length != 0 && that.hasRetrieved != '0') {
                that.isShowRedList = true;
              }
              that.$nextTick(function () {
                that.isShowLoading = false;
                that.trackData(
                  `^enter^h5^${that.memberId == "" ? "N" : "Y"
                  }^${that.hasRetrieved}^`
                );
              });
            } else {
              that.isNoNetWork = true;
            }
            resolve();

          },
          error: function (data) {
            that.isNoNetWork = true;
            resolve();
          }
        });
      })
    },
    /**
     * 领取更多红包链接
     * */
    getMoreRed(isFirst) {
      let that = this;
      debugger;
      that.openNewUrl(
        "https://m.17u.cn/app/links/react/page?projectId=110008&trnLogin=1"
      );

      if (isFirst) {
        that.trackData(
          `^领取更多红包1^h5^Y^`
        );
      } else {
        that.trackData(
          `^领取更多红包2^h5^Y^`
        );
      }
    },
    /**
     * 资源项目红包按钮跳转
     * type:
     * 0:不显示项目红包，不做跳转
     * 1：显示项目红包，提示去领取
     * 2：显示项目红包，提示去使用
     */
    projectRedBtn(projectRed) {
      var that = this,
        url = projectRed.wxJumpUrl;
      if (projectRed.type == "1" || projectRed.type == 1) {
        that.trackData(
          `^资源推荐^${projectRed.projectName}^h5^去领取^Y^`
        );
        window.scrollTo(0, 0);
      } else if (projectRed.type == "2" || projectRed.type == 2) {
        that.trackData(
          `^资源推荐^${projectRed.projectName}^h5^去使用^Y^`
        );
        that.openNewUrl(url);
      }
    },
    /**
     * 领取红包
     * */
    getAcceptRed(isApp) {
      let that = this;
      that.trackData(
        `^红包领取^h5^${that.memberId == "" ? "N" : "Y"
        }^${that.hasRetrieved}^`
      );
      if (!/^1\d{10}/g.test(that.mobilePhone)) {
        this.$refs.toastV.show("请输入正确的手机号", 2500);
        return;
      } else if (!that.verifyCode) {
        this.$refs.toastV.show("请输入验证码", 2500);
        return;
      }
      if (!that.getService) {
        this.$refs.toastV.show("请阅读并点击确认服务协议哦", 2500);
        return;
      }
      if (that.flag) {
        that.flag = false;
        $.ajax({
          type: "post",
          dataType: "json",
          contentType: "application/json",
          url:
            baseUrl + "/activityservice/marketTemplate/retrieveCoupon",
          data: JSON.stringify({
            refid,
            activityNo,
            mobile: that.mobilePhone,
            verifyCode: that.verifyCode
          }),
          success: function (data) {
            that.flag = true;
            // data.statusCode = 0;
            // data.data = [{
            //   "parValue": "2",
            //   "projectName": "火车票",
            //   "beginTime": "2021-04-12 00:00:00",
            //   "endTime": "2021-04-18到期",
            //   "minConsume": "满¥20使用",
            //   "redirectUrl": "tctclient://web/hy?id=83&route=index.html%23%2Findex",
            //   "usedPeople": "0",
            //   "timeLong": "0",
            //   "activeTime": "2021-04-12 16:48:04",
            //   "sill": 20.0,
            //   "type": 0,
            //   "expireDesc": "",
            //   "timeType": 0,
            //   "group": 0,
            //   "scene": "",
            //   "desc": "",
            //   "remark": "",
            //   "isGetMore": 0,
            //   "couponNo": "AP_CO_TC4Q3JZTK3H54NAF375JXJ5H",
            //   "statusId": "1",
            //   "statusText": "立即使用",
            //   "couponType": "0",
            //   "amtPrefix": "",
            //   "dailyMaxCount": 0,
            //   "mileagePrice": 0,
            //   "amtSuffix": "",
            //   "minOrderAmt": "",
            //   "consumeTime": "",
            //   "projectCodeUsed": "H",
            //   "sort": 0
            // }];
            console.log(data)
            let resCode = data.statusCode;
            let resDesc = data.message;
            if (resCode == 3) {
              //老客
              that.isShowDialog = true;
              $('body').css({ position: 'fixed' })
              return;
            }
            if (resCode == 0) {
              that.redList = data.data;
              that.trackData(
                `^红包领取^h5^Y^1^${that.form}^`
              );
              that.memberTrack("接口领取成功");
              that.hasRetrieved = 1;
              that.getQueryTabList();
              // if (that.redList.length != 0 && that.hasRetrieved != '0') {
              //   that.isShowRedList = true;
              //   window.scrollTo(0, 0);
              // }
            } else {
              that.trackData(
                `^红包领取^h5^Y^0^`
              );
              that.$refs.toastV.show(
                resDesc,
                2500
              );
            }
          },
          error: function (data) {
            that.flag = true;
            console.log(2)
          }
        });
      }
    },
    // 勾选服务协议
    clickService() {
      this.getService = !this.getService;
    },
    h5GuideRedCenter() {
      this.isShowDialog = false;
      $('body').css({ position: 'static' })
      // this.hasRetrieved = 1;
    },
    h5Hide() {
      this.openNewUrl('https://m.17u.cn/app/links/react/page?projectId=110008&trnLogin=1&wakeRefid=' + refid + '&wakePwdId=0')
    },
    /**
     * 红包去使用
     * */
    gotoUseRed(url, redName) {
      let that = this;
      this.trackData(
        `^去使用红包^h5^Y^${redName}^`
      );
      this.openNewUrl(url);
    },
    tomileage() {
      this.needReload = true;
      this.openNewUrl(
        "https://m.17u.cn/app/links/react/page?trnLogin=1&pathName=mileageIndex&&projectId=112003&showback=1"
      );
    },
    /**
     * 获取酒店火车票机票资源
     * form==1 未切换资源模块
     * */
    getQueryTabList(form) {
      //单独调酒店接口
      this.getHotelList();

      this.isShowDoing = true;
      let that = this,
        reqBody = {
          cityId: that.selectCity.cityId,
          cityName: that.selectCity.cityName
        };
      if (that.isTC) {
        reqBody.memberId = that.memberId;
        reqBody.reqFrom = "app";
      } else {
        reqBody.mobile = that.mobilePhone;
        reqBody.reqFrom = "wx";
      }
      commonFnc.getData(
        {
          url: tranTabService,
          params: JSON.stringify(reqBody),
          cb: function (data) {
            that.isShowDoing = false;
            let resCode = data && data.data && data.data.ResCode;
            if (resCode === "0000") {
              let body = data && data.data && data.data.Body;
              that.resource = body;
              that.train.trainList = body.trainList;
              if (that.isNewMember == 1) {//未登录或者新客展示红包
                that.air.airRed = body.airRed;
                that.train.trainRed = body.trainRed;
                that.hotel.hotelRed = body.hotelRed;
              }
              if (that.isTC) {
                that.air.airUrl = body.airUrl;
                that.train.trainUrl = body.trainUrl;
                that.hotel.hotelUrl = body.hotelUrl;
              } else {
                that.air.airUrl = body.airWxUrl;
                that.train.trainUrl = body.trainWxUrl;
                that.hotel.hotelUrl = body.hotelWxUrl;
              }
              // that.hotResList = body.hotResList.data;
            } else {
              if (form == 1 && form == "1") {
                this.$refs.toastV.show(
                  "加载资源失败，请重试！",
                  2500
                );
              } else {
                this.isShowResource = false;
              }
            }
          }
        },
        "post"
      );
      $.ajax({
        type: "post",
        dataType: "json",
        contentType: "application/json",
        url: airService,
        data: JSON.stringify(reqBody),
        success: function (data) {
          let resCode = data && data.statusCode;
          if (resCode == "0") {
            that.air.airList = data.data.priceList;
            that.hotResList = data.data.themeList;
          }
        },
        error: function (data) {
        }
      });
    },

    /**
     * 获取酒店资源
     */
    getHotelList() {
      this.isHotelResourceLoading = true;

      let that = this,
        reqBody = {};
      if (that.isTC) {
        reqBody.memberId = that.memberId || "0";
        reqBody.reqFrom = "app";
      } else {
        reqBody.reqFrom = "wx";
      }
      reqBody.cityID = that.selectCity.cityId || "";
      reqBody.pageIndex = 1;
      reqBody.pageSize = 20;

      let tempFilterInfo = {};
      if (that.hotel.hotelFilterInfo) {
        let hotelFilterInfo = that.hotel.hotelFilterInfo;

        tempFilterInfo.filterId = hotelFilterInfo.filterId;
        tempFilterInfo.filterTypeId = hotelFilterInfo.filterTypeId;
        tempFilterInfo.nameCn = hotelFilterInfo.filterName;
      }
      reqBody.hotelSimpleFilterInfo = [tempFilterInfo];

      $.ajax({
        type: "post",
        dataType: "json",
        contentType: "application/json",
        url:
          "https://tcmobileapi.17usoft.com/activityservice/newMember/getHotelList",
        data: JSON.stringify(reqBody),
        success: function (data) {
          that.isHotelResourceLoading = false;

          let dataBody = data.data;
          that.hotel.hotelSimpleFilterInfos =
            dataBody.hotelSimpleFilterInfos;
          that.hotel.hotelList = dataBody.hotelList;
        },
        error: function (data) {
          that.isHotelResourceLoading = false;
        }
      });
    },

    /*获取景区资源*/
    getSceneryList(hint) {
      this.isScenicResourceLoading = true;

      let that = this,
        reqBody = {
          areaName: that.selectCity.province
        };
      if (that.isTC) {
        reqBody.memberId = that.memberId;
        reqBody.reqFrom = "app";
      } else {
        reqBody.mobile = that.mobilePhone;
        reqBody.reqFrom = "wx";
      }
      commonFnc.getData(
        {
          url: sceneryTabService,
          params: JSON.stringify(reqBody),
          cb: function (data) {
            that.isScenicResourceLoading = false;

            let resCode = data && data.data && data.data.ResCode;
            if (resCode === "0000") {
              let body = data && data.data && data.data.Body;
              that.scenery.sceneryList = body.resourceList;
              that.provinceList = body.proList;
              if (that.isTC) {
                that.scenery.sceneryUrl =
                  "tctclient://scenery/home";
              } else {
                that.scenery.sceneryUrl =
                  "https://m.17u.cn/app/links/scenery/home";
              }
            } else {
              if (hint) {
                this.$refs.toastV.show(
                  "加载资源失败，请重试！",
                  2500
                );
              }
            }
          }
        },
        "post"
      );
    },
    /*获取任务列表*/
    getTaskList() {
      let that = this,
        reqBody = {};
      return new Promise(resolve => {
        if (that.isTC) {
          reqBody.memberId = that.memberId || "0";
          reqBody.reqFrom = "app";
        } else {
          reqBody.reqFrom = "wx";
        }
        $.ajax({
          type: "post",
          dataType: "json",
          contentType: "application/json",
          url: "https://tcmobileapi.17usoft.com/activityservice/newMember/getTaskList",
          data: JSON.stringify(reqBody),
          success: function (data) {
            that.taskList = data.data || [];
            if (that.taskList.length > 0) {
              that.taskInfo = that.taskList[0];
              let nowtime = +new Date();
              if (nowtime < +that.taskInfo.endtime) {
                that.timeInfo = that.getDayTime(+that.taskInfo.endtime, nowtime)
                that.cutDown(+that.taskInfo.endtime);
              }
            } else {
              that.taskInfo = ''
            }
            resolve()
          },
          error: function (data) {
            resolve()
          }
        });
      })
    },
    cutDown(endtime) {
      let that = this;
      if (window.newvip_interval)
        clearInterval(window.newvip_interval)
      window.newvip_interval = setInterval(() => {
        let nowtime = +new Date();
        that.timeInfo = that.getDayTime(endtime, nowtime);
        if (that.timeInfo.dateDiff < 1000) {
          location.reload();
          clearInterval(window.newvip_interval)
        }
      }, 1000)
    },
    getDayTime(dateend, datenow) {
      //如果时间格式是正确的，那下面这一步转化时间格式就可以不用了
      let dateDiff = dateend - datenow;//时间差的毫秒数
      //计算出相差天数
      let days = Math.floor(dateDiff / (24 * 3600 * 1000));
      let leave1 = dateDiff % (24 * 3600 * 1000) //计算天数后剩余的毫秒数
      let hours = Math.floor(leave1 / (3600 * 1000))//计算出小时数
      //计算相差分钟数
      let leave2 = leave1 % (3600 * 1000) //计算小时数后剩余的毫秒数
      let minute = Math.floor(leave2 / (60 * 1000))//计算相差分钟数
      //计算相差秒数
      let leave3 = leave2 % (60 * 1000) //计算分钟数后剩余的毫秒数
      let seconds = Math.floor(leave3 / 1000)
      return {
        days,
        hours,
        minute,
        seconds,
        dateDiff
      }
    },
    getMemberRights() {
      let that = this,
        reqBody = { source: "index" };
      if (that.isTC) {
        reqBody.reqFrom = "app";
      } else {
        reqBody.reqFrom = "wx";
      }
      $.ajax({
        type: "post",
        dataType: "json",
        contentType: "application/json",
        url:
          "https://tcmobileapi.17usoft.com/activityservice/newMember/getMemberRights",
        data: JSON.stringify(reqBody),
        success: function (data) {
          let response = data.data,
            list = [];
          response.indexList.map((project, index) => {
            if (index % 4 == 0) {
              that.dotList.push(1);
            }
          });
          that.memberRightList = response.indexList;
          that.computeScroll();
        },
        error: function (data) { }
      });
    },
    /**
     *查看更多里程资源
     * */
    gotoMoreMileage() {
      let that = this;
      that.trackData(`^更多^${that.isTC ? "app" : "h5"}^`);
      that.judgeUrl();
    },
    /**
     * 去使用
     * */
    goToUseMileage() {
      let that = this;
      that.trackData(`^去使用^${that.isTC ? "app" : "h5"}^`);
      that.judgeUrl();
    },
    /**
     * 查看更多资源跳转
     */
    getMoreResource(url, projectName) {
      this.trackData(
        `^查看更多^${this.isTC ? "app" : "h5"}^${this.memberId != "" ? "Y" : "N"
        }^${projectName}`
      );
      this.openNewUrl(url);
    },
    computeScroll() {
      return;

      if (this.memberRightList.length < 5) return;

      let that = this,
        distancepoiX = 0,
        startpoiX = 0,
        distancepoiY = 0,
        startpoiY = 0,
        sTop = 0,
        range = 80,
        moveWidth = $(window).width() - 20,
        totalcount = that.dotList.length,
        movelength = 0;

      $(".priority-scroll").on("touchstart", function (event) {
        sTop = $(window).scrollTop();
        distancepoiX = 0; //滑动距离重置，防止点击后直接滑动
        startpoiX = event.touches[0].pageX;
        distancepoiY = 0;
        startpoiY = event.touches[0].pageY;
        movelength = -that.dotPage * moveWidth; //记录上次滑动距离
        setCssStyle(movelength, 0); //防止
      });
      $(".priority-scroll").on("touchmove", function (event) {
        distancepoiX = event.touches[0].pageX - startpoiX;
        distancepoiY = event.touches[0].pageY - startpoiY;
        //                        $(window).scrollTop(sTop - distancepoiY);
        if (
          (that.dotPage == 0 && distancepoiX > 0) ||
          (that.dotPage == totalcount - 1 && distancepoiX < 0)
        ) {
          return;
        }
        setCssStyle(distancepoiX + movelength, 0); //滑动中...
        event.preventDefault();
      });
      $(".priority-scroll").on("touchend", function (event) {
        if (distancepoiX >= range && that.dotPage > 0) {
          that.dotPage--; //下滑--右划
        } else if (
          -distancepoiX >= range &&
          that.dotPage < totalcount - 1
        ) {
          that.dotPage++; //上划--左划
        }
        setCssStyle(-that.dotPage * moveWidth, 0.5); //实时滑动距离
      });

      function setCssStyle(length, time) {
        $(".priority-list").css({
          transform: "translate3d(" + length + "px,0,0)",
          "-webkit-transform": "translate3d(" + length + "px,0,0)",
          transition: time + "s",
          "-webkit-transition": time + "s"
        });
      }
    },
    /**
     * 查看运营版块资源
     */
    openAdvertiseUrl(item) {
      this.trackData(
        `^promotion^${this.isTC ? "app" : "h5"}^${item.advName
        }^`
      );
      this.openNewUrl(item.redirectUrl);
    },
    /**
     * 跳转判断
     * */
    judgeUrl() {
      let that = this;
      if (that.mileageType ==1&&that.taskInfo==2) {
        //真实里程，可以正常兑换
        if (that.isTC) {
          that.openNewUrl(
            "https://appnew.ly.com/sign/newsign/#/newsign"
          );
        } else {
          that.openNewUrl(that.$linkUrl('https://appnew.ly.com/sign/newsign/#/newsign', { wakeRefid: refid }));
        }
      } else if (
        that.mileageType == 0 ||
        that.mileageType == 2 ||
        that.mileageType == 4 ||
        that.mileageType == 6 ||
        that.mileageType == 7
      ) {
        // 非app里程用户，需绑定微信升级
        that.goUpToMileageShop();
      } else if (
        that.mileageType == 8 ||
        that.mileageType == 9 ||
        that.mileageType == 10
      ) {
        //虚拟里程，需绑定微信升级
        if (that.isTC) {
          that.openNewUrl(
            " https://appnew.ly.com/sign/newsign/?newAppUser=1#/newsign"
          );
        } else {
          that.openNewUrl(that.$linkUrl('https://appnew.ly.com/sign/newsign/?newAppUser=1#/newsign', { wakeRefid: refid }));
        }
      }
    },
    /**
     * 里程模块
     *查询抽奖状态
     * status ：1 未领取新人红包，2已领新人红包未下单，3已领已下单，4已抽
     * */
    queryMileageStatus() {
      let that = this,
        reqBody = {};
      if (that.isTC) {
        reqBody.memberId = that.memberId;
        reqBody.reqFrom = "app";
      } else {
        return;
      }
      commonFnc.getData({
        url: queryStatusService,
        params: JSON.stringify(reqBody),
        cb: function (data) {
          let resCode = data && data.data && data.data.ResCode;
          if (resCode === "0000") {
            let body = data && data.data && data.data.Body;
            that.mileageStatus = body.status;
            that.mileagePrice = body.mileage;
          } else {
            //查询失败显示默认
            that.mileageStatus = 1;
          }
        }
      });
    },

    /**
     * 去下单
     * */
    gotoTakeOrder() {
      if (this.isTC) {
        this.trackData(`^去下单^app^`);
        this.openNewUrl("tctclient://homepage/homePage");
      } else {
        this.openNewUrl(this.$linkUrl('tctclient://homepage/homePage', { wakeRefid: refid }));
      }
    },
    /**
     * 抽里程
     * */
    getDrawMileage(status) {
      let that = this;
      if (status == 6) {
        that.isShowGoUpDialog = true;
        return;
      }
      that.isShowDoing2 = true;
      that.trackData(`^抽里程^${that.isTC ? "app" : "h5"}^`);
      commonFnc.getData({
        url: drawMileageService,
        params: JSON.stringify({
          memberId: that.memberId
        }),
        cb: function (data) {
          let resCode = data && data.data && data.data.ResCode,
            rspType = data && data.data && data.data.rspType;
          if (rspType == "55" || rspType == "77" || rspType == "88") {
            that.$refs.toastV.show(
              "网络未开启，请检查网络设置",
              2500
            );
          }
          if (resCode === "0000") {
            //抽取成功
            let body = data && data.data && data.data.Body;
            that.mileagePrice = body.mileage;
            that.isShowDoing2 = false;
            that.isShowMileageDialog = true;
            that.queryMileageStatus();
          } else if (resCode === "0002") {
            //不符合条件情况
            that.isShowDoing2 = false;
            that.$refs.toastV.show(
              data && data.data && data.data.ResDesc,
              2500
            );
          } else {
            //网络错误
            that.$refs.toastV.show("加载失败，请重试", 2500);
          }
        }
      });
    },
    /**
     * 跳转至升级里程商城
     * */
    goUpToMileageShop() {
      this.needReload = true;
      if (this.isTC) {
        this.openNewUrl(
          "https://appnew.ly.com/sign/app/view/main.html?wvc6=1&back=1#/exchange"
        );
      } else {
        this.openNewUrl(this.$linkUrl('https://appnew.ly.com/sign/app/view/main.html?wvc6=1&back=1#/exchange', { wakeRefid: refid }));
      }
      this.trackData(
        `^去升级为里程商城^${this.isTC ? "app" : "h5"}^`
      );
    },
    /**
     * 获取设备信息
     * */
    getDevice() {
      let that = this;
      bridgeFnc.getDeviceInfo(function (data) {
        var dbody = JSON.parse(data.CBData);
        if (dbody.memberInfo && dbody.memberInfo.memberId) {
          that.memberId = dbody.memberInfo.memberId;
        }
        if (dbody.deviceInfo && dbody.deviceInfo.deviceId) {
          that.deviceId = dbody.deviceInfo.deviceId;

          // APP是否是审核模式 since 10.0.1  "0":否 "1":是
          that.isAudit = (dbody.deviceInfo.isAudit == "1") ? true : false
        }
        _tc_bridge_map.app_location({
          param: {
            showType: "2",
            cacheType: "3"
          },
          callback: function (data1) {
            var dbody1 = JSON.parse(data1.CBData);
            if (
              dbody1.locationInfo &&
              dbody1.locationInfo.cityId &&
              dbody1.locationInfo.cityName &&
              dbody1.locationInfo.countryId == "1"
            ) {
              that.selectCity.cityId = dbody1.locationInfo.cityId;
              that.selectCity.cityName =
                dbody1.locationInfo.cityName;
              that.selectCity.lon = dbody1.locationInfo.lon;
              that.selectCity.lat = dbody1.locationInfo.lat;
              that.locationProvince =
                dbody1.locationInfo.provinceName;
              that.selectCity.province = that.locationProvince;
              that.hasLoacate = true;
            } else {
              that.selectCity.cityId = "321";
              that.selectCity.cityName = "上海";
              that.selectCity.lon = "121.47"; //经度
              that.selectCity.lat = "31.23"; //纬度
              that.locationProvince = "上海";
              that.selectCity.province = that.locationProvince;
            }
            that.getQueryIndexInfo();
            that.getQueryTabList();
            that.queryMileageStatus();
            that.getSceneryList();
            that.getTaskList();
          }
        });
      });
    },
    /**
     * 切换资源tap
     * */
    changeTap(type, isTop) {
      let that = this;
      that.resourceType = type;
      if (that.scenery.sceneryList.length == 0 && type == 4) {
        this.getSceneryList();
      }
      switch (type) {
        case 1:
          that.trackData(
            `^tab^${that.isTC ? "app" : "h5"}^酒店^`
          );
          break;
        case 2:
          that.trackData(
            `^tab^${that.isTC ? "app" : "h5"}^机票^`
          );
          break;
        case 3:
          that.trackData(
            `^tab^${that.isTC ? "app" : "h5"}^火车票^`
          );
          break;
        case 4:
          that.trackData(
            `^tab^${that.isTC ? "app" : "h5"}^景区^`
          );
          break;
        default:
          break;
      }
      if (isTop) {
        var top = $("#segmentView_inView").offset().top + 1;
        window.scrollTo(0, top);
      }
    },
    /**
     * 切换城市
     * */
    changeCity() {
      var that = this;
      if ((!that.sortCityList.domesticTag).length == 0) {
        that.getCityList();
      }
      if (!that.isTC) {
        if (that.cities.length == 0) {
          that.$refs.toastV.show("暂无其他城市资源", 2500);
        } else {
          that.isShowCity = true;
        }
        return;
      } else {
        _tc_bridge_map.select_city({
          param: {
            title: "选择城市",
            sName: that.selectCity.cityName,
            tabType: "left",
            cityConfig: [
              {
                subTitle: "国内",
                tips: "请输入城市名称(如北京,bj,Beijing)",
                allCitys: JSON.stringify({
                  cellType: "grid",
                  tagList: that.sortCityList.domesticTags
                })
              }
            ]
          },
          callback: function (data) {
            var res = JSON.parse(data.CBData);
            that.selectCity.cityName = res.cityInfo.cName;
            that.trackData(
              "^定位^" + that.isTC
                ? "app"
                : "h5" + "^" + that.selectCity.cityName + "^"
            );
            that.selectCity.cityId = res.cityInfo.cityId;
            that.selectCity.lon = "";
            that.selectCity.lat = "";
            // that.page = 1;
            // that.trackId = that.getTrackId();
            that.getQueryTabList(1);
          }
        });
      }
    },
    /*切换省份*/
    changeProvince() {
      let that = this;
      if (that.isTC) {
        let provinceData = [
          {
            title: "当前",
            longTitle: "当前 定位",
            cellType: "grid",
            cityList: [
              {
                cName: this.locationProvince,
                cPY: "",
                cPYS: "",
                countryId: "1",
                cityId: ""
              }
            ]
          },
          {
            title: "热门",
            longTitle: "热门",
            cellType: "grid",
            cityList: []
          }
        ];
        this.provinceList.map((pro, index) => {
          provinceData[1].cityList.push({
            cName: pro,
            cPY: "",
            cPYS: "",
            countryId: "1",
            cityId: ""
          });
        });
        _tc_bridge_map.select_city({
          param: {
            title: "选择省份",
            sName: this.selectCity.province,
            tabType: "left",
            cityConfig: [
              {
                subTitle: "国内",
                tips: "请输入省份名称",
                allCitys: JSON.stringify({
                  cellType: "grid",
                  tagList: provinceData
                })
              }
            ]
          },
          callback: function (data) {
            var res = JSON.parse(data.CBData);
            that.selectCity.province = res.cityInfo.cName;
            that.trackData(
              "^定位^" + that.isTC
                ? "app"
                : "h5" + "^" + that.selectCity.province + "^"
            );
            that.getSceneryList();
          }
        });
      } else {
        that.provinceDatas = [
          {
            cellType: "grid",
            tagList: [
              {
                title: "热门",
                longTitle: "热门",
                celType: "grid",
                cityList: []
              }
            ]
          }
        ];
        that.provinceList.map((pro, index) => {
          that.provinceDatas[0].tagList[0].cityList.push({
            cName: pro,
            cPY: "",
            cPYS: "",
            countryId: "1",
            extend: ""
          });
        });
        that.isShowProvince = true;
      }
    },
    /**
     * 手机验证
     * */
    phoneNumberCheck() {
      var mobile = this.mobilePhone;
      if (mobile.length < 11 || !/^1[1234567890]\d{9}$/.test(mobile)) {
        this.$refs.toastV.show("请输入有效手机号码", 2500);
        return;
      }
    },
    /**
     * 点击获取验证码
     * */
    sendMessageCode() {
      let that = this;
      var mobile = this.mobilePhone;
      if (that.timeCount != 60) return;
      if (mobile.length < 11 || !/^1[1234567890]\d{9}$/.test(mobile)) {
        this.$refs.toastV.show("请输入有效手机号码", 2500);
        return;
      } else {
        var reqBody = {
          mobile: mobile,
          jy_response: that.jy_response,
          jy_type: that.jy_type,
          jy_project_id: "tcwireless_net_activityplatform",
          activityTag: "appxz",
          bussinessType: "coupon"
        };
      }
      $.ajax({
        type: "post",
        dataType: "json",
        contentType: "application/json",
        url:
          baseUrl + "/activityservice/verification/sendverificationcodeforh5",
        data: JSON.stringify(reqBody),
        headers: { "Labrador-Token": "c2167576-9a81-4eb3-ad29-67c1fd724cf1" },
        success: function (data) {
          let resCode = data && data.statusCode,
            resDesc = data && data.message,
            body = data && data.data,
            timer;
          if (resCode === 0) {
            that.$refs.toastV.show(resDesc, 2500);

            that.isShowGetCode = false;
            timer = setInterval(function () {
              that.verifyStr = "剩" + --that.timeCount + "s重发";
              if (that.timeCount <= 0) {
                clearInterval(timer);
                that.timeCount = 60;
                that.isShowGetCode = true;
                that.verifyStr = "获取验证码";
              }
            }, 1000);
          } else {
            that.$refs.toastV.show("验证码发送失败", 2500);
          }
        },
        error: function (data) {
          that.$refs.toastV.show("验证码发送失败", 2500);
        }
      });
    },
    /**
     * 获取城市列表
     * */
    getCityList() {
      var that = this;
      commonFnc.getData(
        {
          url: cityService,
          params: JSON.stringify({
            cityVersion: 1
          }),
          cb: function (data) {
            let resCode = data && data.data && data.data.ResCode;
            if (resCode === "0000") {
              let body = data && data.data && data.data.Body;
              var sortCityList = {
                domesticTags: [],
                foreignTags: []
              };
              var citiesList = [];
              var userObj = {};
              var hotDomestics = [],
                hotcities = [];
              body.domesticCityList.map(function (item, index) {
                var obj = {};
                obj.cName = item.name;
                obj.cPY = item.namePY;
                obj.cPYS = item.initialMultiplePY;
                obj.countryId = item.countryId;
                if (that.isTC) {
                  obj.cityId = item.cityId;
                } else {
                  obj.extend = item.cityId;
                }
                if (
                  that.selectCity.cityName == item.name &&
                  that.hasLoacate
                ) {
                  userObj = obj;
                }
                if (item.isHot == "1") {
                  hotDomestics.push(obj);
                }
                var find = false;
                sortCityList.domesticTags.map(function (
                  tag,
                  index
                ) {
                  if (tag.title == item.initialSinglePY) {
                    find = true;
                    tag.cityList.push(obj);
                  }
                });
                if (!find) {
                  var tag = {};
                  tag.title = item.initialSinglePY;
                  tag.longTitle = item.initialSinglePY;
                  tag.cellType = "grid";
                  tag.cityList = [];
                  tag.cityList.push(obj);
                  sortCityList.domesticTags.push(tag);
                }
              });
              if (that.isTC) {
                sortCityList.domesticTags = that.insertSort(
                  sortCityList.domesticTags
                );
                sortCityList.domesticTags.unshift({
                  title: "热门",
                  longTitle: "热门",
                  cellType: "grid",
                  cityList: hotDomestics
                });
                if (userObj.cName && userObj.cName.length) {
                  sortCityList.domesticTags.unshift({
                    title: "当前",
                    longTitle: "当前 定位",
                    cellType: "grid",
                    cityList: [userObj]
                  });
                }
                that.sortCityList = sortCityList;
              } else {
                citiesList.unshift({
                  cellType: "line",
                  tagList: sortCityList.domesticTags
                });
                hotcities.unshift({
                  cellType: "grid",
                  tagList: [
                    {
                      title: "热门",
                      longTitle: "热门",
                      celType: "grid",
                      cityList: hotDomestics
                    }
                  ]
                });
                that.extendCities = hotcities;
                that.cities = citiesList;
              }
            } else {
              that.$refs.toastV.show(
                "获取城市失败，请稍后再试",
                1000
              );
            }
          }
        },
        "post"
      );
    },
    insertSort(arr) {
      var len = arr.length;
      for (var i = 1; i < len; i++) {
        var key = arr[i];
        var j = i - 1;
        while (j >= 0 && arr[j].title > key.title) {
          arr[j + 1] = arr[j];
          j--;
        }
        arr[j + 1] = key;
      }
      return arr;
    },
    showRule: function (show) {
      this.isShowRule = show;
      if (show) {
        $(".newvip").addClass("scrollstop");
        $('body').css({ position: 'fixed' })
        $(".newvip").css({ height: this.heightApp + "px" });
      } else {
        $(".newvip").removeClass("scrollstop");
        $('body').css({ position: 'static' })
        $(".newvip").css({ height: "auto" });
      }
    },

    /**
     * 显示
     * */
    isShowGotoTop() {
      let $newvip = $(".newvip"),
        $resourceTap = $("#segmentView_inView"),
        resourceTapTop = $resourceTap.offset().top,
        winTop = $newvip.offset().top,
        winHeight = $(window).height(),
        time = null;
      setInterval(() => {
        resourceTapTop = $resourceTap.offset().top;
      }, 50);
      $(window).scroll(() => {
        if (!time) {
          time = setTimeout(() => {
            let scrollTop = $(window).scrollTop();
            if (scrollTop > winHeight - 20) {
              $(".goto-top-btn").removeClass("hidden");
            } else {
              $(".goto-top-btn").addClass("hidden");
            }
            if (scrollTop > resourceTapTop) {
              $(".resource-tap").removeClass("resource-hidden");
            } else {
              $(".resource-tap").addClass("resource-hidden");
            }
            time = null;
          }, 20);
        }
      });
    },
    /**
     * 超过一屏出现回到顶部按钮
     * 一键置顶
     * */
    gotoTop() {
      // window.scrollTo({
      //     left:0,
      //     top:0,
      //     behavior:"smooth",
      // });
      this.trackData(
        `^回到顶部^${this.isTC ? "app" : "h5"}^${this.memberId != "" ? "Y" : "N"
        }^`
      );
      window.scrollTo(0, 0);
    },
    clickChallenge(item) {
      let that = this;
      if (that.isTC) {
        if (that.memberId) {
          that.openNewUrl(item.linkURL);
        } else {
          _tc_bridge_user.user_login({
            param: {},
            callback: function (data) {
              let dbody = JSON.parse(data.CBData);
              if (dbody.memberInfo && dbody.memberInfo.memberId) {
                that.memberId = dbody.memberInfo.memberId;
                Promise.all([that.getQueryIndexInfo(), that.getTaskList()]).then(() => {
                  if (that.isNewMember == '0') {
                    _tc_bridge_util.show_tips_dialog({
                      param: {
                        desc:
                          "您已经是尊贵的老用户啦，更多超值会员任务等你领",
                        btnList: [
                          {
                            showText: "放弃福利",
                            tagname: "tag_click_cancel_btn"
                          },
                          {
                            showText: "去看看",
                            tagname: "tag_click_sure_btn"
                          }
                        ]
                      },
                      callback: function (data) {
                        data = ({}).toString.call(data) === '[object Object]' ? data : JSON.parse(data);
                        if (data && data.tagname === 'tag_click_sure_btn') {
                          that.openNewUrl("tctclient://web/hy?id=7&route=main.html%3Fwvc1%3D1%26from%3DmyLeft%26come%3Dmy%23%2Fvipcenter");
                          that.memberTrack("app非新客跳转红包中心");
                        }
                      }
                    });
                  }
                })
              } else {
                that.memberId = "";
              }
            }
          });
        }
      } else {
        that.openNewUrl(that.$linkUrl(item.linkURL, { wakeRefid: refid }));
      }
      let btn = "";
      switch (item.type) {
        case 1:
          btn = "已完成";
          break;
        case 2:
          btn = "已领完";
          break;
        case 3:
          btn = "去领取";
          break;
        case 4:
          btn = "去完成";
          break;
      }
      that.trackData(
        "^挑战任务^" +
        (that.isTC ? "app" : "h5") +
        "^" +
        (that.memberId != "" ? "Y" : "N") +
        "^" +
        item.maintitle +
        "^" +
        btn +
        "^" +
        (refid || "") +
        "^"
      );
    },
    hotelFilterTagClicked(tagItem) {
      this.hotel.hotelFilterInfo = tagItem;

      this.getHotelList();
    },
    clickHotelItemDetail(item) {
      this.openNewUrl(item.redirectUrl);
      this.trackData(
        `^资源^${this.isTC ? "app" : "h5"}^酒店^${item.title}^`
      );
    },
    trainWayItemClicked(item) {
      this.openNewUrl(this.isTC ? item.jumpUrl : item.wxUrl);
      this.trackData(
        `^资源^${this.isTC ? "app" : "h5"}^火车票^${item.title}^`
      );
    },
    trainScenicItemClicked(i, item) {
      this.openNewUrl(this.isTC ? i.appUrl : i.wxUrl);
    },
    airItemClicked(item) {
      this.openNewUrl(this.isTC ? item.jumpUrl : item.wxUrl);
      this.trackData(
        `^资源^${this.isTC ? "app" : "h5"}^机票^${item.title}^`
      );
    },
    airHotIndexChanged(index) {
      this.selectItem = index;
    },
    airHotSourceClicked(item) {
      this.openNewUrl(this.isTC ? item.jumpUrl : item.wxUrl);
      this.trackData(
        `^资源^${this.isTC ? "app" : "h5"}^热门目的地^${item.dcn}^`
      );
    },
    clickSceneryDetail(item) {
      if (this.isTC) {
        this.openNewUrl(item.JumpUrl);
      } else {
        this.openNewUrl(item.WxUrl);
      }
    },
    clickPriorityDetail(item) {
      let arr = window.location.href.split("#");
      if (item) {
        this.openNewUrl(
          arr[0] +
          "#/newvipDetail?project=" +
          item.project +
          "&title=" +
          encodeURIComponent(item.title)
        );
        this.trackData(
          "^权益^" +
          (this.isTC ? "app" : "h5") +
          "^" +
          (this.memberId != "" ? "Y" : "N") +
          "^" +
          item.project +
          "^" +
          item.title +
          "^" +
          (refid || "") +
          "^"
        );
      } else {
        this.openNewUrl(arr[0] + "#/newvipDetail?");
        this.trackData(
          "^权益^" +
          (this.isTC ? "app" : "h5") +
          "^" +
          (this.memberId != "" ? "Y" : "N") +
          "^更多^更多^" +
          (refid || "") +
          "^"
        );
      }
    },
    /**
     * 打开新链接
     * */
    openNewUrl: function (url) {
      if (
        url.indexOf("shouji") != -1 ||
        url.indexOf("tctclient") != -1 ||
        url.indexOf("tcwvcnew") != -1
      ) {
        window.location.href = url;
      } else {
        var jsonObj = {
          param: {
            tagname: "tagback",
            openParams: "newWindow,hideBottom", //打开新webview
            jumpUrl: url
          }
        };
        setTimeout(function () {
          window._tc_bridge_web.open_newurl(jsonObj);
        }, 0);
      }
    },
    configTrackInfo() {
      var that = this;
      var new_element = document.createElement("script");
      new_element.setAttribute("type", "text/javascript");
      new_element.setAttribute("src", "//vstlog.17usoft.com/vst.ashx");
      document.body.appendChild(new_element);
      new_element.onload = function () {
        that.track();
      };
    },
    /**统计流量 */
    track() {
      let self = this,
        refid =
          commonFnc.getHashString("refid") ||
          commonFnc.getQueryString("refid") ||
          "",
        pageName = "微信转移承接H5发红包页面",
        _tcq = _tcq || [],
        _timediff = -1;
      if (typeof _tcopentime != "undefined") {
        _timediff = new Date().getTime() - _tcopentime;
      }
      _tcq.push(["_serialid", ""]); //如果是下单页面，需要传入订单号，多个订单号用下划分割 "_"
      _tcq.push(["_vrcode", "10007-2000-0"]); //产品号见下面解释，最后一位默认为0，写成其他的统计不到，此条代码最重要
      _tcq.push(["_refId", refid]); //Refid需要传入来源refid，不同平台的读取方法不同，项目自己读取Refid
      _tcq.push(["_userId", this.memberId || this.mobilePhone || ""]); //传入访问者中登录的会员ID，未登录的为0，不同平台的读取方法不同，项目自己读取会员ID
      _tcq.push(["_openTime", _timediff]);
      _tcq.push(["_trackPageview", pageName]); //虚拟url，项目自己定义,如:/Touch站/首页，只针对微信，在此项原基础上修改为：_tcq.push(['_trackPageview', ' openid ||xxx ']),即在pageview所传值的前面加“openid||”（即openid+双竖线）
      _tcq.push(["_resId", ""]); //新增项：资源id（只针对详情页\交通类项目的订单填写页  需要添加该项）----有疑问可联系@支夏萍
      _tcq.push(["_qdid", ""]); //新增项：市场渠道id（用于区分市场中心各个部门）----有疑问可联系@支夏萍
      _tcq.push(["_openid", ""]);
    },
    /**
     * 设置埋点
     * */
    trackData(val) {
      if (this.isTC) {
        bridgeFnc.trackData("a_25541", val);
      }
      var that = this;
      var value =
        (that.isTC ? "app^" : "wx^") +
        (that.memberId || that.mobilePhone || "") +
        "^" +
        that.deviceId;
      _tcq.map(function (item, index) {
        if (item[0] == "_refId") {
          item[1] = refid;
        }
        if (item[0] == "_trackPageview") {
          item[1] = "h5_newvip";
        }
        if (item[0] == "_openid") {
          item[1] = that.getParams("openId");
        }
        if (item[0] == "_vrcode") {
          if (that.isTC) {
            item[1] = "10007-2000-0";
          } else {
            item[1] = "10005-2000-0";
          }
        }
      });

      window._tcTraObj._tcTrackEvent(
        "h5_newvip",
        "click",
        "a_25541",
        value + val
      );
    },
    getParams(key) {
      var value =
        commonFnc.getQueryString(key) ||
        commonFnc.getHashString(key) ||
        "";
      return value;
    },
    /**
     * 统计轨迹
     * */
    memberTrack(info) {
      bridgeFnc.trackInfo(info, {
        project: "h5",
        pageName: "newvip",
        platform: "App"
      });
    },
    getTrackId() {
      var guid = "";
      for (var i = 1; i <= 32; i++) {
        var n = Math.floor(Math.random() * 16.0).toString(16);
        guid += n;
        if (i == 8 || i == 12 || i == 16 || i == 20) guid += "-";
      }
      return guid;
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../css/newvip/newvip.css";
@import "../../css/newvip/newvip.scss";
@import "../../css/newvip/april.scss";
</style>
<style scoped>
@font-face {
  font-family: iconfont;
  src: url("https://file.40017.cn/css40017cnproduct/touch/pushcode/nail/travel/iconfont.otf");
}
.newvip .app-received .title {
  font-family: iconfont;
}
.newvip .app-received .title .num {
  font-family: iconfont;
}
</style>
