const BASE_URL = 'https://fastapi-get-started-gokul-n2w8.vercel.app'
 
async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Request failed')
  }
  // 204 No Content – return null
  if (res.status === 204) return null
  return res.json()
}

/** Fetch all tasks from the backend */
export const fetchTasks = () => request('/tasks')

/** Create a new task.
 * @param {{ text: string, priority: string, category: string, due: string|null }} data
 */
export const createTask = (data) =>
  request('/tasks', { method: 'POST', body: JSON.stringify(data) })

/** Partially update a task (text / done / priority / category / due).
 * @param {string} id
 * @param {object} updates
 */
export const updateTask = (id, updates) =>
  request(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(updates) })

/** Delete a task by id */
export const deleteTask = (id) =>
  request(`/tasks/${id}`, { method: 'DELETE' })
