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
    /** 可视化断言结果 */
    visual_assertions?: {
      total: number
      passed: number
      failed: number
      details?: Array<{
        name: string
        passed: boolean
        actual?: unknown
        expected?: unknown
        error?: string
        assertion_type?: string
      }>
    }
  }
}

const ScriptTestResults: React.FC<ScriptTestResultsProps> = ({ scriptExecution }) => {
  const { t } = useTranslation();
  if (!scriptExecution) {
    return <Empty description={t("apiTest.noCases")} />
  }

  const { pre_script, post_script, visual_assertions } = scriptExecution

  const hasExecutedScript = (pre_script?.executed || post_script?.executed)
  const hasVisualAssertions = (visual_assertions?.total ?? 0) > 0

  if (!hasExecutedScript && !hasVisualAssertions) {
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

      {/* 可视化断言结果 */}
      {hasVisualAssertions && visual_assertions && (
        <Card size="small" title={<Space><Text strong>可视化断言</Text></Space>}>
          <Space direction="vertical" style={{ width: "100%" }} size="small">
            <Space>
              {visual_assertions.failed === 0 ? (
                <Tag icon={<CheckCircleOutlined />} color="success">{t("common.passed")}</Tag>
              ) : (
                <Tag icon={<CloseCircleOutlined />} color="error">{t("common.failed")}</Tag>
              )}
              <Text>总计: <Text strong>{visual_assertions.total}</Text></Text>
              <Text type="success">通过: <Text strong>{visual_assertions.passed}</Text></Text>
              {visual_assertions.failed > 0 && (
                <Text type="danger">失败: <Text strong>{visual_assertions.failed}</Text></Text>
              )}
            </Space>

            {/* 可视化断言详情 */}
            {visual_assertions.details && visual_assertions.details.length > 0 && (
              <Table
                size="small"
                dataSource={visual_assertions.details.map((d, i) => ({ ...d, key: i }))}
                columns={[
                  {
                    title: t("common.status"),
                    dataIndex: "passed",
                    width: 60,
                    render: (passed: boolean) => passed ? (
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
                    title: "实际值",
                    dataIndex: "actual",
                    width: 120,
                    render: (val: unknown) => val !== undefined && val !== null ? (
                      <Text code style={{ fontSize: 12 }}>{String(val)}</Text>
                    ) : (
                      <Text type="secondary">-</Text>
                    ),
                  },
                  {
                    title: "期望值",
                    dataIndex: "expected",
                    width: 120,
                    render: (val: unknown) => val !== undefined && val !== null ? (
                      <Text code style={{ fontSize: 12 }}>{String(val)}</Text>
                    ) : (
                      <Text type="secondary">-</Text>
                    ),
                  },
                  {
                    title: t("apiTest.errorMessage"),
                    dataIndex: "error",
                    render: (error: string) => error ? (
                      <Text type="danger" style={{ fontSize: 12 }}>{error}</Text>
                    ) : (
                      <Text type="secondary">-</Text>
                    ),
                  },
                ]}
                pagination={false}
              />
            )}
          </Space>
        </Card>
      )}
    </Space>
  )
}

export default ScriptTestResults
