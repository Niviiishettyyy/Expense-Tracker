const express = require('express');
const cors = require('cors');
const path = require('path');
const Database = require('better-sqlite3');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public'))); // serve frontend

const db = new Database('data.db');

// ✅ Create table if not exists (includes mood column)
db.exec(`
CREATE TABLE IF NOT EXISTS expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  amount REAL NOT NULL,
  category TEXT NOT NULL,
  note TEXT,
  mood TEXT
);
`);

// ✅ Ensure mood column exists even if table was created earlier without it
try {
  db.prepare("ALTER TABLE expenses ADD COLUMN mood TEXT;").run();
} catch (err) {
  // Ignore error if column already exists
}

// Get all expenses
app.get('/api/expenses', (req, res) => {
  const rows = db
    .prepare('SELECT id, date, amount, category, note, mood FROM expenses ORDER BY date DESC')
    .all();
  res.json(rows);
});

// Add expense
app.post('/api/expenses', (req, res) => {
  const { date, amount, category, note, mood } = req.body;
  if (!date || !amount || !category) {
    return res.status(400).json({ error: 'Missing fields' });
  }

  const stmt = db.prepare(
    'INSERT INTO expenses (date, amount, category, note, mood) VALUES (?, ?, ?, ?, ?)'
  );
  const info = stmt.run(date, amount, category, note, mood);

  const row = db
    .prepare('SELECT id, date, amount, category, note, mood FROM expenses WHERE id=?')
    .get(info.lastInsertRowid);
  res.status(201).json(row);
});

// Delete expense
app.delete('/api/expenses/:id', (req, res) => {
  db.prepare('DELETE FROM expenses WHERE id=?').run(req.params.id);
  res.json({ ok: true });
});

app.listen(3000, () => console.log('Server running at http://localhost:3000'));
  