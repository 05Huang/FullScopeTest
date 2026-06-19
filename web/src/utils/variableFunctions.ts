/**
 * 内置变量函数库
 *
 * 提供可在 URL/Header/Body 中使用的动态变量函数：
 *   {{$randomEmail}} / {{$randomPhone}} / {{$randomName}}
 *   {{$timestamp}} / {{$date}} / {{$uuid}}
 *   {{$randomInt(min,max)}} / {{$randomString(length)}}
 */

/** 生成 UUID v4 */
function uuid(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => {
    const r = (Math.random() * 16) | 0
    const v = c === "x" ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

/** 随机整数 */
function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

/** 随机字符串 */
function randomString(length: number): string {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  let result = ""
  for (let i = 0; i < length; i++) result += chars.charAt(Math.floor(Math.random() * chars.length))
  return result
}

/** 随机邮箱 */
function randomEmail(): string {
  return randomString(8).toLowerCase() + "@example.com"
}

/** 随机手机号 */
function randomPhone(): string {
  const prefixes = ["138","139","150","151","152","157","158","159","186","187","188"]
  return prefixes[Math.floor(Math.random() * prefixes.length)] + String(randomInt(10000000, 99999999))
}

/** 随机姓名 */
function randomName(): string {
  const surnames = ["张","李","王","刘","陈","杨","黄","赵","周","吴"]
  const names = ["伟","芳","娜","秀英","敏","静","丽","强","磊","洋"]
  return surnames[randomInt(0, surnames.length - 1)] + names[randomInt(0, names.length - 1)]
}

/** 内置变量函数映射 */
export const VARIABLE_FUNCTIONS: Record<string, () => string> = {
  "$randomEmail": randomEmail,
  "$randomPhone": randomPhone,
  "$randomName": randomName,
  "$timestamp": () => String(Date.now()),
  "$date": () => new Date().toISOString().split("T")[0],
  "$uuid": uuid,
  "$randomInt": () => String(randomInt(1, 10000)),
  "$randomString": () => randomString(16),
}

/** 带参数的变量函数正则 */
const PARAM_REGEX = /\{\{\$(\w+)\(([^)]*)\)\}\}/g

/** 简单变量正则 */
const SIMPLE_REGEX = /\{\{\$(\w+)\}\}/g

/**
 * 替换字符串中的变量函数调用
 *
 * 示例：
 *   "{{$timestamp}}" -> "1718800000000"
 *   "{{$randomInt(1,100)}}" -> "42"
 *   "user_{{$randomString(8)}}" -> "user_aBcDeFgH"
 */
export function replaceVariableFunctions(input: string): string {
  if (!input) return input

  // 替换带参数的函数：{{$func(arg1,arg2)}}
  let result = input.replace(PARAM_REGEX, (match, funcName, args) => {
    if (funcName === "randomInt") {
      const [min, max] = args.split(",").map(Number)
      return String(randomInt(min || 1, max || 10000))
    }
    if (funcName === "randomString") {
      return randomString(Number(args) || 16)
    }
    const fn = VARIABLE_FUNCTIONS["$" + funcName]
    return fn ? fn() : match
  })

  // 替换简单函数：{{$func}}
  result = result.replace(SIMPLE_REGEX, (match, funcName) => {
    const fn = VARIABLE_FUNCTIONS["$" + funcName]
    return fn ? fn() : match
  })

  return result
}

/** 获取所有可用的变量函数名称（用于自动补全提示） */
export function getVariableFunctionNames(): string[] {
  return Object.keys(VARIABLE_FUNCTIONS)
}
