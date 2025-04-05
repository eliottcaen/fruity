import React, { useState, useEffect } from 'react';
import api from "../api.js";
import AddFruitForm from './AddFruitForm';

const FruitList = () => {
  const [fruits, setFruits] = useState([]);
  const [selectedFruit, setSelectedFruit] = useState(null);
  useEffect(() => {
  console.log("🍌 selectedFruit changed:", selectedFruit);
}, [selectedFruit]);
  const [updatedName, setUpdatedName] = useState('');

  // Fetch fruits from backend
  const fetchFruits = async () => {
    try {
      const response = await api.get('/fruits');
      console.log("🔍 GET response:", response.data);
      setFruits(response.data.data);
    } catch (error) {
      console.error("Error fetching fruits", error);
    }
  };

  // Add a fruit
  const addFruit = async (fruitName) => {
    try {
      await api.post('/fruits', { name: fruitName });
      fetchFruits(); // Refresh the list
    } catch (error) {
      console.error("Error adding fruit", error);
    }
  };

const updateFruit = async () => {
  if (selectedFruit && updatedName) {
    try {
      const response = await api.put('http://localhost:8000/fruits', {
        id: selectedFruit.id,
        new_name: updatedName
      });
      fetchFruits(); // Refresh the list

      setUpdatedName('');
      setSelectedFruit(null);

      // Optionally show a confirmation message
    } catch (error) {
      console.error("Error updating fruit", error);
    }
  }
};

  useEffect(() => {
    fetchFruits(); // Fetch fruits on initial load
  }, []);

  return (
    <div>
      <h2>Fruits List</h2>
      <ul>
        {fruits.map((fruit, index) => (
          <li key={index}>
            {fruit.name}
            <button onClick={() => setSelectedFruit(fruit)}>Edit</button>
          </li>
        ))}
      </ul>

      {/* Add Fruit Form */}
      <AddFruitForm addFruit={addFruit} />

      {/* Update Fruit Form */}
      {selectedFruit && (
        <div>
          <h3>Update Fruit</h3>
          <input
            type="text"
            value={updatedName}
            onChange={(e) => setUpdatedName(e.target.value)}
            placeholder={`Update ${selectedFruit.name}`}
          />
          <button onClick={updateFruit}>Update</button>
        </div>
      )}
    </div>
  );
};

export default FruitList;
