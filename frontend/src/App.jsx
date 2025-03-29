import React from 'react';
import './App.css';
import FruitList from './components/Fruits';  // Make sure the import path is correct

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Fruit Management App</h1>
      </header>
      <main>
        <FruitList /> {/* Ensure that this is being rendered */}
      </main>
    </div>
  );
};

export default App;
