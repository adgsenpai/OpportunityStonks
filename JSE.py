import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

START = "1990-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Opportunity Stonks App')

stocks = {
'PRX.JO':'Prosus N.V. ',
'ANH.JO':'Anheuser-Busch Inbev ',
'BTI.JO':'British American Tobacco ',
'GLN.JO':'Glencore plc ',
'CFR.JO':'Compagnie Fin Richemont ',
'BHP.JO':'BHP Group plc ',
'NPN.JO':'Naspers Limited - N ',
'AGL.JO':'Anglo American plc ',
'AMS.JO':'Anglo American Platinum Ltd ',
'FSR.JO':'Firstrand Limited ',
'MTN.JO':'MTN Group Limited ',
'VOD.JO':'Vodacom Group Limited ',
'SBK.JO':'Standard Bank Group ',
'CPI.JO':'Capitec Bank Holdings ',
'SOL.JO':'Sasol Limited ',
'S32.JO':'South32 Limited ',
'IMP.JO':'Impala Platinum Holdings Limited ',
'MNP.JO':'Mondi plc ',
'KIO.JO':'Kumba Iron Ore ',
'SSW.JO':'Sibanye Stillwater Limited ',
'ABG.JO':'Absa Group Limited ',
'GFI.JO':'Gold Fields Limited ',
'SLM.JO':'Sanlam Limited ',
'SHP.JO':'Shoprite Holdings Limited ',
'ANG.JO':'Anglogold Ashanti ',
'BID.JO':'Bid Corporation Limited ',
'DSY.JO':'Discovery Limited ',
'NED.JO':'Nedbank Group Limited ',
'APN.JO':'Aspen Pharmacare Holdings Limited ',
'PPH.JO':'Pepkor Holdings Limited ',
'NHM.JO':'Northam Platinum Limited ',
'RMI.JO':'Rand Merchant Investment Holdings ',
'CLS.JO':'Clicks Group Limited ',
'REM.JO':'Remgro Limited ',
'OMU.JO':'Old Mutual Limited ',
'NRP.JO':'Nepi Rockcastle plc ',
'BVT.JO':'Bidvest Group ',
'INP.JO':'Investec plc ',
'EXX.JO':'Exxaro Resources Limited ',
'RNI.JO':'Reinet Investments S.C.A. ',
'WHL.JO':'Woolworths Holdings Limited ',
'MCG.JO':'MultiChoice Group ',
'MRP.JO':'Mr Price Group ',
'GRT.JO':'Growthpoint Properties Limited ',
'ARI.JO':'African Rainbow Minerals ',
'MEI.JO':'Mediclinic International plc ',
'QLT.JO':'Quilter plc ',
'RBP.JO':'Royal Bafokeng Platinum Limited ',
'TFG.JO':'The Foschini Group ',
'DGH.JO':'Distell Group Holdings ',
'VVO.JO':'Vivo Energy plc ',
'HMN.JO':'Hammerson plc ',
'TBS.JO':'Tiger Brands Limited ',
'N91.JO':'Ninety One plc ',
'LHC.JO':'Life Healthcare Group ',
'TXT.JO':'Textainer Group Holdings ',
'HAR.JO':'Harmony Gold Mining Company ',
'SPP.JO':'Spar Group Limited ',
'TCP.JO':'Transaction Capital Ltd ',
'SRE.JO':'Sirius Real Estate ',
'SNT.JO':'Santam Limited ',
'CCO.JO':'Capital & Counties Properties plc ',
'DCP.JO':'Dis-Chem Pharmacies Limited ',
'MSP.JO':'MAS Real Estate Inc ',
'MTM.JO':'Momentum Metropolitan Holdings ',
'LBH.JO':'Liberty Holdings Limited ',
'INL.JO':'Investec Limited ',
'APH.JO':'Alphamin Resources Corporation ',
'BAW.JO':'Barloworld Limited ',
'PIK.JO':'Pick n Pay Stores Limited ',
'AVI.JO':'AVI Limited ',
'TKG.JO':'Telkom SA Limited ',
'RDF.JO':'Redefine Properties Limited ',
'RES.JO':'Resilient REIT Limited ',
'SAP.JO':'Sappi Limited ',
'TRU.JO':'Truworths International Limited ',
'BYI.JO':'Bytes Technology Group ',
'MTH.JO':'Motus Holdings Limited ',
'SNH.JO':'Steinhoff International Holdings NV ',
'NTC.JO':'Netcare Limited ',
'ITE.JO':'Italtile Limited ',
'KST.JO':'PSG Konsult Limited ',
'PSG.JO':'PSG Group Limited ',
'CML.JO':'Coronation Fund Managers ',
'KRO.JO':'Karooooo Ltd ',
'NY1.JO':'Ninety One Limited ',
'EQU.JO':'Equites Property Fund Limited ',
'FFA.JO':'Fortress REIT Limited - A ',
'LTE.JO':'Lighthouse Capital Limited ',
'RCL.JO':'RCL Foods Limited ',
'IPL.JO':'Imperial Logistics Limited ',
'MSM.JO':'Massmart Holdings Limited ',
'AFE.JO':'AECI Limited ',
'HYP.JO':'Hyprop Investments Limited ',
'SPG.JO':'Super Group Limited ',
'TGA.JO':'Thungela Resources Limited ',
'IAP.JO':'Irongate Group ',
'TSG.JO':'Tsogo Sun Gaming ',
'ACL.JO':'ArcelorMittal South Africa Limited ',
'VKE.JO':'Vukile Property Fund Limited ',
'KAP.JO':'Kap Industrial Holdings Limited ',
'STP.JO':'Stenprop Limited ',
'DRD.JO':'DRDGOLD Limited ',
'JSE.JO':'JSE Limited ',
'IPF.JO':'Investec Property Fund Limited ',
'OMN.JO':'Omnia Holdings Limited ',
'EPP.JO':'EPP N.V. ',
'GTC.JO':'Globe Trade Centre S.A. ',
'AIP.JO':'Adcock Ingram Holdings ',
'AIL.JO':'African Rainbow Capital Investments ',
'RLO.JO':'Reunert Limited ',
'ADH.JO':'ADvTECH Limited ',
'AFT.JO':'Afrimat Limited ',
'PAN.JO':'Pan African Resources plc ',
'COH.JO':'Curro Holdings Limited ',
'DTC.JO':'Datatec Limited ',
'JBL.JO':'Jubilee Metals Group Plc ',
'OCE.JO':'Oceana Group Limited ',
'THA.JO':'Tharisa plc ',
'PPC.JO':'PPC Limited ',
'ARL.JO':'Astral Foods Limited ',
'CSB.JO':'Cashbuild Limited ',
'FBR.JO':'Famous Brands Limited ',
'SSS.JO':'Stor-Age Property REIT ',
'SUI.JO':'Sun International Limited ',
'WBO.JO':'Wilson Bayly Holmes-Ovcon Limited ',
'RBX.JO':'Raubex Group Limited ',
'HCI.JO':'Hosken Consolidated Investments Limited ',
'MUR.JO':'Murray & Roberts Holdings Limited ',
'SAC.JO':'SA Corporate Real Estate Fund Limited ',
'BAT.JO':'Brait SE ',
'ATT.JO':'Attacq Limited ',
'MTA.JO':'Metair Investments Limited ',
'AFH.JO':'Alexander Forbes Group Holdings Limited ',
'RAV.JO':'Raven Property Group Limited ',
'EMI.JO':'Emira Property Fund Limited ',
'MPT.JO':'Mpact Limited ',
'ZED.JO':'Zeder Investments Limited ',
'GSH.JO':'Grindrod Shipping Holdings ',
'TGO.JO':'Tsogo Sun Hotels ',
'MED.JO':'Middle East Diamond Resources Limited ',
'SHG.JO':'Sea Harvest Group Limited ',
'BLU.JO':'Blue Label Telecoms ',
'L2D.JO':'Liberty Two Degrees Limited ',
'REN.JO':'Renergen Limited ',
'MIX.JO':'Mix Telematics Limited ',
'HDC.JO':'Hudaco Industries Limited ',
'LBR.JO':'Libstar Holdings Limited ',
'GML.JO':'Gemfields Group Limited ',
'L4L.JO':'Long4Life Limited ',
'KAL.JO':'Kaap Agri Limited ',
'NT1.JO':'Net 1 UEPS Technologies Inc ',
'FFB.JO':'Fortress REIT Limited - B ',
'MTN.JO':'F,MTN Zakhele Futhi ',
'PPE.JO':'Purple Group Limited ',
'CLI.JO':'Clientele Limited ',
'AHB.JO':'Arrowhead Properties Limited B ',
'RFG.JO':'RFG Holdings Limited ',
'AEG.JO':'Aveng Group Limited ',
'MRF.JO':'Merafe Resources Limited ',
'GND.JO':'Grindrod Limited ',
'AEL.JO':'Allied Electronics Corporation ',
'CAT.JO':'Caxton & CTP Publishers & Printers Limited ',
'EXP.JO':'Exemplar Reitail Limited ',
'CLH.JO':'City Lodge Hotels Limited ',
'IVT.JO':'Invicta Holdings Limited ',
'SCD.JO':'Schroder European Real Estate Investment Trust ',
'LEW.JO':'Lewis Group Limited ',
'ACT.JO':'Afrocentric Investment Corp ',
'SDO.JO':'STADIO Holdings Limited ',
'HET.JO':'Heriot REIT Limited ',
'HIL.JO':'Homechoice International plc ',
'TDH.JO':'Tradehold Limited ',
'WEZ.JO':'Wesizwe Platinum Limited ',
'OAO.JO':'Oando PLC ',
'NPK.JO':'Nampak Limited ',
'CTA.JO':'Capital Appreciation Limited ',
'SYG.JO':'Sygnia Limited ',
'YYL.JO':'EE,YeboYethu (RF) Limited ',
'DIA.JO':'Dipula Income Fund Limited A ',
'SBP.JO':'Sabvest Capital Limited ',
'OCT.JO':'Octodec Investments Limited ',
'RMH.JO':'RMB Holdings Limited ',
'FVT.JO':'Fairvest Property Holdings ',
'CRP.JO':'Capital & Regional plc ',
'AVV.JO':'Alviva Holdings Limited ',
'SUR.JO':'Spur Corporation Limited ',
'DRA.JO':'DRA Global Limited ',
'CMH.JO':'Combined Motor Holdings Limited ',
'TTO.JO':'Trustco Group Holdings Limited ',
'SEA.JO':'Spear Reit Limited ',
'MDI.JO':'Master Drilling Group Limited ',
'ARH.JO':'ARB Holdings Limited ',
'BWN.JO':'Balwin Properties Limited ',
'ACS.JO':'Acsion Limited ',
'BRN.JO':'Brimstone Investment Corporation - N Shares ',
'SAR.JO':'Safari Investments RSA Limited ',
'ENX.JO':'enX Group Limited ',
'EMN.JO':'E Media Holdings Limited - N Shares ',
'HLM.JO':'Hulamin Limited ',
'MFL.JO':'Metrofile Holdings Limited ',
'EPE.JO':'EPE Capital Partners Limited ',
'OAS.JO':'Oasis Crescent Property Fund ',
'ORN.JO':'Orion Minerals Limited ',
'UPL.JO':'Universal Partners Limited ',
'TEX.JO':'Texton Property Fund Limited ',
'GPL.JO':'Grand Parade Investments Limited ',
'BEL.JO':'Bell Equipment Limited ',
'AYO.JO':'AYO Tech Solutions ',
'YRK.JO':'York Timber Holdings Limited ',
'ILU.JO':'Indluplace Properties Limited ',
'DIB.JO':'Dipula Income Fund Limited B ',
'HPR.JO':'Hosken Passenger Logistics and Rail Limited ',
'APF.JO':'Accelerate Property Fund Ltd ',
'QFH.JO':'Quantum Foods Holdings ',
'SOL.JO':'E1,Sasol Limited - BEE ',
'CHP.JO':'Choppies Enterprises Limited ',
'AHA.JO':'Arrowhead Properties Limited A ',
'PBG.JO':'PBT Group Limited ',
'SFN.JO':'Sasfin Holdings Limited ',
'EOH.JO':'EOH Holdings ',
'TRE.JO':'Trencor Limited ',
'TPF.JO':'Transcend Residential Property Fund Limited ',
'BCF.JO':'Bowler Metcalf Limited ',
'MST.JO':'Mustek Limited ',
'FGL.JO':'Finbond Group Limited ',
'DNB.JO':'Deneb Investments Limited ',
'SNV.JO':'Santova Limited ',
'NVS.JO':'Novus Holdings Limited ',
'MMP.JO':'Marshall Monteagle PLC ',
'WSL.JO':'Wescoal Holdings Limited ',
'OLG.JO':'Onelogix Group Limited ',
'TMT.JO':'Trematon Capital Investments Limited ',
'ART.JO':'Argent Industrial Limited ',
'DKR.JO':'Deutsche Konsum REIT-AG ',
'NWL.JO':'Nu-World Holdings Limited ',
'KP2.JO':'Kore Potash Plc ',
'ADR.JO':'Adcorp Holdings Limited ',
'TON.JO':'Tongaat Hulett Limited ',
'EPS.JO':'Eastern Platinum Limited ',
'HUG.JO':'Huge Group Limited ',
'CND.JO':'Conduit Capital Limited ',
'CKS.JO':'Crookes Brothers Limited ',
'TPC.JO':'Transpaco Limited ',
'CGR.JO':'Calgro M3 Holdings Limited ',
'ALH.JO':'Alaris Holdings Limited ',
'VUN.JO':'Vunani Limited ',
'SEP.JO':'Sephaku Holdings Limited ',
'NVE.JO':'Nvest Financial Holdings Limited ',
'AEE.JO':'African Equity Empowerment Investments ',
'DLT.JO':'Delta Property Fund Limited ',
'ISB.JO':'Insimbi Industrial Holdings Ltd ',
'ASC.JO':'Ascendis Health Limited ',
'RSG.JO':'Resource Generation Limited ',
'NRL.JO':'Newpark REIT Limited ',
'RHB.JO':'RH Bophelo Limited ',
'SOH.JO':'South Ocean Holdings ',
'WKF.JO':'Workforce Holdings Limited ',
'BUC.JO':'Buffalo Coal Corporation ',
'BIK.JO':'Brikor Limited ',
'TRL.JO':'Trellidor Holdings Limited ',
'SEB.JO':'Sebata Holdings Limited ',
'BAU.JO':'Bauba Resources Limited ',
'AME.JO':'African Media Entertainment ',
'EMH.JO':'E Media Holdings Limited ',
'AVL.JO':'Advanced Health Limited ',
'BRT.JO':'Brimstone Investment Corporation ',
'ARA.JO':'Astoria Investments Limited ',
'ETO.JO':'Etion Limited ',
'ELI.JO':'Ellies Holdings Limited ',
'LNF.JO':'London Finance & Investment Group Plc ',
'HUL.JO':'Hulisani Limited ',
'FSE.JO':'Firestone Energy Limited ',
'KBO.JO':'Kibo Energy PLC ',
'PFB.JO':'Premier Fishing and Brands ',
'REA.JO':'Rebosis Property Fund - A Shares ',
'RTN.JO':'Rex Trueform Group - N Shares ',
'CVW.JO':'Castleview Property Fund Limited ',
'REB.JO':'Rebosis Property Fund ',
'CMO.JO':'Chrometco Limited ',
'MCZ.JO':'MC Mining Limited ',
'CSG.JO':'CSG Holdings Limited ',
'ISA.JO':'ISA Holdings Limited ',
'4SI.JO':'4Sight Holdings Limited ',
'CGN.JO':'Cognition Holdings Limited ',
'PPR.JO':'Putprop Limited ',
'EEL.JO':'Efora Energy Limited ',
'LAB.JO':'Labat Africa Limited ',
'PMV.JO':'Primeserv Group Limited ',
'SSK.JO':'Stefanutti Stocks Holdings Limited ',
'EUZ.JO':'Europa Metals Limited ',
'RNG.JO':'Randgold And Exploration Company ',
'JSC.JO':'Jasco Electronics Holdings ',
'AON.JO':'African and Overseas Enterprises - N Shares ',
'TLM.JO':'TeleMasters Holdings Limited ',
'UAT.JO':'Union Atlantic Minerals Limited ',
'BSR.JO':'Basil Read Holdings Limited ',
'AHL.JO':'AH-Vest Limited ',
'HWA.JO':'Hwange Colliery Company Limited ',
'RTO.JO':'Rex Trueform Group ',
'SVB.JO':'SilverBridge Holdings Limited ',
'NCS.JO':'Nictus Limited ',
'PEM.JO':'Pembury Lifestyle Group ',
'CAC.JO':'CAFCA Limited ',
'PSV.JO':'PSV Holdings Limited ',
'ILE.JO':'Imbalie Beauty Limited ',
'MRI.JO':'Mine Restoration Investments Limited ',
'TAS.JO':'Taste Holdings Limited ',
'AOO.JO':'African and Overseas Enterprises Limited ',
'VIS.JO':'Visual International Holdings Limited ',
'ADW.JO':'African Dawn Capital ',
'ECS.JO':'Ecsponent Limited ',
'GLI.JO':'Go Life International Ltd ',
'WEA.JO':'WG Wearne Limited ',
'NFP.JO':'New Frontier Properties Limited ',
'NUT.JO':'Nutritional Holdings Limited ',
'ACZ.JO':'Arden Capital Limited ',
'PHM.JO':'Phumelela Gaming And Leisure Limited ',
'RPL.JO':'RDI REIT PLC ',
'ACE.JO':'Accentuate Limited ',
'RDI.JO':'Rockwell Diamonds Incorporated ',
'AFX.JO':'African Oxygen Limited ',
'ACG.JO':'Anchor Group Limited ',
'ALP.JO':'Atlantic Leaf Properties Limited ',
'TBG.JO':'Tiso Blackstar Group SE ',
'CTK.JO':'Cartrack Holdings ',
'UCP.JO':'Unicorn Capital Partners Limited ',
'VLE.JO':'Value Group Limited ',
'COM.JO':'Comair Limited ',
'CIL.JO':'Consolidated Infrastructure Group ',
'EFG.JO':'Efficient Group Limited ',
'ELR.JO':'ELB Group Limited ',
'ESR.JO':'Esor Limited ',
'FDP.JO':'Freedom Property Fund Limited ',
'GAI.JO':'Gaia Infrastructure Capital Limited ',
'GRF.JO':'Group Five Limited ',
'HPB.JO':'Hospitality Property Fund - B ',
'IDQ.JO':'Indequity Group Limited ',
'KDV.JO':'Kaydav Group Limited ',
'MZR.JO':'Mazor Group Limited ',
'MLE.JO':'Mettle Investments Limited ',
'MNK.JO':'Montauk Holdings Limited '
}

def format_func(option):
    return stocks[option]

selected_stock = st.selectbox('Select dataset for prediction', options=list(stocks.keys()), format_func=format_func)

n_years = st.slider('Years of prediction:', 1, 25)
period = n_years * 365


@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data = load_data(selected_stock)

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
def dividendData():
	div = yf.Ticker(selected_stock)
	div = div.dividends
	div = div.reset_index()
	div = div.rename(columns={"Date": "ds", "Dividends": "y"})
	st.subheader('Dividend Payouts')
	st.write(div.tail())
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=div['ds'], y=div['y'], name="dividends"))
	fig.layout.update(title_text='Dividend Payout Plot', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

	return div


def News():
	# Get the data
	news = yf.Ticker(selected_stock)
	news = news.news
	st.subheader('News')

	df = pd.DataFrame(news)
	st.table(df)

def FinancialStatements():
	# Get the data
	stock = yf.Ticker(selected_stock)
	stock = stock.financials
	st.subheader('Financial Statements')
	st.write(stock.tail())
	

plot_raw_data()

News()

FinancialStatements()

dividendData()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
