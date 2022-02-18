<template>
  <div class="row my-font">
    <q-card class="col-12 column q-pa-md" style="height: 770px">
      <q-card-section class="col-7 column" style="border-bottom:1px #E6E6E6 solid ">
        <div class="col-1 text-h6 my-font">{{ $t('community.per_info') }}</div>
        <div class="col-1"></div>
        <!--                      头像-->
        <div class="col-4 row">
          <div class="col-2"></div>
          <q-avatar style="cursor: pointer" size="120px" @click="click_avatar()">
            <q-img
              width="120px" height="120px"
              :src="icon"/>
          </q-avatar>
          <input
            @change="search"
            v-show="false"
            ref="fileRef"
            type="file"
          />
        </div>
        <!--                      昵称-->
        <div class="col-1 row">
          <div v-show="lange === 'zh-hans'" class="col-1"></div>
          <div v-if="lange === 'zh-hans'" class="col-1 flex flex-center">
            <span style="letter-spacing: 10px;">{{ $t('community.nick') }}</span>
          </div>
          <div v-if="lange !== 'zh-hans'" class="col-2 flex flex-center">
            <span>{{ $t('community.nick') }}</span>
          </div>
          <input
            @input="length_name = personal_center.nickname.length"
            v-model="personal_center.nickname"
            class="col-3 per_input"
            maxlength="16"
            @focus="show_name_len()"
            @blur="show_ln = false"
          />
          <span class="q-pa-sm content_font" v-show="show_ln === true">
            {{ length_name }}/16
          </span>
        </div>

        <div class="col-1"></div>
        <!--                      个人介绍-->
        <div class="col-1 row">
          <div v-show="lange === 'zh-hans'" class="col-1"></div>
          <div v-if="lange === 'zh-hans'" class="col-1 flex flex-center">
            <span style="letter-spacing: 10px;">
              {{ $t('community.self_intro') }}
            </span>
          </div>
          <div v-if="lange !== 'zh-hans'" class="col-2 flex flex-center">{{ $t('community.self_intro') }}</div>
          <input
            @input="length_intro = personal_center.intro.length"
            v-model="personal_center.intro"
            class="col-6 per_input"
            maxlength="100"
            @focus="show_intro_len()"
            @blur="show_li = false"
          />
          <span class="q-pa-sm content_font" v-show="show_li === true">
            {{ length_intro }}/100
          </span>
        </div>

        <div class="col-1"></div>
        <!--                      保存-->
        <div class="col-1 row">
          <div class="col-2"></div>
          <q-btn unelevated style="width: 100px;height: 34px;background: #116FEC;color: white" @click="modifyPreinfo()">
            {{ $t('index.save') }}
          </q-btn>
        </div>
      </q-card-section>

      <q-card-section class="col-5 column">
        <div class="col-1 text-h6 my-font">{{ $t('community.act_psd') }}</div>
        <div class="col-2"></div>
        <!--                      邮箱-->
        <div class="col-2 row">
          <div class="col-1"></div>
          <div class="col-1">{{ $t('community.emails') }}</div>
          <input v-model="personal_center.email" readonly="readonly" class="col-3 per_input"
                 style="height:34px;background:#f1f1f1;"/>
        </div>
        <div class="col-1"></div>
        <!--                      密码-->
        <div class="col-2 row">
          <div class="col-1"></div>
          <div class="col-1">{{ $t('community.passwords') }}</div>
          <input placeholder="********" readonly="readonly" type="password" class="col-3 per_input"
                 style="height:34px"/>
        </div>
        <div class="col-1"></div>
        <div class="col-2 row">
          <div class="col-2"></div>
          <!--                        修改密码按钮-->
          <q-btn
            unelevated
            :class="{'change_psdbtn':this.$q.cookies.get('lang') === 'zh-hans','change_psdbtn_e':this.$q.cookies.get('lang') !== 'zh-hans'}"
            @click="psd_changedia = true"
          >
            {{ $t('community.change_psd') }}
          </q-btn>
        </div>
      </q-card-section>
    </q-card>
  </div>
  <q-dialog v-model="psd_changedia">
    <q-card class="psd_changedia">
      <!--      头部-->
      <q-card-section style="border-bottom: 1px #E4E4E4 solid">
        <span class="change_tip">
          {{ $t('community.change_psd') }}
        </span>
        <!--        关闭按钮-->
        <q-btn
          unelevated
          icon="close"
          style="width: 16px;height: 16px;float: right"
          @click="psd_changedia = false"
        />
      </q-card-section>
      <!--      输入框-->
      <q-card-section>
        <!--        请输入您收到的验证码-->
        <div class="verify_tit">
          {{ $t('community.receive_code') }}
        </div>
        <div class="row">
          <div class="col-8">
            <q-input
              class="verify_inp"
              dense
              v-model="ver_code"
              outlined
              :rules="[val => val.length === 6 || v_code]"
              @keyup="getSubBtn()"
            />
          </div>
          <div class="col-4">
            <q-btn
              v-if="isverify === false"
              :class="{'send_verBtn':this.$q.cookies.get('lang') === 'zh-hans','send_verBtn_e':this.$q.cookies.get('lang') !== 'zh-hans',}"
              flat
              :label=svc
              @click.once="getcpsd_ver()"
            />
            <q-btn
              v-if="isverify === true"
              :class="{'send_verBtn2':this.$q.cookies.get('lang') === 'zh-hans','send_verBtn2_e':this.$q.cookies.get('lang') !== 'zh-hans',}"
              flat
              :label=effective_time
            />
          </div>
          <div v-show="isverify === true" class="verify_msg">
            {{ $t('community.sended_email') }}
          </div>
        </div>
        <!--        输入新密码-->
        <div class="nwePsd_tit">
          {{ $t('community.newpsd') }}
        </div>
        <q-input
          οnpaste="return false"
          type="password"
          dense
          v-model="new_psd"
          outlined
          style="margin-top: 10px"
          :rules="[val => val.length >= 8 || less_eight]"
          @keyup="getSubBtn()"
        />
        <!--        再次输入新密码-->
        <div class="nwePsd_tit">
          {{ $t('community.agenpsd') }}
        </div>
        <q-input
          onpaste="return false"
          type="password"
          dense
          v-model="confirm_psd"
          outlined
          style="margin-top: 10px"
          :rules="[val => val === new_psd || psd_dif]"
          @keyup="getSubBtn()"
        />
        <!--        提交按钮-->
        <q-btn
          v-if="isBtnok === true"
          flat
          class="push_btn"
          :label=submit
          @click="change_subPsd()"
        />
        <q-btn
          v-if="isBtnok === false"
          flat
          class="push_btn_less"
          :label=submit
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import {getauth, putauth, postauth} from 'boot/axios';
import jwtDecode from "jwt-decode";

