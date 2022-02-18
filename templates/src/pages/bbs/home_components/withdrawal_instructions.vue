<template>
  <div class="row">
    <q-card class="col-12">
      <q-card-actions>
        <q-btn
          @click="this.$router.push( '/community/myWallet')"
          style="font-size: 14px;font-weight: 400;color: #999999"
          unelevated
          :label="goblack"/>
      </q-card-actions>
      <div>
        <img v-if="this.$q.cookies.get('lang') === 'zh-hans'" src="statics/community/withdrawal_instructions.svg">
        <img v-if="this.$q.cookies.get('lang') !== 'zh-hans'" src="statics/community/withdrawal_instructions_e.svg">
      </div>
    </q-card>
  </div>
</template>

<script>
import {defineComponent} from "vue";

export default defineComponent({
  name: "withdrawal_instructions",
  data() {
    return {
      goblack: this.$t('community.black'),
    }
  }
})
</script>

<style scoped>

</style>
