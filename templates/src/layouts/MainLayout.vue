<template>
    <router-view />
</template>
<script>
import { defineComponent } from 'vue'
import { getauth, post } from "boot/axios";

export default defineComponent({
  name: 'MainLayout',
  methods: {
    getAreaCheck () {
      var _this = this
        getauth('area_v2/check/').then(res =>{
          _this.$q.cookies.set('area', res.area)
        })
    },
    verifyToken () {
      var _this = this
      if (_this.$q.cookies.has('token')) {
        console.log(_this.$q.cookies.get('token'))
        var msg = {
          token: _this.$q.cookies.get('token')
        }
        post('token/verify/', msg).then(res =>{
          if (res.detail) {
            _this.$q.cookies.remove('token')
          }
        })
      }
      if (_this.$q.cookies.has('area')) {} else {
        _this.getAreaCheck()
      }
    }
  },
  mounted() {
    var _this = this
    _this.verifyToken()
  },
})
</script>
