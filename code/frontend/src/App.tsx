import { useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || ''

interface AuthResponse {
  AccessToken: string
  IdToken: string
  RefreshToken: string
  ExpiresIn: number
  TokenType: string
}

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        let message = 'ログインに失敗しました'
        if (err.detail) {
          message = Array.isArray(err.detail) ? err.detail[0]?.msg ?? message : String(err.detail)
        } else if (err.message) {
          message = err.message
        }
        throw new Error(message)
      }

      const data: AuthResponse = await res.json()
      localStorage.setItem('accessToken', data.AccessToken)
      localStorage.setItem('idToken', data.IdToken)
      localStorage.setItem('refreshToken', data.RefreshToken)
      // TODO: 認証後にダッシュボードなどへ遷移
      window.location.reload()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ログインに失敗しました')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">microDDNS</h1>
        <p className="login-subtitle">サインインして続行</p>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">メールアドレス</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              autoComplete="email"
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">パスワード</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="current-password"
              required
              disabled={loading}
            />
          </div>
          {error && <p className="login-error">{error}</p>}
          <button type="submit" className="login-button" disabled={loading}>
            {loading ? 'ログイン中...' : 'ログイン'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
