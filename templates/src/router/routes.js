const routes = [{
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{
        path: '',
        name: 'index',
        component: () => import('pages/Index.vue'),
        children: [{
            path: 'Homepage',
            name: 'Homepage',
            component: () => import('pages/home/hp.vue'),
        },
        {
            path: 'contact_us',
            name: 'contact_us',
            component: () => import('pages/home/contact_us.vue'),
        },
        {
            path: 'release_notes',
            name: 'release_notes',
            component: () => import('pages/home/release_notes.vue'),
        },
        {
            path: '/phone',
            name: 'phone',
            component: () => import('pages/mobile/phone_homepage.vue'),
        },
        {
            path: '/phone_contact_us',
            name: 'phone_contact_us',
            component: () => import('pages/mobile/contact_us.vue'),
        },
        {
            path: '/phone_release_notes',
            name: 'phone_release_notes',
            component: () => import('pages/mobile/release_notes.vue'),
        }
        ]
    },
    {
        path: '/community',
        name: 'community',
        redirect: '/community/GreaterWMS',
        component: () => import('pages/bbs/home.vue'),
        children: [{
            path: 'GreaterWMS',
            name: 'GreaterWMS',
            component: () => import('pages/bbs/home_components/articleList.vue'),
        },
        {
            path: 'GreaterWMSDetail/:id',
            name: 'GreaterWMSDetail',
            component: () => import('pages/bbs/home_components/articleDetail.vue')
        },
        {
            path: 'DVadmin',
            name: 'DVadmin',
            component: () => import('pages/bbs/home_components/articleListDV.vue'),
        },
        {
            path: 'DVadminDetail/:id',
            name: 'DVadminDetail',
            component: () => import('pages/bbs/home_components/articleDetailDV.vue')
        },
        {
            path: 'personalHomepage',
            name: 'personalHomepage',
            component: () => import('pages/bbs/home_components/personalHomepage.vue')
        },
        {
            path: 'myReleasedPlugins',
            name: 'myReleasedPlugins',
            component: () => import('pages/bbs/home_components/myReleasedPlugins.vue')
        },
        {
            path: 'myOrders',
            name: 'myOrders',
            component: () => import('pages/bbs/home_components/myOrders.vue')
        },
        {
            path: 'orderDetail/:id',
            name: 'orderDetail',
            component: () => import('pages/bbs/home_components/orderDetail.vue')
        },
        {
            path: 'myWallet',
            name: 'myWallet',
            component: () => import('pages/bbs/home_components/myWallet.vue')
        },
          {
            path: 'withdrawal_instructions',
            name: 'withdrawal_instructions',
            component: () => import('pages/bbs/home_components/withdrawal_instructions.vue')
          },
        {
            path: 'withdraw',
            name: 'withdraw',
            component: () => import('pages/bbs/home_components/withdraw.vue')
        },
          {
            path: 'withdraw_foreign',
            name: 'withdraw_foreign',
            component: () => import('pages/bbs/home_components/withdraw_foreign.vue')
          },
        {
            path: 'tos',
            name: 'tos',
            component: () => import('pages/bbs/home_components/termsofservice.vue')
        },
        {
            path: 'pa',
            name: 'pa',
            component: () => import('pages/bbs/home_components/privacyagreement.vue')
        },
        {
            path: 'changePsd',
            name: 'changePsd',
            component: () => import('pages/bbs/home_components/changePsd.vue')
        },
        {
            path: 'release',
            name: 'release',
            component: () => import('pages/bbs/home_components/release.vue')
        },
        {
            path: 'authentication',
            name: 'authentication',
            component: () => import('pages/bbs/home_components/authentication.vue')
        },
        {
            path: 'myAccount',
            name: 'myAccount',
            component: () => import('pages/bbs/home_components/myAccount.vue')
        },
        {
            path: '/market/plugins/:belong',
            name: 'plugins',
            component: () => import('pages/bbs/home_components/market/plugins.vue')
        },
        {
            path: '/market/pluginDetail/:id',
            name: 'pluginDetail',
            component: () => import('pages/bbs/home_components/market/pluginDetail.vue')
        },
        {
            path: '/market/pluginRelease/:id',
            name: 'pluginRelease',
            component: () => import('pages/bbs/home_components/market/pluginRelease.vue')
        },
        {
            path: '/market/pluginUpdate/:id',
            name: 'pluginUpdate',
            component: () => import('pages/bbs/home_components/market/pluginUpdate.vue')
        },
        ]
    },
      {
        path: '/community/mobile',
        name: 'community_mobile',
        redirect: '/community/mobile/articleList',
        component: () => import('pages/bbs/mobile/home.vue'),
        children: [
          {
            path: 'articleList',
            name: 'articleList',
            component: () => import('pages/bbs/mobile/articleList.vue'),
          },
          {
            path: 'articleListDV',
            name: 'articleListDV',
            component: () => import('pages/bbs/mobile/articleListDV.vue'),
          },
          {
            path: 'GreaterWMSDetail/:id',
            name: 'GreaterWMSDetail_m',
            component: () => import('pages/bbs/mobile/articleDetail.vue')
          },
          {
            path: 'DVadminDetail/:id',
            name: 'DVadminDetail_m',
            component: () => import('pages/bbs/mobile/articleDetailDV.vue')
          },
        ]
      },
    ]
},

// Always leave this as last one,
// but you can also remove it
{
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
}
]

export default routes
