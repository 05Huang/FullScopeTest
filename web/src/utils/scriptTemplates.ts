/**
 * API 测试脚本模板库
 *
 * 提供常用的前置脚本和后置断言模板
 */

export interface ScriptTemplate {
  name: string
  description: string
  category: 'pre' | 'post'
  code: string
}

// ==================== 前置脚本模板 ====================

export const preScriptTemplates: ScriptTemplate[] = [
  {
    name: '时间戳参数',
    description: '添加当前时间戳到请求参数',
    category: 'pre',
    code: `// 添加时间戳参数
const timestamp = Date.now()
pm.request.url = pm.request.url + (pm.request.url.includes('?') ? '&' : '?') + 't=' + timestamp
console.log('已添加时间戳:', timestamp)`
  },
  {
    name: '随机数生成',
    description: '生成随机数用于测试',
    category: 'pre',
    code: `// 生成随机数
const randomNum = Math.floor(Math.random() * 100000)
pm.environment.set('random_num', randomNum)
console.log('生成随机数:', randomNum)`
  },
  {
    name: '设置请求头',
    description: '动态设置或修改请求头',
    category: 'pre',
    code: `// 设置请求头
pm.request.headers['X-Custom-Header'] = 'custom-value'
pm.request.headers['X-Timestamp'] = Date.now().toString()
console.log('已设置自定义请求头')`
  },
  {
    name: '使用 Token',
    description: '从环境变量获取 Token 并设置到请求头',
    category: 'pre',
    code: `// 从环境变量获取 Token
const token = pm.environment.get('auth_token')
if (token) {
  pm.request.headers['Authorization'] = 'Bearer ' + token
  console.log('已设置 Authorization')
} else {
  console.warn('未找到 auth_token，请先执行登录接口')
}`
  },
  {
    name: '计算签名',
    description: '计算请求签名（示例）',
    category: 'pre',
    code: `// 计算请求签名示例
const timestamp = Date.now()
const secret = pm.environment.get('api_secret') || 'your-secret-key'

// 简单的签名示例（实际根据业务需求调整）
const signStr = timestamp + secret
const sign = require('crypto').createHash('md5').update(signStr).digest('hex')

pm.request.headers['X-Timestamp'] = timestamp.toString()
pm.request.headers['X-Sign'] = sign
console.log('签名已生成:', sign)`
  }
]

// ==================== 后置断言模板 ====================

