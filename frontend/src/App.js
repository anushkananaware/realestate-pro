import React, {useState} from 'react';
import ChatInput from './components/ChatInput';
import Message from './components/Message';
import TrendChart from './components/TrendChart';
import { analyze, compare, upload, download } from './api';
import { saveAs } from 'file-saver';

export default function App(){
  const [messages,setMessages]=useState([]);
  const [chartData,setChartData]=useState(null);
  const [tableData,setTableData]=useState([]);
  const [compareData,setCompareData]=useState(null);

  const push = (m)=> setMessages(prev=>[...prev,m]);

  const handleSubmit = async (text) => {
    push({from:'user', text});
    if(/compare/i.test(text)){
      push({from:'bot', text:'Working on comparison...'});
      try{
        const res = await compare(text);
        setCompareData(res.areas || []);
        setChartData(null);
        setTableData([]);
        push({from:'bot', text:'Comparison ready.'});
      }catch(e){
        push({from:'bot', text:'Error during compare.'});
      }
      return;
    }
    push({from:'bot', text:'Analyzing...'});
    try{
      const res = await analyze(text);
      push({from:'bot', text: res.summary});
      const years = res.chart.years;
      const chart = years.map((y,i)=>({year:y, price:res.chart.price[i], demand:res.chart.demand[i]}));
      setChartData(chart);
      setTableData(res.table || []);
      setCompareData(null);
    }catch(e){
      push({from:'bot', text: 'Analysis failed.'});
    }
  };

  const handleUpload = async (ev) => {
    const f = ev.target.files[0];
    if(!f) return;
    push({from:'user', text:`Uploaded file ${f.name}`});
    const res = await upload(f);
    push({from:'bot', text: res.message || 'Uploaded'});
  };

  const handleDownload = async () => {
    const area = tableData?.[0]?.Area;
    if(!area){ alert('No area to download'); return; }
    const blob = await download(area);
    saveAs(blob, `${area}.csv`);
  };

  return (
    <div className='container my-4'>
      <h3>RealEstate Pro Chatbot</h3>
      <div className='card my-3'>
        <div className='card-body'>
          <ChatInput onSubmit={handleSubmit}/>
          <div className='mt-3'>
            <label className='btn btn-outline-secondary me-2'>
              Upload dataset <input type='file' hidden onChange={handleUpload}/>
            </label>
            <button className='btn btn-success' onClick={handleDownload}>Download CSV</button>
          </div>
        </div>
      </div>

      <div>
        {messages.map((m,i)=>(<Message key={i} m={m}/>))}
      </div>

      {compareData ? (
        <>
          <h5>Comparison Chart</h5>
          <TrendChart data={compareData} multi />
        </>
      ) : (
        <>
          {chartData && <>
            <h5>Trend Chart</h5>
            <TrendChart data={chartData} />
          </>}
          {tableData && tableData.length>0 && <>
            <h5 className='mt-3'>Filtered Table</h5>
            <div className='table-responsive'><table className='table table-striped'>
              <thead><tr>{Object.keys(tableData[0]).map(h=><th key={h}>{h}</th>)}</tr></thead>
              <tbody>{tableData.map((r,idx)=><tr key={idx}>{Object.keys(r).map(k=><td key={k}>{r[k]}</td>)}</tr>)}</tbody>
            </table></div>
          </>}
        </>
      )}
    </div>
  );
}
