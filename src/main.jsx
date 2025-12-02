import React from 'react';
import ReactDOM from 'react-dom/client';
import BuilderDemo from './pages/BuilderDemo';

// Simple routing to render the builder demo
const App = () => {
  return (
    <BuilderDemo />
  );
};

// Create root and render app
const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);