export const postScriptTemplates: ScriptTemplate[] = [
  {
    name: '状态码验证',
    description: '验证 HTTP 状态码',
    category: 'post',
    code: `// 验证状态码为 200
pm.test('状态码为 200', function() {
  pm.response.to.have.status(200)
})`
  },
  {
    name: '获取 Token',
    description: '验证登录成功并提取 Token',
    category: 'post',
    code: `// 验证登录成功
pm.test('登录成功', function() {
  const json = pm.response.json()
  pm.expect(json.code).to.eql(200)
  pm.expect(json.data).to.have.property('token')
})

// 提取 token 供后续接口使用
const json = pm.response.json()
pm.environment.set('auth_token', json.data.token)
pm.environment.set('user_id', json.data.id)
console.log('已提取 token:', json.data.token.substring(0, 10) + '...')`
  },
  {
    name: '响应结构验证',
    description: '验证返回的数据结构',
    category: 'post',
    code: `// 验证响应结构
pm.test('返回正确的数据结构', function() {
  const json = pm.response.json()
  pm.expect(json).to.have.property('code')
  pm.expect(json).to.have.property('data')
  pm.expect(json.data).to.have.property('id')
  pm.expect(json.data).to.have.property('name')
  pm.expect(json.data.name).to.be.a('string')
})`
  },
  {
    name: '业务逻辑验证',
    description: '验证业务逻辑（如订单金额）',
    category: 'post',
    code: `// 验证订单金额计算
pm.test('订单金额计算正确', function() {
  const json = pm.response.json()
  const expectTotal = json.data.price * json.data.quantity
  pm.expect(json.data.totalAmount).to.eql(expectTotal)
})`
  },
  {
    name: '响应时间验证',
    description: '验证响应时间是否满足要求',
    category: 'post',
    code: `// 验证响应时间
pm.test('响应时间小于 500ms', function() {
  pm.expect(pm.response.responseTime).to.be.below(500)
})

pm.test('响应时间小于 200ms 为优秀', function() {
  pm.expect(pm.response.responseTime).to.be.below(200)
})`
  },
  {
    name: '字段存在性验证',
    description: '验证关键字段是否存在',
    category: 'post',
    code: `// 验证字段存在
pm.test('包含必要字段', function() {
  const json = pm.response.json()
  pm.expect(json.data).to.have.property('id')
  pm.expect(json.data).to.have.property('createdAt')
  pm.expect(json.data).to.have.property('updatedAt')
})`
  },
  {
    name: '数组长度验证',
    description: '验证返回数组的长度',
    category: 'post',
    code: `// 验证数组长度
pm.test('返回数据列表', function() {
  const json = pm.response.json()
  pm.expect(json.data).to.be.an('array')
  pm.expect(json.data.length).to.be.above(0)
})

pm.test('数据不超过100条', function() {
  const json = pm.response.json()
  pm.expect(json.data.length).to.be.below(100)
})`
  },
  {
    name: '提取变量',
    description: '从响应中提取变量供后续使用',
    category: 'post',
    code: `// 提取响应中的数据
const json = pm.response.json()

pm.environment.set('user_id', json.data.id)
pm.environment.set('username', json.data.username)
pm.environment.set('order_id', json.data.orderId)

console.log('已提取变量:', Object.keys(json.data))`
  }
]

// ==================== 完整示例模板 ====================

/**
 * 登录接口完整示例
 */
export const loginExample = {
  preScript: `// 登录接口通常不需要前置脚本
console.log('准备执行登录请求')`,
  postScript: `// 验证登录成功
pm.test('登录成功', function() {
  const json = pm.response.json()
  pm.expect(json.code).to.eql(200)
  pm.expect(json.data).to.have.property('token')
  pm.expect(json.data).to.have.property('user')
})

// 提取 token 和用户信息
const json = pm.response.json()
pm.environment.set('auth_token', json.data.token)
pm.environment.set('user_id', json.data.user.id)
pm.environment.set('username', json.data.user.username)

console.log('登录成功，用户:', json.data.user.username)`
}

/**
 * 需要认证的接口示例
 */
export const authenticatedRequestExample = {
  preScript: `// 使用之前保存的 token
const token = pm.environment.get('auth_token')
if (token) {
  pm.request.headers['Authorization'] = 'Bearer ' + token
} else {
  console.error('未找到 auth_token，请先执行登录接口')
}`,
  postScript: `// 验证请求成功
pm.test('请求成功', function() {
  const json = pm.response.json()
  pm.expect(json.code).to.eql(200)
})

// 验证响应时间
pm.test('响应时间小于 500ms', function() {
  pm.expect(pm.response.responseTime).to.be.below(500)
})`
}

/**
 * 导出所有模板
 */
export const allTemplates = {
  pre: preScriptTemplates,
  post: postScriptTemplates,
  examples: {
    login: loginExample,
    authenticated: authenticatedRequestExample
  }
}

/**
 * 根据分类获取模板
 */
export function getTemplates(category: 'pre' | 'post'): ScriptTemplate[] {
  return category === 'pre' ? preScriptTemplates : postScriptTemplates
}

/**
 * 根据名称搜索模板
 */
export function searchTemplate(keyword: string): ScriptTemplate[] {
  const all = [...preScriptTemplates, ...postScriptTemplates]
  return all.filter(t =>
    t.name.toLowerCase().includes(keyword.toLowerCase()) ||
    t.description.toLowerCase().includes(keyword.toLowerCase())
  )
}
