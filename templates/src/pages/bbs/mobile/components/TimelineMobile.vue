<template>
  <div class="markdown">
    <q-timeline color="grey-5" layout="comfortable">
      <q-timeline-entry
        class="text-body1 timeline_subtitle_mobile"
        :title="item.version + '-' + item.version_type"
        :subtitle="item.updata_time"
        v-for="item in timeline"
        :key="item.version"
      >
        <div style="font-size: 14px" class="q-mr-md" v-html="item.plugin_instructions"></div>
      </q-timeline-entry>
    </q-timeline>
  </div>
</template>
<script>
export default {
  props: {
    timeline: "",
  },
};
</script>
