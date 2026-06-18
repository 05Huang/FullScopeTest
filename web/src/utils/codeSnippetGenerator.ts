/**
 * 多语言代码片段生成器
 *
 * 将 HTTP 请求转换为多种编程语言的可运行代码片段
 */

interface RequestSnippet {
  method: string
  url: string
  headers: Array<{ key: string; value: string }>
  body?: string
}

/**
 * 生成 cURL 命令
 */
export function generateCurl(req: RequestSnippet): string {
  let curl = `curl -X ${req.method} '${req.url}'`
  req.headers.filter(h => h.key && h.value).forEach(h => {
    curl += ` \\n  -H '${h.key}: ${h.value}'`
  })
  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body && req.body !== '{}') {
    curl += ` \\n  -d '${req.body}'`
  }
  return curl
}

/**
 * 生成 Python requests 代码
 */
export function generatePython(req: RequestSnippet): string {
  const headers: Record<string, string> = {}
  req.headers.filter(h => h.key && h.value).forEach(h => {
    headers[h.key] = h.value
  })

  let code = `import requests\n\n`
  code += `url = "${req.url}"\n`

  if (Object.keys(headers).length > 0) {
    code += `headers = ${JSON.stringify(headers, null, 4)}\n`
  }

  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
    code += `payload = ${req.body}\n\n`
    code += `response = requests.${req.method.toLowerCase()}(url`
    if (Object.keys(headers).length > 0) code += `, headers=headers`
    code += `, json=payload)\n`
  } else {
    code += `\nresponse = requests.${req.method.toLowerCase()}(url`
    if (Object.keys(headers).length > 0) code += `, headers=headers`
    code += `)\n`
  }

  code += `\nprint(response.status_code)\nprint(response.json())`
  return code
}

/**
 * 生成 JavaScript fetch 代码
 */
export function generateJavaScript(req: RequestSnippet): string {
  const headers: Record<string, string> = {}
  req.headers.filter(h => h.key && h.value).forEach(h => {
    headers[h.key] = h.value
  })

  let code = `const response = await fetch("${req.url}", {\n`
  code += `  method: "${req.method}",\n`

  if (Object.keys(headers).length > 0) {
    code += `  headers: ${JSON.stringify(headers, null, 4)},\n`
  }

  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
    code += `  body: JSON.stringify(${req.body}),\n`
  }

  code += `});\n\nconst data = await response.json();\nconsole.log(data);`
  return code
}

/**
 * 生成 Java OkHttp 代码
 */
export function generateJava(req: RequestSnippet): string {
  let code = `OkHttpClient client = new OkHttpClient();\n\n`

  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
    code += `MediaType JSON = MediaType.get("application/json; charset=utf-8");\n`
    code += `RequestBody body = RequestBody.create(${JSON.stringify(req.body)}, JSON);\n\n`
  }

  code += `Request request = new Request.Builder()\n`
  code += `    .url("${req.url}")\n`

  req.headers.filter(h => h.key && h.value).forEach(h => {
    code += `    .addHeader("${h.key}", "${h.value}")\n`
  })

  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
    code += `    .${req.method.toLowerCase()}(body)\n`
  } else {
    code += `    .${req.method.toLowerCase()}()\n`
  }

  code += `    .build();\n\n`
  code += `try (Response response = client.newCall(request).execute()) {\n`
  code += `    System.out.println(response.body().string());\n`
  code += `}`
  return code
}

/**
 * 生成 Go net/http 代码
 */
export function generateGo(req: RequestSnippet): string {
  let code = `package main\n\nimport (\n    "fmt"\n    "io"\n    "net/http"\n`

  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
    code += `    "strings"\n`
  }

  code += `)\n\nfunc main() {\n`

  if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body) {
    code += `    body := strings.NewReader(${JSON.stringify(req.body)})\n`
    code += `    req, err := http.NewRequest("${req.method}", "${req.url}", body)\n`
  } else {
    code += `    req, err := http.NewRequest("${req.method}", "${req.url}", nil)\n`
  }

  code += `    if err != nil {\n        panic(err)\n    }\n\n`

  req.headers.filter(h => h.key && h.value).forEach(h => {
    code += `    req.Header.Set("${h.key}", "${h.value}")\n`
  })

  code += `\n    resp, err := http.DefaultClient.Do(req)\n`
  code += `    if err != nil {\n        panic(err)\n    }\n    defer resp.Body.Close()\n\n`
  code += `    data, _ := io.ReadAll(resp.Body)\n`
  code += `    fmt.Println(string(data))\n}`
  return code
}

/** 代码生成器映射 */
export const snippetGenerators: Record<string, (req: RequestSnippet) => string> = {
  curl: generateCurl,
  python: generatePython,
  javascript: generateJavaScript,
  java: generateJava,
  go: generateGo,
}
