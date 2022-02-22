<template>
<div>
  <q-card class="col-12 shadow-0">
    <!--                  返回按钮-->
    <q-card-actions>
      <q-btn
        @click="this.$router.push({ name: 'articleList' })"
        style="font-size: 14px;font-weight: 400;color: #999999"
        unelevated
        :label="goblack"/>
    </q-card-actions>

    <q-separator inset/>

    <q-card-section horizontal>
      <!--        头像及作者-->
      <q-card-section class="q-pa-md">
        <q-avatar
          size="30px"
        >
          <img
            :src=avatar_img
          />
        </q-avatar>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center myAuthor">
          <span class="author">
            {{ author }}
          </span>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center art_time">
          <span v-if="is_uptime === true">
            {{ $t('community.push_time') }}
          </span>
        <span v-if="is_uptime === false">
            {{ $t('community.revise_time') }}
          </span>
        <span>
            {{ time }}
          </span>
      </q-card-section>
    </q-card-section>
    <!--      文章标题-->
    <q-card-section style="padding-top: 0;padding-bottom: 0">
      <div class="tit">
        {{ title }}
      </div>
    </q-card-section>
    <!--        文章集体内容-->
    <q-card-section style="padding-top: 10px!important;">
      <div v-html="content" class="art_msg">
      </div>
    </q-card-section>
    <!--       图片-->
    <q-card-section v-if="imgs">
      {{ imgs }}
    </q-card-section>
    <q-separator inset/>
    <q-card-section>
      {{comment_count}} {{ $t('community.replies') }}
    </q-card-section>
    <q-separator inset/>
  </q-card>
<!--    评论表-->
    <q-card v-for="item in comment" class="shadow-0">
    <q-card-section horizontal>
      <q-card-section>
        <q-avatar size="30px">
          <img :src=item.user__icon alt="">
        </q-avatar>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center mycontenter">
          <span class="contenter">
            {{ item.user__nickname }}
          </span>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center art_time">
        <span>
            {{ item.create_time}}
          </span>
      </q-card-section>
    </q-card-section>
    <q-card-section style="padding-left:62px;padding-top: 0">
      {{item.content}}
    </q-card-section>
<!--      二级评论-->
      <div class="sen_cun" v-if="item.child" v-for="(sen_item,ind) in item.child" :key="ind">
        <q-avatar
          size="30px"
        >
          <img
            :src=sen_item.user__icon
          />
        </q-avatar>

        <span class="q-pa-md fir_reply_author">
            {{ sen_item.user__nickname }}
          </span>
        <span class="art_time">
            {{ sen_item.create_time }}
          </span>
        <div v-html="sen_item.content" style="margin-left: 55px">
        </div>
      </div>
      <q-separator inset/>
  </q-card>
  <q-card-section style="padding: 30px">

  </q-card-section>
</div>
</template>

<script>
import jwtDecode from "jwt-decode";
import {get} from "boot/axios";
import {createMetaMixin} from "quasar";

export default {
  name: "articleDetail",
  data() {
    return {
      goblack: this.$t('community.black'),
      title: '',
      avatar_img: '',
      author: '',
      time: '',
      content: '',
      imgs: '',
      userid: '',
      is_uptime: true,
      comment_count: '0',
      comment: []
    }
  },
  computed: {
    articleId() {
      return this.$store.state.bbsChange.articleId;
    }
  },
  methods: {
    getavayarinfo() {
      var _this = this;
      let userinfoStr = jwtDecode(_this.$q.cookies.get("token"));
      _this.avatar_now = userinfoStr.icon;
    },
    // 获取文章详情
    getdetailedinfo() {
      var _this = this
      get('article/api/v1/Browse/' +_this.$q.cookies.get('articleId') + '/' + '?community_type=0').then(res => {
        var res_msg = res.result
        _this.title = res_msg.title
        _this.head_title = res_msg.title
        _this.author = res_msg.author_icon.author
        _this.content = res_msg.content
        _this.imgs = res_msg.cover
        _this.comment_count = res_msg.comment_count
        _this.avatar_img = res_msg.author_icon.icon
        _this.comment = res_msg.comment
        _this.userid = res_msg.author_icon.id
        if (res_msg.changed_time === res_msg.create_time) {
          _this.time = res_msg.updata_time
          _this.is_uptime = true
        } else {
          _this.time = res_msg.create_time
          _this.is_uptime = false
        }
        _this.meta = {
          description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
          keywords: {name: 'keywords', content: res_msg.content },
          equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
          ogTitle: {
            property: 'og:title',
            template(ogTitle) {
              return `${ogTitle} - GreaterWMS`
            }
          }
        }
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.head_title,
        meta: this.meta,
      };
    }),
  ],
  created() {
    var _this = this
    if (_this.$q.cookies.get('lang') === 'zh-hans') {
      _this.head_title = 'GreaterWMS - 开源社区'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {name: 'keywords', content: '聚商汇WMS,开源仓库管理系统,仓库管理系统,wms,仓库管理软件,仓库管理,GreaterWMS, greaterwms'},
        equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
        ogTitle: {
          property: 'og:title',
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`
          }
        }
      }
    } else {
      _this.head_title = 'GreaterWMS - Community'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {
          name: 'keywords',
          content: 'GreaterWMS - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms'
        },
        equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
        ogTitle: {
          property: 'og:title',
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`
          }
        }
      }
    }
  },
  mounted() {
    this.getdetailedinfo()
  }
}
</script>

<style lang="scss" scoped>
.sen_cun {
  margin-left: 48px;
  padding-bottom: 10px;
}
.author {
  font-size: 12px;
  color: #333333;
  font-weight: 400;
}
.myAuthor {
  padding-left: 0;
}
.art_time{
  font-size: 12px;
  font-weight: 400;
  color: #999999;
}
.tit {
  font-size: 15px;
  color: #333333;
  font-weight: 500;
}
.mycontenter {
  padding-left: 0;
  padding-right: 0;
}
.contenter {
  font-size: 15px;
  font-weight: 500;
  color: #333333;
}
.fir_reply_author {
  font-size: 14px;
  font-weight: 400;
  color: #666666;
}
</style>
