import { useTranslation } from "react-i18next"
import { Card, Space, Table, Tag, Typography, Empty } from "antd"
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"

const { Text } = Typography

interface ScriptTestResultsProps {
  scriptExecution?: {
    pre_script?: {
      executed: boolean
      passed?: boolean
      error?: string
      duration?: number
    }
    post_script?: {
      executed: boolean
      passed?: boolean
      error?: string
      duration?: number
      assertions?: {
        total: number
        passed: number
        failed: number
        details?: Array<{
          name: string
          passed: boolean
          error?: string
        }>
      }
    }
  }
}

const ScriptTestResults: React.FC<ScriptTestResultsProps> = ({ scriptExecution }) => {
  const { t } = useTranslation();
  if (!scriptExecution) {
    return <Empty description={t("apiTest.noCases")} />
  }

  const { pre_script, post_script } = scriptExecution

  const hasExecutedScript = (pre_script?.executed || post_script?.executed)

  if (!hasExecutedScript) {
    return <Empty description={t("apiTest.noCases")} />
  }

  return (
    <Space direction="vertical" style={{ width: "100%" }} size="large">
      {/* 前置脚本结果 */}
      {pre_script?.executed && (
        <Card size="small" title={<Space><Text strong>{t("apiTest.preScript")}</Text></Space>}>
          <Space direction="vertical" style={{ width: "100%" }} size="small">
            <Space>
              {pre_script.passed ? (
                <Tag icon={<CheckCircleOutlined />} color="success">{t("apiTest.runSuccess")}</Tag>
              ) : (
                <Tag icon={<CloseCircleOutlined />} color="error">{t("apiTest.runFailed")}</Tag>
              )}
              {pre_script.duration !== undefined && (
                <Text type="secondary">耗时: {pre_script.duration}ms</Text>
              )}
            </Space>
            {pre_script.error && (
              <Text type="danger">{pre_script.error}</Text>
            )}
          </Space>
        </Card>
      )}

      {/* 后置脚本结果 */}
      {post_script?.executed && (
        <Card size="small" title={<Space><Text strong>{t("apiTest.postScript")}</Text></Space>}>
          <Space direction="vertical" style={{ width: "100%" }} size="small">
            <Space>
              {post_script.passed ? (
                <Tag icon={<CheckCircleOutlined />} color="success">{t("common.passed")}</Tag>
              ) : (
                <Tag icon={<CloseCircleOutlined />} color="error">{t("common.failed")}</Tag>
              )}
              {post_script.duration !== undefined && (
                <Text type="secondary">耗时: {post_script.duration}ms</Text>
              )}
            </Space>

            {/* 断言统计 */}
            {post_script.assertions && (
              <Space>
                <Text>总计: <Text strong>{post_script.assertions.total}</Text></Text>
                <Text type="success">通过: <Text strong>{post_script.assertions.passed}</Text></Text>
                {post_script.assertions.failed > 0 && (
                  <Text type="danger">失败: <Text strong>{post_script.assertions.failed}</Text></Text>
                )}
              </Space>
            )}

            {/* 断言详情 */}
            {post_script.assertions?.details && post_script.assertions.details.length > 0 && (
              <Table
                size="small"
                dataSource={post_script.assertions.details.map((d, i) => ({ ...d, key: i }))}
                columns={[
                  {
                    title: t("common.status"),
                    dataIndex: "passed",
                    width: 60,
                    render: (passed) => passed ? (
                      <CheckCircleOutlined style={{ color: "#52c41a" }} />
                    ) : (
                      <CloseCircleOutlined style={{ color: "#ff4d4f" }} />
                    ),
                  },
                  {
                    title: t("apiTest.assertionDesc"),
                    dataIndex: "name",
                    ellipsis: true,
                  },
                  {
                    title: t("apiTest.errorMessage"),
                    dataIndex: "error",
                    render: (error) => error ? (
                      <Text type="danger" style={{ fontSize: 12 }}>{error}</Text>
                    ) : (
                      <Text type="secondary">-</Text>
                    ),
                  },
                ]}
                pagination={false}
                showHeader={false}
              />
            )}

            {post_script.error && (
              <Text type="danger">{post_script.error}</Text>
            )}
          </Space>
        </Card>
      )}
    </Space>
  )
}

export default ScriptTestResults
