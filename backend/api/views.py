import os, io
import pandas as pd
import numpy as np
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from .utils import extract_areas, fuzzy_match
import openai, logging

# Optional OpenAI integration: requires OPENAI_API_KEY in env
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

BASE = settings.BASE_DIR
DATA_PATH = os.path.join(BASE, 'dataset.xlsx')

_df_cache = None
def load_dataset():
    global _df_cache
    if _df_cache is None:
        if os.path.exists(DATA_PATH):
            _df_cache = pd.read_excel(DATA_PATH)
        else:
            # sample data
            data = {'Year':[2022,2023,2024,2022,2023,2024],
                    'Area':['Wakad','Wakad','Wakad','Aundh','Aundh','Aundh'],
                    'Price':[100,110,125,200,220,240],
                    'Demand':[50,70,90,40,50,60],
                    'Size':[500,520,530,600,610,620]}
            _df_cache = pd.DataFrame(data)
    return _df_cache.copy()

def _filter_by_area(df, area):
    mask = df['Area'].astype(str).str.contains(area, case=False, na=False)
    return df[mask]

def _mock_summary(area, df_area):
    yrs = sorted(df_area['Year'].unique())
    if len(yrs) >= 2:
        first = df_area[df_area['Year'] == yrs[0]]['Price'].mean()
        last = df_area[df_area['Year'] == yrs[-1]]['Price'].mean()
        growth = ((last - first) / first) * 100 if first else 0
        demand_trend = "increasing" if df_area.groupby('Year')['Demand'].mean().diff().fillna(0).sum() > 0 else "decreasing or flat"
        summary = f"{area}: Price changed by {growth:.1f}% from {yrs[0]} to {yrs[-1]}. Demand is {demand_trend}."
    else:
        summary = f"{area}: Not enough yearly data for trend summary."
    return summary

def _openai_summary(area, df_area):
    # build concise prompt
    try:
        rows = df_area.sort_values('Year').to_dict(orient='records')
        prompt = f"Provide a short (2-3 sentence) real-estate summary for '{area}' given rows: {rows}\nFocus on price growth and demand trend."
        resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}], max_tokens=200)
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logging.exception('OpenAI failed')
        return _mock_summary(area, df_area)

@api_view(['POST'])
def analyze(request):
    query = request.data.get('query','')
    areas = extract_areas(query)
    if not areas:
        return JsonResponse({'error':'No area detected in query.'}, status=400)
    df = load_dataset()
    # fuzzy choices from dataset unique areas
    choices = df['Area'].astype(str).unique().tolist()
    primary = areas[0]
    match = fuzzy_match(primary, choices) or primary
    filtered = _filter_by_area(df, match)
    if filtered.empty:
        return JsonResponse({'error':f'No data found for area: {primary}'}, status=404)
    agg = filtered.groupby('Year').agg({'Price':'mean','Demand':'mean'}).reset_index().sort_values('Year')
    chart = {'years': list(agg['Year'].astype(int)), 'price': list(np.round(agg['Price'],2)), 'demand': list(np.round(agg['Demand'],2))}
    # OpenAI summary if key present, else mock
    if OPENAI_KEY:
        summary = _openai_summary(match, filtered)
    else:
        summary = _mock_summary(match, filtered)
    table = filtered.to_dict(orient='records')
    return JsonResponse({'summary':summary,'chart':chart,'table':table})

@api_view(['POST'])
def compare(request):
    query = request.data.get('query','')
    areas = extract_areas(query)
    if not areas or len(areas)<2:
        return JsonResponse({'error':'Provide at least two areas to compare'}, status=400)
    df = load_dataset()
    choices = df['Area'].astype(str).unique().tolist()
    response = {'areas':[]}
    for a in areas:
        match = fuzzy_match(a, choices) or a
        filtered = _filter_by_area(df, match)
        if filtered.empty:
            response['areas'].append({'area':a,'error':'No data'})
            continue
        agg = filtered.groupby('Year').agg({'Price':'mean','Demand':'mean'}).reset_index().sort_values('Year')
        response['areas'].append({'area':match,'chart':{'years':list(agg['Year'].astype(int)),'price':list(np.round(agg['Price'],2)),'demand':list(np.round(agg['Demand'],2))}})
    return JsonResponse(response)

@api_view(['POST'])
def upload_dataset(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error':'No file uploaded'}, status=400)
    f = request.FILES['file']
    with open(DATA_PATH, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    global _df_cache
    _df_cache = None
    return JsonResponse({'message':'Uploaded'})

@api_view(['POST'])
def download_filtered(request):
    area = request.data.get('area')
    if not area:
        return JsonResponse({'error':'Provide area'}, status=400)
    df = load_dataset()
    filtered = _filter_by_area(df, area)
    if filtered.empty:
        return JsonResponse({'error':'No data for area'}, status=404)
    csv_io = io.StringIO()
    filtered.to_csv(csv_io, index=False)
    csv_io.seek(0)
    resp = HttpResponse(csv_io.read(), content_type='text/csv')
    resp['Content-Disposition'] = f'attachment; filename="{area}_data.csv"'
    return resp