export default defineComponent({
  data() {
    return {
      submit: this.$t('index.submit'),
      svc: this.$t('community.send_verify_code'),
      effective_time: this.$t('index.efficient'),
      psd_dif: this.$t('community.inconsistent'),
      less_eight: this.$t('community.less_eight'),
      v_code: this.$t('community.v_code'),
      isverify: false,
      confirm_psd: '',
      ver_code: '',
      new_psd: '',
      psd_changedia: false,
      inputa_avatar: '',
      icons: '',
      isBtnok: false,
      lange: this.$q.cookies.get('lang'),
      length_name: '',
      length_intro: '',
      show_ln: false,
      show_li: false,
      icon: '',
      token: '',
      userinfoStr: ''
    }
  },
  computed: {
    personal_center() {
      return JSON.parse(JSON.stringify(this.$store.state.bbsChange.user_info));
    }
  },
  methods: {
    // 修改个人信息的昵称、个人简介
    modifyPreinfo() {
      var _this = this;
      var msg = new FormData();
      msg.append('nickname', _this.personal_center.nickname)
      msg.append('intro', _this.personal_center.intro)
      msg.append('icon', _this.icons)
      if (_this.$q.cookies.has("token")) {
        putauth('/user/api/v1/userdetail/' + _this.token.user_id + '/', msg)
          .then(res => {
              _this.$q.cookies.set('token',res.result.access)
              _this.userinfoStr = jwtDecode( _this.$q.cookies.get('token'))
              _this.icon = _this.userinfoStr.icon
              _this.personal_center.nickname = _this.userinfoStr.nickname;
              _this.personal_center.intro = _this.userinfoStr.intro;
              let user_info = {
                id: _this.userinfoStr.user_id,
                nickname: _this.userinfoStr.nickname,
                intro: _this.userinfoStr.intro,
                icon:_this.userinfoStr.icon,
                email: _this.userinfoStr.email,
                username: _this.userinfoStr.username
              };
              _this.$store.dispatch('bbsChange/userInfoChange', user_info);
              _this.$q.notify({
                message: _this.$t('community.change_suc'),
                icon: 'check',
                color: 'green'
              })
              location.reload()
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            });
          });
      }
    },
    // 点击修改头像
    click_avatar() {
      var _this = this
      _this.$refs.fileRef.dispatchEvent(new MouseEvent('click'))
    },
    // 拿到修改头像的本地文件
    search(e) {
      var _this = this
      _this.icons = e.target.files[0]
      var reader = new FileReader();
      reader.onload = function (e) {
        // console.log( reader.result);  //或者 e.target.result都是一样的，都是base64码
        _this.icon = reader.result
      }
      _this.$q.notify({
        message: _this.$t('community.confirm_avatar'),
        icon: 'check',
        color: 'green'
      })
      reader.readAsDataURL(e.target.files[0])
    },
    // 获取修改密码的验证码
    getcpsd_ver() {
      var _this = this
      getauth('/user/api/v1/pwd_codes/' + '?email=' + _this.$store.state.bbsChange.user_info.email).then(res => {
        _this.$q.notify({
          message: '验证码发送成功',
          icon: 'check',
          color: 'green'
        })
        _this.isverify = true
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    // 修改密码
    change_subPsd() {
      var _this = this
      var msg = {}
      msg['email'] = _this.$store.state.bbsChange.user_info.email
      msg['code'] = _this.ver_code
      msg['password'] = _this.new_psd
      msg['re_password'] = _this.confirm_psd
      postauth('/user/api/v1/putpwd/', msg).then(res => {
        if (res.code === 200) {
          _this.$q.notify({
            message: _this.$t('community.edit_suc_relogin'),
            icon: 'check',
            color: 'green'
          })
          _this.logout_sub()
        }
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    // 登出
    logout_sub() {
      var _this = this;
      _this.$q.cookies.remove("token");
      _this.$store.dispatch("bbsChange/loginChange", false);
      _this.isIndexMenu = true;
      let user_info = {
        id: '',
        icon: '',
        nickname: '',
        intro: '',
        email: '',
      };
      _this.$store.dispatch("bbsChange/userInfoChange", user_info);
      _this.$router.push({
        path: "/community/GreaterWMS",
      });
    },
    //判断提交按钮变色
    getSubBtn() {
      var _this = this
      if (_this.ver_code.length === 6 &&
        _this.new_psd.length >= 8 &&
        _this.confirm_psd.length >= 8
      ) {
        _this.isBtnok = true
      } else {
        _this.isBtnok = false
      }
    },
    //当修改昵称获得焦点显示长度
    show_name_len() {
      var _this = this
      _this.show_ln = true
      _this.length_name = _this.personal_center.nickname.length
    },
    //当修改签名获得焦点显示长度
    show_intro_len() {
      var _this = this
      _this.show_li = true
      _this.length_intro = _this.personal_center.intro.length
    }
  },
  mounted() {
    if (this.$q.cookies.has('token')) {
      this.token = jwtDecode(this.$q.cookies.get("token"));
      this.icon = window.g.BaseUrl + this.token.icon
    } else {
    }
    this.$store.dispatch('bbsChange/isIndexMenu', false)
    this.$store.dispatch('bbsChange/link', 'changePsd')
  }
})
</script>

<style scoped lang="sass">
.change_psdbtn
  width: 100px
  height: 34px
  background: #116FEC
  color: white
.change_psdbtn_e
  width: 100px
  height: 50px
  background: #116FEC
  color: white
.content_font
  font-size: 14px
  color: #999999

.push_btn
  color: white
  width: 100%
  height: 40px
  background: #116FEC
  border-radius: 4px
  margin-top: 20px

.push_btn_less
  width: 100%
  height: 40px
  background: #e6e6e6
  border-radius: 4px
  margin-top: 20px

.nwePsd_tit
  font-size: 16px
  font-weight: 400
  color: #666666
  margin-top: 20px

.send_verBtn
  font-size: 14px
  font-weight: 400
  color: white
  width: 120px
  height: 40px
  background: #116fec
  border-radius: 4px
  margin-top: 9px
.send_verBtn_e
  font-size: 14px
  font-weight: 400
  color: white
  width: 120px
  height: 60px
  background: #116fec
  border-radius: 4px
  margin-top: 9px

.send_verBtn2
  font-size: 14px
  font-weight: 400
  color: #999999
  width: 120px
  height: 40px
  background: #E6E6E6
  border-radius: 4px
  margin-top: 9px
.send_verBtn2_e
  font-size: 14px
  font-weight: 400
  color: #999999
  width: 120px
  height: 80px
  background: #E6E6E6
  border-radius: 4px
  margin-top: 9px

.verify_msg
  margin-top: 12px
  font-size: 14px
  font-weight: 400
  color: #d82e2e

.verify_inp
  width: 304px
  margin-top: 10px

.verify_tit
  font-size: 16px
  font-weight: 400
  color: #666666

.change_tip
  margin-top: 8px
  font-size: 20px
  font-weight: 400
  color: #333333

.psd_changedia
  width: 500px
  height: 530px
  background: #ffffff
  border-radius: 4px

.per_input
  border: 1px solid #e6e6e6
  border-radius: 4px
  outline-color: #5b86e5
</style>
