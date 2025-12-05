import React from 'react';
export default function Message({m}) {
  const cls = m.from==='user' ? 'text-end' : 'text-start';
  const badge = m.from==='user' ? 'bg-primary' : 'bg-secondary';
  return (
    <div className={`mb-2 ${cls}`}>
      <span className={`badge ${badge}`}>{m.from}</span>
      <div className='mt-1'>{m.text}</div>
    </div>
  );
}
