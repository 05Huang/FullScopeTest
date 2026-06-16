/**
 * FullScopeTest JavaScript/TypeScript SDK
 *
 * @example
 * ```ts
 * import { FullScopeTestClient } from '@fullscopetest/sdk';
 *
 * const client = new FullScopeTestClient({
 *   baseUrl: 'https://api.fullscopetest.com',
 *   apiToken: 'fst_xxx',
 * });
 *
 * const result = await client.runTests({ projectId: 1, testType: 'api' });
 * ```
 */

export interface ClientConfig {
  baseUrl: string;
  apiToken?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface TestRunResult {
  test_run_id: number;
  report_id: number;
  total: number;
  passed: number;
  failed: number;
  duration: number;
}

export interface TestCase {
  id?: number;
  name: string;
  method: string;
  url: string;
  headers?: Record<string, string>;
  body?: any;
  assertions?: any[];
}

export interface Project {
  id: number;
  name: string;
  description?: string;
}

export class FullScopeTestClient {
  private baseUrl: string;
  private apiToken: string;
  private timeout: number;
  private maxRetries: number;

  constructor(config: ClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.apiToken = config.apiToken || '';
    this.timeout = config.timeout || 30000;
    this.maxRetries = config.maxRetries || 3;
  }

  private async request<T>(method: string, path: string, body?: any): Promise<T> {
    const url = `${this.baseUrl}/api/v1${path}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (this.apiToken) {
      headers['Authorization'] = `Bearer ${this.apiToken}`;
    }

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await fetch(url, {
          method,
          headers,
          body: body ? JSON.stringify(body) : undefined,
          signal: AbortSignal.timeout(this.timeout),
        });

        if (!response.ok) {
          const errorBody = await response.text();
          if (attempt < this.maxRetries && response.status >= 500) {
            await this.delay(attempt * 1000);
            continue;
          }
          throw new Error(`HTTP ${response.status}: ${errorBody}`);
        }

        return await response.json();
      } catch (error: any) {
        if (attempt < this.maxRetries && error.name === 'TimeoutError') {
          await this.delay(attempt * 1000);
          continue;
        }
        throw error;
      }
    }
    throw new Error('Max retries exceeded');
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /** 执行测试 */
  async runTests(params: {
    projectId: number;
    testType?: string;
    collectionId?: number;
    triggeredBy?: string;
  }): Promise<TestRunResult> {
    const data = await this.request<any>('POST', '/test-runs/execute', {
      project_id: params.projectId,
      test_type: params.testType || 'api',
      collection_id: params.collectionId,
      triggered_by: params.triggeredBy || 'sdk',
    });
    return data.data;
  }

  /** 查询执行状态 */
  async getRunStatus(runId: number): Promise<any> {
    const data = await this.request<any>('GET', `/test-runs/${runId}`);
    return data.data;
  }

  /** 获取测试报告 */
  async getReport(reportId: number): Promise<any> {
    const data = await this.request<any>('GET', `/reports/${reportId}`);
    return data.data;
  }

  /** 创建用例 */
  async createCase(collectionId: number, testCase: TestCase): Promise<TestCase> {
    const data = await this.request<any>('POST', '/api-test/cases', {
      collection_id: collectionId,
      ...testCase,
    });
    return data.data;
  }

  /** 列出项目 */
  async listProjects(): Promise<Project[]> {
    const data = await this.request<any>('GET', '/projects');
    return data.data;
  }

  /** 健康检查 */
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    return await response.json();
  }
}

export default FullScopeTestClient;
