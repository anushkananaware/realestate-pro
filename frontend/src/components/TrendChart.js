import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer } from 'recharts';
export default function TrendChart({data,multi}) {
  if(!data) return null;
  if(multi){
    // data: array of {area, chart}
    const all = {};
    data.forEach(a=>{
      if(!a.chart) return;
      a.chart.years.forEach((y,i)=>{
        if(!all[y]) all[y] = { year:y };
        all[y][`${a.area}_price`] = a.chart.price[i];
        all[y][`${a.area}_demand`] = a.chart.demand[i];
      });
    });
    const chartData = Object.values(all).sort((a,b)=>a.year-b.year);
    const keys = Object.keys(chartData[0]||{}).filter(k=>k!=='year');
    return (
      <ResponsiveContainer width='100%' height={300}>
        <LineChart data={chartData}>
          <XAxis dataKey='year'/>
          <YAxis/>
          <Tooltip/>
          <CartesianGrid strokeDasharray='5 5'/>
          {keys.map((k,i)=>(<Line key={k} dataKey={k} stroke={['#8884d8','#82ca9d','#ff7300','#387908','#ff0000'][i%5]} />))}
        </LineChart>
      </ResponsiveContainer>
    );
  } else {
    return (
      <ResponsiveContainer width='100%' height={300}>
        <LineChart data={data}>
          <XAxis dataKey='year'/>
          <YAxis/>
          <Tooltip/>
          <Legend />
          <CartesianGrid strokeDasharray='5 5'/>
          <Line dataKey='price' name='Price' />
          <Line dataKey='demand' name='Demand' />
        </LineChart>
      </ResponsiveContainer>
    );
  }
}
