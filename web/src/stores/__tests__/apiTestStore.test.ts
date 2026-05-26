import { describe, it, expect, beforeEach } from 'vitest'
import { useApiTestStore } from '../apiTestStore'

describe('apiTestStore', () => {
  beforeEach(() => {
    // Reset store state
    useApiTestStore.setState({
      collections: [],
      cases: [],
      activeCollectionId: undefined,
      activeCaseId: undefined,
      activeCase: undefined,
      environments: [],
      selectedEnvId: undefined,
      loading: false,
      error: undefined,
    })
  })

  it('should have correct initial state', () => {
    const state = useApiTestStore.getState()
    expect(state.collections).toEqual([])
    expect(state.cases).toEqual([])
    expect(state.activeCollectionId).toBeUndefined()
    expect(state.activeCaseId).toBeUndefined()
    expect(state.loading).toBe(false)
  })

  it('should set collections', () => {
    const collections = [
      { id: 1, name: 'Collection 1', project_id: 1, created_at: '', updated_at: '' },
      { id: 2, name: 'Collection 2', project_id: 1, created_at: '', updated_at: '' },
    ]

    useApiTestStore.getState().setCollections(collections)
    expect(useApiTestStore.getState().collections).toEqual(collections)
  })

  it('should set active collection id', () => {
    useApiTestStore.getState().setActiveCollectionId(5)
    expect(useApiTestStore.getState().activeCollectionId).toBe(5)
  })

  it('should add case', () => {
    const testCase = {
      id: 1,
      name: 'Test Case',
      method: 'GET' as const,
      url: '/api/test',
      headers: {},
      params: {},
      body_type: 'json' as const,
      mock_enabled: false,
      created_at: '',
      updated_at: '',
    }

    useApiTestStore.getState().addCase(testCase)
    expect(useApiTestStore.getState().cases).toHaveLength(1)
    expect(useApiTestStore.getState().cases[0]).toEqual(testCase)
  })

  it('should update case', () => {
    const testCase = {
      id: 1,
      name: 'Original',
      method: 'GET' as const,
      url: '/api/test',
      headers: {},
      params: {},
      body_type: 'json' as const,
      mock_enabled: false,
      created_at: '',
      updated_at: '',
    }

    useApiTestStore.getState().addCase(testCase)
    useApiTestStore.getState().updateCase(1, { name: 'Updated', method: 'POST' })

    const updated = useApiTestStore.getState().cases[0]
    expect(updated.name).toBe('Updated')
    expect(updated.method).toBe('POST')
  })

  it('should remove case', () => {
    const cases = [
      {
        id: 1,
        name: 'Case 1',
        method: 'GET' as const,
        url: '/api/1',
        headers: {},
        params: {},
        body_type: 'json' as const,
        mock_enabled: false,
        created_at: '',
        updated_at: '',
      },
      {
        id: 2,
        name: 'Case 2',
        method: 'POST' as const,
        url: '/api/2',
        headers: {},
        params: {},
        body_type: 'json' as const,
        mock_enabled: false,
        created_at: '',
        updated_at: '',
      },
    ]

    useApiTestStore.setState({ cases })
    useApiTestStore.getState().removeCase(1)

    expect(useApiTestStore.getState().cases).toHaveLength(1)
    expect(useApiTestStore.getState().cases[0].id).toBe(2)
  })

  it('should set loading state', () => {
    useApiTestStore.getState().setLoading(true)
    expect(useApiTestStore.getState().loading).toBe(true)
  })

  it('should set error state', () => {
    useApiTestStore.getState().setError('Something went wrong')
    expect(useApiTestStore.getState().error).toBe('Something went wrong')
  })
})
