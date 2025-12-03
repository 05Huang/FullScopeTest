const { createApp } = Vue;

createApp({
    data() {
        return {
            // 页面状态
            currentPage: 'collections',
            loading: false,
            notification: null,

            // 环境相关
            environments: [],
            selectedEnvironment: null,

            // 集合相关
            collections: [],
            expandedCollections: [],
            currentRequest: null,
            currentRequestCollection: null,

            // 请求相关
            requestTab: 'headers',
            currentResponse: null,

            // 报告相关
            reports: [],

            // 模态框
            showCollectionModal: false,
            showEnvironmentModal: false,
            editingCollection: null,
            editingEnvironment: null,

            // 表单数据
            collectionForm: {
                name: '',
                description: ''
            },
            environmentForm: {
                name: '',
                base_url: '',
                headersText: '{}'
            }
        };
    },

    mounted() {
        this.loadEnvironments();
        this.loadCollections();
        this.loadReports();
    },

    methods: {
        // ============= 通知 =============
        showNotification(message, type = 'success', icon = 'fas fa-check-circle') {
            this.notification = { message, type, icon };
            setTimeout(() => {
                this.notification = null;
            }, 3000);
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN');
        },

        formatJson(text) {
            try {
                return JSON.stringify(JSON.parse(text), null, 2);
            } catch {
                return text;
            }
        },

        // ============= 环境管理 =============
        async loadEnvironments() {
            try {
                this.loading = true;
                const response = await fetch('/api/environments');
                this.environments = await response.json();
            } catch (error) {
                console.error('Error loading environments:', error);
                this.showNotification('加载环境失败', 'error', 'fas fa-exclamation-circle');
            } finally {
                this.loading = false;
            }
        },

        async saveEnvironment() {
            try {
                const url = this.editingEnvironment ? `/api/environments/${this.editingEnvironment.id}` : '/api/environments';
                const method = this.editingEnvironment ? 'PUT' : 'POST';

                const headers = JSON.parse(this.environmentForm.headersText);

                const response = await fetch(url, {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: this.environmentForm.name,
                        base_url: this.environmentForm.base_url,
                        headers: headers
                    })
                });

                if (response.ok) {
                    this.showNotification('环境保存成功', 'success');
                    this.showEnvironmentModal = false;
                    this.editingEnvironment = null;
                    this.loadEnvironments();
                    this.resetEnvironmentForm();
                } else {
                    this.showNotification('保存失败', 'error', 'fas fa-exclamation-circle');
                }
            } catch (error) {
                console.error('Error saving environment:', error);
                this.showNotification('保存环境失败: ' + error.message, 'error', 'fas fa-exclamation-circle');
            }
        },

        async deleteEnvironment(envId) {
            if (!confirm('确定要删除此环境吗？')) return;

            try {
                const response = await fetch(`/api/environments/${envId}`, { method: 'DELETE' });
                if (response.ok) {
                    this.showNotification('环境删除成功', 'success');
                    this.loadEnvironments();
                } else {
                    this.showNotification('删除失败', 'error', 'fas fa-exclamation-circle');
                }
            } catch (error) {
                console.error('Error deleting environment:', error);
                this.showNotification('删除环境失败', 'error', 'fas fa-exclamation-circle');
            }
        },

        editEnvironment(env) {
            this.editingEnvironment = env;
            this.environmentForm = {
                name: env.name,
                base_url: env.base_url,
                headersText: JSON.stringify(env.headers, null, 2)
            };
            this.showEnvironmentModal = true;
        },

        resetEnvironmentForm() {
            this.environmentForm = {
                name: '',
                base_url: '',
                headersText: '{}'
            };
        },

        onEnvironmentChange() {
            this.showNotification(`已切换到环境: ${this.selectedEnvironment?.name || '默认'}`, 'info', 'fas fa-info-circle');
        },

        // ============= 集合管理 =============
        async loadCollections() {
            try {
                this.loading = true;
                const response = await fetch('/api/collections');
                this.collections = await response.json();

                // 加载每个集合的请求
                for (const collection of this.collections) {
                    await this.loadCollectionDetail(collection.id);
                }
            } catch (error) {
                console.error('Error loading collections:', error);
                this.showNotification('加载集合失败', 'error', 'fas fa-exclamation-circle');
            } finally {
                this.loading = false;
            }
        },

        async loadCollectionDetail(collectionId) {
            try {
                const response = await fetch(`/api/collections/${collectionId}`);
                const data = await response.json();
                const collection = this.collections.find(c => c.id === collectionId);
                if (collection) {
                    collection.requests = data.requests;
                }
            } catch (error) {
                console.error('Error loading collection detail:', error);
            }
        },

        async saveCollection() {
            try {
                const url = this.editingCollection ? `/api/collections/${this.editingCollection.id}` : '/api/collections';
                const method = this.editingCollection ? 'PUT' : 'POST';

                const response = await fetch(url, {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: this.collectionForm.name,
                        description: this.collectionForm.description
                    })
                });

                if (response.ok) {
                    this.showNotification('集合保存成功', 'success');
                    this.showCollectionModal = false;
                    this.editingCollection = null;
                    this.loadCollections();
                    this.resetCollectionForm();
                } else {
                    this.showNotification('保存失败', 'error', 'fas fa-exclamation-circle');
                }
            } catch (error) {
                console.error('Error saving collection:', error);
                this.showNotification('保存集合失败', 'error', 'fas fa-exclamation-circle');
            }
        },

        async deleteCollection(collectionId) {
            if (!confirm('确定要删除此集合及其所有请求吗？')) return;

            try {
                const response = await fetch(`/api/collections/${collectionId}`, { method: 'DELETE' });
                if (response.ok) {
                    this.showNotification('集合删除成功', 'success');
                    this.loadCollections();
                    if (this.currentRequestCollection === collectionId) {
                        this.currentRequest = null;
                    }
                } else {
                    this.showNotification('删除失败', 'error', 'fas fa-exclamation-circle');
                }
            } catch (error) {
                console.error('Error deleting collection:', error);
                this.showNotification('删除集合失败', 'error', 'fas fa-exclamation-circle');
            }
        },

        editCollection(collection) {
            this.editingCollection = collection;
            this.collectionForm = {
                name: collection.name,
                description: collection.description
            };
            this.showCollectionModal = true;
        },

        openCollection(collectionId) {
            this.currentPage = 'request';
            this.expandedCollections = [collectionId];
        },

        resetCollectionForm() {
            this.collectionForm = { name: '', description: '' };
        },

        toggleCollectionExpanded(collectionId) {
            const index = this.expandedCollections.indexOf(collectionId);
            if (index > -1) {
                this.expandedCollections.splice(index, 1);
            } else {
                this.expandedCollections.push(collectionId);
            }
        },

        // ============= 请求管理 =============
        async selectRequest(collectionId, requestId) {
            const collection = this.collections.find(c => c.id === collectionId);
            const request = collection?.requests?.find(r => r.id === requestId);
            
            if (request) {
                this.currentRequest = JSON.parse(JSON.stringify(request));
                this.currentRequestCollection = collectionId;
                this.currentRequest.bodyType = 'json';
                this.currentRequest.bodyText = request.body ? JSON.stringify(request.body, null, 2) : '{}';
                this.requestTab = 'headers';
            }
        },

        async addRequest(collectionId) {
            const newRequest = {
                collection_id: collectionId,
                name: 'New Request',
                method: 'GET',
                url: '',
                headers: { 'Content-Type': 'application/json' },
                body: null,
                params: {},
                description: ''
            };

            try {
                const response = await fetch('/api/requests', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newRequest)
                });

                if (response.ok) {
                    const data = await response.json();
                    newRequest.id = data.id;
                    this.showNotification('请求创建成功', 'success');
                    
                    // 重新加载集合
                    await this.loadCollectionDetail(collectionId);
                    
                    // 选择新请求
                    this.selectRequest(collectionId, data.id);
                }
            } catch (error) {
                console.error('Error creating request:', error);
                this.showNotification('创建请求失败', 'error', 'fas fa-exclamation-circle');
            }
        },

        async saveRequest() {
            if (!this.currentRequest) return;

            try {
                // 解析 body
                let body = null;
                if (this.currentRequest.bodyText) {
                    try {
                        body = JSON.parse(this.currentRequest.bodyText);
                    } catch {
                        body = this.currentRequest.bodyText;
                    }
                }

                const updateData = {
                    name: this.currentRequest.name,
                    method: this.currentRequest.method,
                    url: this.currentRequest.url,
                    headers: this.currentRequest.headers,
                    body: body,
                    params: this.currentRequest.params,
                    description: this.currentRequest.description
                };

                const response = await fetch(`/api/requests/${this.currentRequest.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updateData)
                });

                if (response.ok) {
                    this.showNotification('请求保存成功', 'success');
                    await this.loadCollectionDetail(this.currentRequestCollection);
                } else {
                    this.showNotification('保存失败', 'error', 'fas fa-exclamation-circle');
                }
            } catch (error) {
                console.error('Error saving request:', error);
                this.showNotification('保存请求失败', 'error', 'fas fa-exclamation-circle');
            }
        },

        async deleteCurrentRequest() {
            if (!confirm('确定要删除此请求吗？')) return;

            try {
                const response = await fetch(`/api/requests/${this.currentRequest.id}`, { method: 'DELETE' });
                if (response.ok) {
                    this.showNotification('请求删除成功', 'success');
                    this.currentRequest = null;
                    await this.loadCollectionDetail(this.currentRequestCollection);
                }
            } catch (error) {
                console.error('Error deleting request:', error);
                this.showNotification('删除请求失败', 'error', 'fas fa-exclamation-circle');
            }
        },

        addHeader() {
            if (!this.currentRequest.headers) {
                this.$set(this.currentRequest, 'headers', {});
            }
            this.currentRequest.headers[''] = '';
        },

        deleteHeader(key) {
            delete this.currentRequest.headers[key];
        },

        addParam() {
            if (!this.currentRequest.params) {
                this.$set(this.currentRequest, 'params', {});
            }
            this.currentRequest.params[''] = '';
        },

        deleteParam(key) {
            delete this.currentRequest.params[key];
        },

        // ============= 请求发送 =============
        async sendRequest() {
            /**
             * 发送 HTTP 请求
             * 
             * 步骤：
             * 1. 验证请求信息完整性
             * 2. 解析请求体（JSON）
             * 3. 发送到后端 /api/send 端点
             * 4. 处理响应和错误
             * 5. 显示结果给用户
             */
            
            // 参数验证
            if (!this.currentRequest) {
                this.showNotification('请先选择或创建一个请求', 'warning', 'fas fa-exclamation-triangle');
                return;
            }
            
            if (!this.currentRequest.url) {
                this.showNotification('请先填写 URL', 'warning', 'fas fa-exclamation-triangle');
                return;
            }
            
            if (!this.selectedEnvironment && this.currentRequest.url.includes('{{')) {
                this.showNotification('URL 中包含环境变量，请先选择环境', 'warning', 'fas fa-exclamation-triangle');
                return;
            }

            try {
                this.loading = true;
                this.requestTab = 'response';
                this.currentResponse = null;
                
                // 显示发送中的提示
                this.showNotification('📤 正在发送请求...', 'info', 'fas fa-paper-plane');

                // 解析请求体（支持 JSON 和纯文本）
                let body = null;
                if (this.currentRequest.bodyText) {
                    try {
                        body = JSON.parse(this.currentRequest.bodyText);
                    } catch (e) {
                        // 如果不是有效 JSON，当作纯文本发送
                        body = this.currentRequest.bodyText;
                    }
                }

                // 构建请求
                const requestData = {
                    method: this.currentRequest.method,
                    url: this.currentRequest.url,
                    headers: this.currentRequest.headers || {},
                    body: body,
                    params: this.currentRequest.params || {},
                    environment: this.selectedEnvironment
                };
                
                console.log('📤 发送请求:', requestData);

                // 发送到后端
                const response = await fetch('/api/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });

                const result = await response.json();
                console.log('📥 收到响应:', result);

                if (result.success) {
                    this.currentResponse = result.response;
                    
                    // 根据状态码显示不同的通知
                    const statusCode = result.response.status_code;
                    let message = `✅ 请求成功 (${statusCode})`;
                    let type = 'success';
                    
                    if (statusCode >= 400) {
                        message = `⚠️ 请求返回 ${statusCode}`;
                        type = 'warning';
                    }
                    
                    if (statusCode >= 500) {
                        message = `❌ 服务器错误 ${statusCode}`;
                        type = 'error';
                    }
                    
                    this.showNotification(message, type);
                } else {
                    // 后端返回错误
                    this.showNotification(
                        `❌ 请求失败: ${result.error}`,
                        'error',
                        'fas fa-exclamation-circle'
                    );
                }
            } catch (error) {
                console.error('❌ 发送请求失败:', error);
                this.showNotification(
                    `网络错误: ${error.message}`,
                    'error',
                    'fas fa-times-circle'
                );
            } finally {
                this.loading = false;
            }
        },

        // ============= 测试运行 =============
        async runCollection(collectionId) {
            try {
                this.loading = true;
                const response = await fetch('/api/run-tests', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ collection_id: collectionId })
                });

                const result = await response.json();

                if (result.success) {
                    this.showNotification('测试运行完成，请查看报告', 'success');
                    await this.loadReports();
                } else {
                    this.showNotification('测试运行失败', 'error', 'fas fa-exclamation-circle');
                    console.error('Test output:', result.output);
                    console.error('Test errors:', result.errors);
                }
            } catch (error) {
                console.error('Error running tests:', error);
                this.showNotification('运行测试失败', 'error', 'fas fa-exclamation-circle');
            } finally {
                this.loading = false;
            }
        },

        // ============= 报告管理 =============
        async loadReports() {
            try {
                const response = await fetch('/api/reports');
                this.reports = await response.json();
            } catch (error) {
                console.error('Error loading reports:', error);
            }
        },

        refreshReports() {
            this.loadReports();
            this.showNotification('报告已刷新', 'info', 'fas fa-info-circle');
        }
    }
}).mount('#app');
