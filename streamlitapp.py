import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

stocks = (
'PRX.JO',
'ANH.JO',
'BTI.JO',
'GLN.JO',
'CFR.JO',
'BHP.JO',
'NPN.JO',
'AGL.JO',
'AMS.JO',
'FSR.JO',
'MTN.JO',
'VOD.JO',
'SBK.JO',
'CPI.JO',
'SOL.JO',
'S32.JO',
'IMP.JO',
'MNP.JO',
'KIO.JO',
'SSW.JO',
'ABG.JO',
'GFI.JO',
'SLM.JO',
'SHP.JO',
'ANG.JO',
'BID.JO',
'DSY.JO',
'NED.JO',
'APN.JO',
'PPH.JO',
'NHM.JO',
'RMI.JO',
'CLS.JO',
'REM.JO',
'OMU.JO',
'NRP.JO',
'BVT.JO',
'INP.JO',
'EXX.JO',
'RNI.JO',
'WHL.JO',
'MCG.JO',
'MRP.JO',
'GRT.JO',
'ARI.JO',
'MEI.JO',
'QLT.JO',
'RBP.JO',
'TFG.JO',
'DGH.JO',
'VVO.JO',
'HMN.JO',
'TBS.JO',
'N91.JO',
'LHC.JO',
'TXT.JO',
'HAR.JO',
'SPP.JO',
'TCP.JO',
'SRE.JO',
'SNT.JO',
'CCO.JO',
'DCP.JO',
'MSP.JO',
'MTM.JO',
'LBH.JO',
'INL.JO',
'APH.JO',
'BAW.JO',
'PIK.JO',
'AVI.JO',
'TKG.JO',
'RDF.JO',
'RES.JO',
'SAP.JO',
'TRU.JO',
'BYI.JO',
'MTH.JO',
'SNH.JO',
'NTC.JO',
'ITE.JO',
'KST.JO',
'PSG.JO',
'CML.JO',
'KRO.JO',
'NY1.JO',
'EQU.JO',
'FFA.JO',
'LTE.JO',
'RCL.JO',
'IPL.JO',
'MSM.JO',
'AFE.JO',
'HYP.JO',
'SPG.JO',
'TGA.JO',
'IAP.JO',
'TSG.JO',
'ACL.JO',
'VKE.JO',
'KAP.JO',
'STP.JO',
'DRD.JO',
'JSE.JO',
'IPF.JO',
'OMN.JO',
'EPP.JO',
'GTC.JO',
'AIP.JO',
'AIL.JO',
'RLO.JO',
'ADH.JO',
'AFT.JO',
'PAN.JO',
'COH.JO',
'DTC.JO',
'JBL.JO',
'OCE.JO',
'THA.JO',
'PPC.JO',
'ARL.JO',
'CSB.JO',
'FBR.JO',
'SSS.JO',
'SUI.JO',
'WBO.JO',
'RBX.JO',
'HCI.JO',
'MUR.JO',
'SAC.JO',
'BAT.JO',
'ATT.JO',
'MTA.JO',
'AFH.JO',
'RAV.JO',
'EMI.JO',
'MPT.JO',
'ZED.JO',
'GSH.JO',
'TGO.JO',
'MED.JO',
'SHG.JO',
'BLU.JO',
'L2D.JO',
'REN.JO',
'MIX.JO',
'HDC.JO',
'LBR.JO',
'GML.JO',
'L4L.JO',
'KAL.JO',
'NT1.JO',
'FFB.JO',
'MTNZF.JO',
'PPE.JO',
'CLI.JO',
'AHB.JO',
'RFG.JO',
'AEG.JO',
'MRF.JO',
'GND.JO',
'AEL.JO',
'CAT.JO',
'EXP.JO',
'CLH.JO',
'IVT.JO',
'SCD.JO',
'LEW.JO',
'ACT.JO',
'SDO.JO',
'HET.JO',
'HIL.JO',
'TDH.JO',
'WEZ.JO',
'OAO.JO',
'NPK.JO',
'CTA.JO',
'SYG.JO',
'YYLBEE.JO',
'DIA.JO',
'SBP.JO',
'OCT.JO',
'RMH.JO',
'FVT.JO',
'CRP.JO',
'AVV.JO',
'SUR.JO',
'DRA.JO',
'CMH.JO',
'TTO.JO',
'SEA.JO',
'MDI.JO',
'ARH.JO',
'BWN.JO',
'ACS.JO',
'BRN.JO',
'SAR.JO',
'ENX.JO',
'EMN.JO',
'HLM.JO',
'MFL.JO',
'EPE.JO',
'OAS.JO',
'ORN.JO',
'UPL.JO',
'TEX.JO',
'GPL.JO',
'BEL.JO',
'AYO.JO',
'YRK.JO',
'ILU.JO',
'DIB.JO',
'HPR.JO',
'APF.JO',
'QFH.JO',
'SOLBE1.JO',
'CHP.JO',
'AHA.JO',
'PBG.JO',
'SFN.JO',
'EOH.JO',
'TRE.JO',
'TPF.JO',
'BCF.JO',
'MST.JO',
'FGL.JO',
'DNB.JO',
'SNV.JO',
'NVS.JO',
'MMP.JO',
'WSL.JO',
'OLG.JO',
'TMT.JO',
'ART.JO',
'DKR.JO',
'NWL.JO',
'KP2.JO',
'ADR.JO',
'TON.JO',
'EPS.JO',
'HUG.JO',
'CND.JO',
'CKS.JO',
'TPC.JO',
'CGR.JO',
'ALH.JO',
'VUN.JO',
'SEP.JO',
'NVE.JO',
'AEE.JO',
'DLT.JO',
'ISB.JO',
'ASC.JO',
'RSG.JO',
'NRL.JO',
'RHB.JO',
'SOH.JO',
'WKF.JO',
'BUC.JO',
'BIK.JO',
'TRL.JO',
'SEB.JO',
'BAU.JO',
'AME.JO',
'EMH.JO',
'AVL.JO',
'BRT.JO',
'ARA.JO',
'ETO.JO',
'ELI.JO',
'LNF.JO',
'HUL.JO',
'FSE.JO',
'KBO.JO',
'PFB.JO',
'REA.JO',
'RTN.JO',
'CVW.JO',
'REB.JO',
'CMO.JO',
'MCZ.JO',
'CSG.JO',
'ISA.JO',
'4SI.JO',
'CGN.JO',
'PPR.JO',
'EEL.JO',
'LAB.JO',
'PMV.JO',
'SSK.JO',
'EUZ.JO',
'RNG.JO',
'JSC.JO',
'AON.JO',
'TLM.JO',
'UAT.JO',
'BSR.JO',
'AHL.JO',
'HWA.JO',
'RTO.JO',
'SVB.JO',
'NCS.JO',
'PEM.JO',
'CAC.JO',
'PSV.JO',
'ILE.JO',
'MRI.JO',
'TAS.JO',
'AOO.JO',
'VIS.JO',
'ADW.JO',
'ECS.JO',
'GLI.JO',
'WEA.JO',
'NFP.JO',
'NUT.JO',
'ACZ.JO',
'PHM.JO',
'RPL.JO',
'ACE.JO',
'RDI.JO',
'AFX.JO',
'ACG.JO',
'ALP.JO',
'TBG.JO',
'CTK.JO',
'UCP.JO',
'VLE.JO',
'COM.JO',
'CIL.JO',
'EFG.JO',
'ELR.JO',
'ESR.JO',
'FDP.JO',
'GAI.JO',
'GRF.JO',
'HPB.JO',
'IDQ.JO',
'KDV.JO',
'MZR.JO',
'MLE.JO',
'MNK.JO',
)

selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

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
