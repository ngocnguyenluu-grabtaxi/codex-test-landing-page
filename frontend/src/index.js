import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [stocks, setStocks] = useState([]);
  const [search, setSearch] = useState('');
  const [newSymbol, setNewSymbol] = useState('');
  const [currency, setCurrency] = useState('USD');
  const [prices, setPrices] = useState({});

  const fetchStocks = async (q = '') => {
    const params = q ? `?search=${encodeURIComponent(q)}` : '';
    const res = await fetch(`/api/watchlist${params}`);
    const data = await res.json();
    setStocks(data.watchlist);
  };

  useEffect(() => {
    fetchStocks('');
  }, []);

  useEffect(() => {
    async function loadPrices() {
      const priceData = {};
      for (const sym of stocks) {
        const res = await fetch(`/api/price/${sym}?currency=${currency}`);
        const data = await res.json();
        priceData[sym] = data.price;
      }
      setPrices(priceData);
    }
    if (stocks.length) {
      loadPrices();
    }
  }, [stocks, currency]);

  const addStock = async (e) => {
    e.preventDefault();
    if (!newSymbol) return;
    await fetch(`/api/watchlist?symbol=${encodeURIComponent(newSymbol)}`, { method: 'POST' });
    setNewSymbol('');
    fetchStocks(search);
  };

  const removeStock = async (symbol) => {
    await fetch(`/api/watchlist/${symbol}`, { method: 'DELETE' });
    fetchStocks(search);
  };

  return (
    <div>
      <h1>Stock Watchlist</h1>
      <form onSubmit={addStock}>
        <input value={newSymbol} onChange={(e) => setNewSymbol(e.target.value)} placeholder="Symbol" />
        <button type="submit">Add</button>
      </form>
      <div>
        <input value={search} onChange={(e) => { setSearch(e.target.value); fetchStocks(e.target.value); }} placeholder="Search" />
        <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="JPY">JPY</option>
          <option value="SGD">SGD</option>
        </select>
      </div>
      <ul>
        {stocks.map((s) => (
          <li key={s}>
            {s} - {prices[s] === undefined ? '...' : `${prices[s]} ${currency}`}
            <button onClick={() => removeStock(s)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
