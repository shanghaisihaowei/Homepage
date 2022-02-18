<template>
  <div class="markdown">
    <q-timeline color="grey-5" layout="comfortable">
      <q-timeline-entry
        class="text-body1 my-font-D timeline_subtitle"
        :title="item.version + '-' + item.version_type"
        :subtitle="item.updata_time"
        v-for="item in timeline"
        :key="item.version"
      >
        <div class="my-font q-mr-md" v-html="item.plugin_instructions"></div>
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