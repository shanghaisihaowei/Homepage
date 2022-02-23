import {
    boot
} from 'quasar/wrappers'
import axios from 'axios'
import {
    Notify,
    Cookies
} from 'quasar'
import {
    i18n
} from './i18n'

const baseurl = window.g.BaseUrl


const axiosInstance = axios.create({
    baseURL: baseurl,
    timeout: 30000
})

const axiosInstanceVersion = axios.create({
    baseURL: baseurl,
    timeout: 30000
})

const axiosInstanceAuth = axios.create({
    baseURL: baseurl,
    timeout: 30000
})

const axiosFile = axios.create({
    baseURL: baseurl,
    timeout: 36000000
})

function getauth(url) {
    return axiosInstanceAuth.get(url)
}

function get(url) {
    return axiosInstance.get(url)
}

function versioncheck(url) {
    return axiosInstanceVersion.get(url)
}

function post(url, data) {
    return axiosInstance.post(url, data)
}

function postauth(url, data) {
    return axiosInstanceAuth.post(url, data)
}

function putauth(url, data) {
    return axiosInstanceAuth.put(url, data)
}

function patchauth(url, data) {
    return axiosInstanceAuth.patch(url, data)
}

function deleteauth(url) {
    return axiosInstanceAuth.delete(url)
}

function ViewPrintAuth(url) {
    return axiosInstanceAuth.get(url)
}

function uploadpost(url, data) {
    return axiosFile.post(url, data)
}
function uploadput(url, data) {
    return axiosFile.put(url, data)
}

