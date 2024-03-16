import request from '@/utils/request'

export function apiAppsSearch(requestBody) {
  return request({
    url: '/api/application/search',
    method: 'post',
    data: requestBody
  })
}
export function apiAppsProduct() {
  return request({
    url: '/api/application/product',
    method: 'get'
  })
}

export function apiAppsCommit(requestBody) {
  return request({
    url: '/api/application/update',
    method: 'post',
    data: requestBody
  })
}
