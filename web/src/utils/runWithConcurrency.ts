export async function runWithConcurrency<T, R>(
  items: T[],
  concurrency: number,
  task: (item: T, index: number) => Promise<R>
): Promise<R[]> {
  if (items.length === 0) {
    return []
  }

  const results: R[] = new Array(items.length)
  const workerCount = Math.max(1, Math.min(concurrency, items.length))
  let cursor = 0

  const workers = Array.from({ length: workerCount }, async () => {
    while (true) {
      const index = cursor
      cursor += 1
      if (index >= items.length) {
        break
      }
      results[index] = await task(items[index], index)
    }
  })

  await Promise.all(workers)
  return results
}
