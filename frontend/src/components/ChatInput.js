import React, {useState} from 'react';
export default function ChatInput({onSubmit}) {
  const [text,setText]=useState('');
  const send=()=>{ if(!text.trim()) return; onSubmit(text.trim()); setText(''); };
  return (
    <div className='d-flex'>
      <input value={text} onChange={e=>setText(e.target.value)} className='form-control' placeholder='E.g., Analyze Wakad or Compare Aundh and Wakad' />
      <button className='btn btn-primary ms-2' onClick={send}>Send</button>
    </div>
  );
}
