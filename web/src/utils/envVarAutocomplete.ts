/**
 * 环境变量自动补全工具
 *
 * 为 Monaco Editor 提供 {{variable}} 语法的自动补全。
 * 检测输入 {{ 时触发下拉列表，列出当前环境的所有变量名和值。
 */

import type * as Monaco from 'monaco-editor'

interface EnvVariable {
  name: string
  value: string
}

/**
 * 注册环境变量自动补全到 Monaco Editor
 *
 * @param monaco Monaco 实例
 * @param getVariables 获取当前环境变量的函数
 */
export function registerEnvVarAutocomplete(
  monaco: typeof Monaco,
  getVariables: () => EnvVariable[],
): void {
  // 移除已有的注册（避免重复）
  // Monaco 会自动处理重复注册

  monaco.languages.registerCompletionItemProvider('json', {
    triggerCharacters: ['{'],
    provideCompletionItems: (model, position) => {
      const lineContent = model.getLineContent(position.lineNumber)
      const textBeforeCursor = lineContent.substring(0, position.column - 1)

      // 检测是否在 {{ 后面
      if (!textBeforeCursor.endsWith('{{')) {
        return { suggestions: [] }
      }

      const variables = getVariables()
      const suggestions = variables.map((v) => ({
        label: `{{${v.name}}}`,
        kind: monaco.languages.CompletionItemKind.Variable,
        detail: v.value.length > 20 ? v.value.substring(0, 20) + '...' : v.value,
        insertText: `${v.name}}}`,
        range: {
          startLineNumber: position.lineNumber,
          startColumn: position.column,
          endLineNumber: position.lineNumber,
          endColumn: position.column,
        },
      }))

      return { suggestions }
    },
  })

  // 也为纯文本和 yaml 提供补全
  const additionalLanguages = ['plaintext', 'yaml', 'xml']
  additionalLanguages.forEach((language) => {
    monaco.languages.registerCompletionItemProvider(language, {
      triggerCharacters: ['{'],
      provideCompletionItems: (model, position) => {
        const lineContent = model.getLineContent(position.lineNumber)
        const textBeforeCursor = lineContent.substring(0, position.column - 1)

        if (!textBeforeCursor.endsWith('{{')) {
          return { suggestions: [] }
        }

        const variables = getVariables()
        const suggestions = variables.map((v) => ({
          label: `{{${v.name}}}`,
          kind: monaco.languages.CompletionItemKind.Variable,
          detail: v.value.length > 20 ? v.value.substring(0, 20) + '...' : v.value,
          insertText: `${v.name}}}`,
          range: {
            startLineNumber: position.lineNumber,
            startColumn: position.column,
            endLineNumber: position.lineNumber,
            endColumn: position.column,
          },
        }))

        return { suggestions }
      },
    })
  })
}
