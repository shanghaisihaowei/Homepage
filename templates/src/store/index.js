import { store } from 'quasar/wrappers'
import { createStore } from 'vuex'

import tabchange from './tabchange'
import bbsChange from './bbsChange'
import pagelocation from './pagelocation'
import getmore from './getmoreart'

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store(function (/* { ssrContext } */) {
  const Store = createStore({
    modules: {
      tabchange,
      bbsChange,
      pagelocation,
      getmore
    },

    // enable strict mode (adds overhead!)
    // for dev mode and --debug builds only
    strict: process.env.DEBUGGING
  })

  return Store
})
