// cachemed/web/components/Dashboard.js
import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Dashboard({ apiUrl = 'http://localhost:5000' }) {
  const [patients, setPatients] = useState([])
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [readings, setReadings] = useState([])
  const [prediction, setPrediction] = useState(null)

  const loadPatients = async () => {
    try {
      // This would need a real endpoint - for demo just showing structure
      console.log('Loading patients...')
    } catch (error) {
      console.error('Error loading patients:', error)
    }
  }

  const loadPatientReadings = async (patientId) => {
    try {
      const response = await axios.get(`${apiUrl}/api/biometrics/${patientId}`)
      setReadings(response.data.readings || [])
    } catch (error) {
      console.error('Error loading readings:', error)
    }
  }

  const generatePrediction = async (patientId) => {
    try {
      const response = await axios.post(`${apiUrl}/api/predict/${patientId}`)
      setPrediction(response.data.prediction)
    } catch (error) {
      console.error('Error generating prediction:', error)
    }
  }

  return (
    <div>
      <h2>Patient Dashboard</h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        <div>
          <h3>Patients</h3>
          <p>Patient list would go here</p>
        </div>

        <div>
          <h3>Readings</h3>
          {readings.length > 0 ? (
            <ul>
              {readings.slice(0, 5).map(r => (
                <li key={r.readingId}>
                  {r.readingType}: {JSON.stringify(r.value)}
                </li>
              ))}
            </ul>
          ) : (
            <p>No readings</p>
          )}

          {prediction && (
            <div style={{ marginTop: '2rem', padding: '1rem', background: '#e6f7ff' }}>
              <h4>Latest Prediction</h4>
              <p>Risk Level: {prediction.risk_level}</p>
              <p>Risk Score: {prediction.risk_score}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}