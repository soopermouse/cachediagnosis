// cachemed/web/pages/index.js
import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Home() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get('http://localhost:5000/health')
      .then(response => {
        setHealth(response.data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching health:', error)
        setLoading(false)
      })
  }, [])

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Cachemed Dashboard</h1>

      {loading ? (
        <p>Loading...</p>
      ) : health ? (
        <div style={{ background: '#f0f0f0', padding: '1rem', borderRadius: '4px' }}>
          <h2>API Status</h2>
          <p><strong>Status:</strong> {health.status}</p>
          <p><strong>Version:</strong> {health.version}</p>
          <p><strong>Timestamp:</strong> {health.timestamp}</p>
        </div>
      ) : (
        <p style={{ color: 'red' }}>Could not connect to API</p>
      )}
    </div>
  )
}