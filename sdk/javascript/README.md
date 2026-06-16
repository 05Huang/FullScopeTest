# FullScopeTest JavaScript SDK

## Installation

```bash
npm install @fullscopetest/sdk
```

## Usage

```typescript
import { FullScopeTestClient } from '@fullscopetest/sdk';

const client = new FullScopeTestClient({
  baseUrl: 'https://api.fullscopetest.com',
  apiToken: 'fst_xxx',
});

// Run tests
const result = await client.runTests({ projectId: 1, testType: 'api' });
console.log(`Pass rate: ${result.passed}/${result.total}`);
```
