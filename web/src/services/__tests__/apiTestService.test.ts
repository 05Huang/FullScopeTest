import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("../api", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

import { getCollections, createCollection, updateCollection, deleteCollection, getCases, createCase, runCase } from "../apiTestService"
import api from "../api"

describe("apiTestService", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe("collections", () => {
    it("getCollections should call GET /api-test/collections", async () => {
      vi.mocked(api.get).mockResolvedValue({ code: 200, data: [], message: "ok", timestamp: "" })
      await getCollections(1)
      expect(api.get).toHaveBeenCalledWith("/api-test/collections", { params: { project_id: 1 } })
    })

    it("createCollection should call POST with collection data", async () => {
      vi.mocked(api.post).mockResolvedValue({ code: 200, data: { id: 1 }, message: "ok", timestamp: "" })
      await createCollection({ name: "Smoke", description: "smoke tests" })
      expect(api.post).toHaveBeenCalledWith("/api-test/collections", { name: "Smoke", description: "smoke tests" })
    })

    it("updateCollection should call PUT /api-test/collections/:id", async () => {
      vi.mocked(api.put).mockResolvedValue({ code: 200, data: {}, message: "ok", timestamp: "" })
      await updateCollection(5, { name: "Updated" })
      expect(api.put).toHaveBeenCalledWith("/api-test/collections/5", { name: "Updated" })
    })

    it("deleteCollection should call DELETE /api-test/collections/:id", async () => {
      vi.mocked(api.delete).mockResolvedValue({ code: 200, data: null, message: "ok", timestamp: "" })
      await deleteCollection(3)
      expect(api.delete).toHaveBeenCalledWith("/api-test/collections/3")
    })
  })

  describe("cases", () => {
    it("getCases should call GET /api-test/cases", async () => {
      vi.mocked(api.get).mockResolvedValue({ code: 200, data: [], message: "ok", timestamp: "" })
      await getCases({ collection_id: 2 })
      expect(api.get).toHaveBeenCalledWith("/api-test/cases", { params: { collection_id: 2 } })
    })

    it("createCase should call POST /api-test/cases", async () => {
      vi.mocked(api.post).mockResolvedValue({ code: 200, data: { id: 10 }, message: "ok", timestamp: "" })
      const payload = { name: "Login Test", method: "POST" as const, url: "https://httpbin.org/post", collection_id: 1 }
      await createCase(payload)
      expect(api.post).toHaveBeenCalledWith("/api-test/cases", payload)
    })

    it("runCase should call POST /api-test/cases/:id/run", async () => {
      vi.mocked(api.post).mockResolvedValue({ code: 200, data: { result: "success" }, message: "ok", timestamp: "" })
      await runCase(10)
      expect(api.post).toHaveBeenCalledWith("/api-test/cases/10/run", null, expect.objectContaining({}))
    })
  })
})
