import request from '@/utils/request'

export function apiProductCreate(data) {
  return request({
    url: '/api/product/create',
    method: 'post',
    data: data
  })
}

export function apiProductUpdate(data) {
  return request({
    url: '/api/product/update',
    method: 'post',
    data: data
  })
}

export function apiProductDelete(id) {
  return request({
    url: '/api/product/delete',
    method: 'delete',
    params: {
      'id': id
    }
  })
}

export function apiProductRemove(id) {
  return request({
    url: '/api/product/remove',
    method: 'post',
    params: {
      'id': id
    }
  })
}

// 条件查询
export function apiProductSearch(params) {
  return request({
    url: '/api/product/search',
    method: 'get',
    params: params
  })
}
