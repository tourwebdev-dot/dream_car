import { useState } from 'react'
import carsData from './mx5.json' 
import './App.css'

function App() {
  const [cars, setCars] = useState(carsData)

  return (
    <div className="container">
      <h1>🏎️ MX-5 Dream Tracker</h1>
      <p className="subtitle">Βρέθηκαν <strong>{cars.length}</strong> ευκαιρίες κάτω από 5.000€!</p>
      
      <div className="cars-grid">
        {cars.map((car, index) => (
          <div key={index} className="car-card">
            {/* ΝΕΟ: Εικόνα αυτοκινήτου */}
            <div className="card-image-wrapper">
              <img src={car.image} alt={car.title} className="car-image" />
            </div>
            
            <div className="card-content">
              <h2>{car.title}</h2>
              
              {/* ΝΕΟ: Χρονολογία & Χιλιόμετρα */}
              <div className="car-specs">
                <span className="spec-badge">📅 {car.year}</span>
                <span className="spec-badge">🛣️ {car.mileage}</span>
              </div>
              
              <p className="price">{car.price.toLocaleString('el-GR')} €</p>
              
              <a 
                href={car.link} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="btn"
              >
                Δες την αγγελία
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App