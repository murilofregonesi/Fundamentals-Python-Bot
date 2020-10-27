# -*- coding: utf-8 -*-
"""
Fundamentus Scraper

@input: Target Symbol (string)
@output: Market Data (DataFrame)

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

def ScrapMarketData(sym):

    #%% Fundamentus Access
    
    import bs4 as bs
    from urllib.request import Request, urlopen
    
    fund_url = 'https://fundamentus.com.br/'
    tgt_url = 'detalhes.php?papel='
    
    # Use an HTTP client to get the document behind the URL
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request((fund_url + tgt_url + sym),headers=hdr)
    doc = urlopen(req)
    soup_tgt = bs.BeautifulSoup(doc,'lxml') # HTML doc data structure
    
    #%% Market Access
    
    # Scrap Target Page
    tables = soup_tgt.find_all('table') # Tables
    for iTb, table in enumerate(tables):
        
        trs = table.find_all('tr') # Lines
        for iTr, tr in enumerate(trs):
            
            tds = tr.find_all('td') # Columns
            for iTd, td in enumerate(tds):
                
                if(td.text == '?Setor'):
                    href = str(tds[iTd + 1].a).replace('"',' ').split()[2]
                    print('\nSector \'{}\', number {}'.format(tds[iTd + 1].text,href[href.find('=')+1:len(href)]))
                    
    req = Request((fund_url + href),headers=hdr)
    doc = urlopen(req)
    soup_mkt = bs.BeautifulSoup(doc,'lxml') # HTML doc data structure
                
    #%% Market Scrap
    
    import pandas as pd
    
    ths = soup_mkt.table.find_all('th') # HTML table columns
    df_columns = [th.text for th in ths] # Get table columns text
    
    df_mkt = pd.DataFrame() # Market DataFrame
    
    trs = soup_mkt.table.tbody.find_all('tr') # Table content lines
    for iTr, tr in enumerate(trs):
        
        tds = trs[iTr].find_all('td') # Columns per line
        tmp_td = [td.text for td in tds] # Columns content list
        
        # Construct market DataFrame
        df_mkt = pd.concat([df_mkt, pd.DataFrame(tmp_td).transpose()], ignore_index=True)
    
    df_mkt.columns = df_columns # Label columns
    df_mkt.set_index('Papel',inplace=True) # 'Papel' as index
    
    # Prepare Data for Modeling
    for col in df_mkt.columns:
        
        df_mkt[col] = df_mkt[col].str.replace('.','')
        df_mkt[col] = df_mkt[col].str.replace(',','.')
        df_mkt[col] = df_mkt[col].str.replace('%','')
        
        df_mkt[col] = df_mkt[col].astype(float)
        
    totCompanies = df_mkt.shape[0]
    print('Total companies: {}'.format(totCompanies))
    
    if totCompanies > 3:
        return df_mkt
    else:
        return -1;
