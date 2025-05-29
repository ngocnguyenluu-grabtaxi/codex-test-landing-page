import React from 'react';
import ReactDOM from 'react-dom/client';
import TestUtils from 'react-dom/test-utils';
import App from './index';

describe('App component', () => {
  beforeEach(() => {
    global.fetch = jest.fn((url, options) => {
      if (url.startsWith('/api/watchlist')) {
        return Promise.resolve({ json: () => Promise.resolve({ watchlist: [] }) });
      }
      return Promise.resolve({ json: () => Promise.resolve({ price: 0 }) });
    });
  });

  test('renders heading', () => {
    const div = document.createElement('div');
    const root = ReactDOM.createRoot(div);
    TestUtils.act(() => {
      root.render(<App />);
    });
    expect(div.querySelector('h1').textContent).toBe('Stock Watchlist');
  });

  test('adds a symbol', async () => {
    const div = document.createElement('div');
    const root = ReactDOM.createRoot(div);
    await TestUtils.act(async () => {
      root.render(<App />);
    });
    const input = div.querySelector('input[placeholder="Symbol"]');
    const form = div.querySelector('form');
    await TestUtils.act(async () => {
      TestUtils.Simulate.change(input, { target: { value: 'AAPL' } });
    });
    await TestUtils.act(async () => {
      TestUtils.Simulate.submit(form);
    });
    expect(global.fetch).toHaveBeenCalledWith('/api/watchlist?symbol=AAPL', { method: 'POST' });
  });
});