export default boot(({
    app, ssrContext
}) => {
    const cookies = process.env.SERVER
        ? Cookies.parseSSR(ssrContext)
        : Cookies

    var lang = cookies.get('lang')
    if (cookies) {
        lang = lang || 'en-US'
    } else {
        cookies.set('lang', 'en-US')
        lang = 'en-US'
    }

    axiosInstanceAuth.interceptors.request.use(
        function (config) {
            config.headers.post['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.patch['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.put['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.language = lang
            let token = cookies.get('token')
            if (token) {
                config.headers.Authorization = `Bearer ${token}`
            }
            return config
        },
        function (error) {
            return Promise.reject(error)
        }
    )

    axiosInstanceAuth.interceptors.response.use(
        function (response) {
            if (response.data.detail) {
                if (response.data.detail !== '服务器升级，登录令牌无效，请退出重新登录！' || response.data.detail !== '此令牌对任何类型的令牌无效') {
                    Notify.create({
                        message: response.data.detail,
                        icon: 'close',
                        color: 'negative',
                        timeout: 1500
                    })
                    cookies.remove('token')
                }
            }
            return response.data
        },
        function (error) {
            const defaultNotify = {
                message: i18n.t('notice.unknow_error'),
                icon: 'close',
                color: 'negative',
                timeout: 1500
            }
            if (error.code === 'ECONNABORTED' || error.message.indexOf('timeout') !== -1 || error.message ===
                'Network Error') {
                defaultNotify.message = i18n.t('notice.network_error')
                Notify.create(defaultNotify)
                return Promise.reject(error)
            }
            switch (error.response.status) {
                case 400:
                    defaultNotify.message = i18n.t('notice.400')
                    Notify.create(defaultNotify)
                    break
                case 401:
                    defaultNotify.message = i18n.t('notice.401')
                    Notify.create(defaultNotify)
                    break
                case 403:
                    defaultNotify.message = i18n.t('notice.403')
                    Notify.create(defaultNotify)
                    break
                case 404:
                    defaultNotify.message = i18n.t('notice.404')
                    Notify.create(defaultNotify)
                    break
                case 405:
                    defaultNotify.message = i18n.t('notice.405')
                    Notify.create(defaultNotify)
                    break
                case 408:
                    defaultNotify.message = i18n.t('notice.408')
                    Notify.create(defaultNotify)
                    break
                case 409:
                    defaultNotify.message = i18n.t('notice.409')
                    Notify.create(defaultNotify)
                    break
                case 410:
                    defaultNotify.message = i18n.t('notice.410')
                    Notify.create(defaultNotify)
                    break
                case 500:
                    defaultNotify.message = i18n.t('notice.500')
                    Notify.create(defaultNotify)
                    break
                case 501:
                    defaultNotify.message = i18n.t('notice.501')
                    Notify.create(defaultNotify)
                    break
                case 502:
                    defaultNotify.message = i18n.t('notice.502')
                    Notify.create(defaultNotify)
                    break
                case 503:
                    defaultNotify.message = i18n.t('notice.503')
                    Notify.create(defaultNotify)
                    break
                case 504:
                    defaultNotify.message = i18n.t('notice.504')
                    Notify.create(defaultNotify)
                    break
                case 505:
                    defaultNotify.message = i18n.t('notice.505')
                    Notify.create(defaultNotify)
                    break
                default:
                    Notify.create(defaultNotify)
                    break
            }
            return Promise.reject(error)
        }
    )

    axiosInstance.interceptors.request.use(
        function (config) {
            config.headers.post['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.language = lang
            return config
        },
        function (error) {
            return Promise.reject(error)
        }
    )

    axiosInstance.interceptors.response.use(
        function (response) {
            if (response.data.detail) {
                Notify.create({
                    message: response.data.detail,
                    icon: 'close',
                    color: 'negative',
                    timeout: 1500
                })
            }
            return response.data
        },
        function (error) {
            const defaultNotify = {
                message: i18n.t('notice.network_error'),
                icon: 'close',
                color: 'negative',
                timeout: 1500
            }
            if (error.code === 'ECONNABORTED' || error.message.indexOf('timeout') !== -1 || error.message ===
                'Network Error') {
                defaultNotify.message = i18n.t('notice.network_error')
                Notify.create(defaultNotify)
                return Promise.reject(error)
            }
            switch (error.response.status) {
                case 400:
                    defaultNotify.message = i18n.t('notice.400')
                    Notify.create(defaultNotify)
                    break
                case 401:
                    defaultNotify.message = i18n.t('notice.401')
                    Notify.create(defaultNotify)
                    break
                case 403:
                    defaultNotify.message = i18n.t('notice.403')
                    Notify.create(defaultNotify)
                    break
                case 404:
                    defaultNotify.message = i18n.t('notice.404')
                    Notify.create(defaultNotify)
                    break
                case 405:
                    defaultNotify.message = i18n.t('notice.405')
                    Notify.create(defaultNotify)
                    break
                case 408:
                    defaultNotify.message = i18n.t('notice.408')
                    Notify.create(defaultNotify)
                    break
                case 409:
                    defaultNotify.message = i18n.t('notice.409')
                    Notify.create(defaultNotify)
                    break
                case 410:
                    defaultNotify.message = i18n.t('notice.410')
                    Notify.create(defaultNotify)
                    break
                case 500:
                    defaultNotify.message = i18n.t('notice.500')
                    Notify.create(defaultNotify)
                    break
                case 501:
                    defaultNotify.message = i18n.t('notice.501')
                    Notify.create(defaultNotify)
                    break
                case 502:
                    defaultNotify.message = i18n.t('notice.502')
                    Notify.create(defaultNotify)
                    break
                case 503:
                    defaultNotify.message = i18n.t('notice.503')
                    Notify.create(defaultNotify)
                    break
                case 504:
                    defaultNotify.message = i18n.t('notice.504')
                    Notify.create(defaultNotify)
                    break
                case 505:
                    defaultNotify.message = i18n.t('notice.505')
                    Notify.create(defaultNotify)
                    break
                default:
                    Notify.create(defaultNotify)
                    break
            }
            return Promise.reject(error)
        }
    )

    axiosInstanceVersion.interceptors.request.use(
        function (config) {
            return config
        },
        function (error) {
            return Promise.reject(error)
        }
    )

    axiosInstanceVersion.interceptors.response.use(
        function (response) {
            return response.data
        },
        function (error) {
            return Promise.reject(error)
        }
    )

    axiosFile.interceptors.request.use(
        function (config) {
            config.headers.post['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.patch['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.put['Content-Type'] = 'application/json, charset="utf-8"'
            config.headers.language = lang
            let token = cookies.get('token')
            if (token) {
                config.headers.Authorization = `Bearer ${token}`
            }
            return config
        },
        function (error) {
            return Promise.reject(error)
        }
    )

    axiosFile.interceptors.response.use(
        function (response) {
            if (response.data.detail) {
                Notify.create({
                    message: response.data.detail,
                    icon: 'close',
                    color: 'negative',
                    timeout: 1500
                })
            }
            return response
        },
        // function (error) {
        //     const defaultNotify = {
        //         message: i18n.t('notice.network_error'),
        //         icon: 'close',
        //         color: 'negative',
        //         timeout: 1500
        //     }
        //     if (error.code === 'ECONNABORTED' || error.message.indexOf('timeout') !== -1 || error.message ===
        //         'Network Error') {
        //         defaultNotify.message = i18n.t('notice.network_error')
        //         Notify.create(defaultNotify)
        //         return Promise.reject(error)
        //     }
        //     switch (error.response.status) {
        //         case 400:
        //             defaultNotify.message = i18n.t('notice.400')
        //             Notify.create(defaultNotify)
        //             break
        //         case 401:
        //             defaultNotify.message = i18n.t('notice.401')
        //             Notify.create(defaultNotify)
        //             break
        //         case 403:
        //             defaultNotify.message = i18n.t('notice.403')
        //             Notify.create(defaultNotify)
        //             break
        //         case 404:
        //             defaultNotify.message = i18n.t('notice.404')
        //             Notify.create(defaultNotify)
        //             break
        //         case 405:
        //             defaultNotify.message = i18n.t('notice.405')
        //             Notify.create(defaultNotify)
        //             break
        //         case 408:
        //             defaultNotify.message = i18n.t('notice.408')
        //             Notify.create(defaultNotify)
        //             break
        //         case 409:
        //             defaultNotify.message = i18n.t('notice.409')
        //             Notify.create(defaultNotify)
        //             break
        //         case 410:
        //             defaultNotify.message = i18n.t('notice.410')
        //             Notify.create(defaultNotify)
        //             break
        //         case 500:
        //             defaultNotify.message = i18n.t('notice.500')
        //             Notify.create(defaultNotify)
        //             break
        //         case 501:
        //             defaultNotify.message = i18n.t('notice.501')
        //             Notify.create(defaultNotify)
        //             break
        //         case 502:
        //             defaultNotify.message = i18n.t('notice.502')
        //             Notify.create(defaultNotify)
        //             break
        //         case 503:
        //             defaultNotify.message = i18n.t('notice.503')
        //             Notify.create(defaultNotify)
        //             break
        //         case 504:
        //             defaultNotify.message = i18n.t('notice.504')
        //             Notify.create(defaultNotify)
        //             break
        //         case 505:
        //             defaultNotify.message = i18n.t('notice.505')
        //             Notify.create(defaultNotify)
        //             break
        //         default:
        //             Notify.create(defaultNotify)
        //             break
        //     }
        //     return Promise.reject(error)
        // }
    )

    app.config.globalProperties.$axios = axios
})

export {
    get,
    versioncheck,
    post,
    getauth,
    postauth,
    putauth,
    deleteauth,
    patchauth,
    ViewPrintAuth,
    uploadpost,
    uploadput
}
