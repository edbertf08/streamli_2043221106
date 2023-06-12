# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import numpy as np
import streamlit as st
from pywaffle import Waffle
from PIL import Image

# Read Datasets
# survei tahun 2017
countries_by_steps = pd.read_csv('dataset/countries_by_steps.csv')

def find_country(country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        return ("not found")

countries_by_steps['country_code'] = countries_by_steps.apply(lambda row: find_country(row.country) , axis = 1)
# countries_by_steps[countries_by_steps['country_code'] == 'not found']
mask_russia = countries_by_steps['country'] == 'Russia'
mask_south_korea = countries_by_steps['country'] == 'South Korea'
mask_czech = countries_by_steps['country'] == 'Czech Republic'
mask_taiwan = countries_by_steps['country'] == 'Taiwan'

countries_by_steps['country_code'] = np.where(mask_russia, 'RUS', countries_by_steps['country_code'])
countries_by_steps['country_code'] = np.where(mask_south_korea, 'KOR', countries_by_steps['country_code'])
countries_by_steps['country_code'] = np.where(mask_czech, 'CZE', countries_by_steps['country_code'])
countries_by_steps['country_code'] = np.where(mask_taiwan, 'TWN', countries_by_steps['country_code'])

# countries_by_steps[countries_by_steps['country_code'] == 'not found']
# survei tahun 2017
countries_with_gender_gap = pd.read_csv('dataset/countries_with_gender_gap.csv')
countries_with_gender_gap = countries_with_gender_gap.rename(columns={'gender_gap_(m-f)':'gender_gap', 'gender_gap_(m-f)/m':'gender_gap_pct'})
countries_with_gender_gap['gender_gap_pct'] = countries_with_gender_gap['gender_gap_pct'].str.replace('%', '')
countries_with_gender_gap['gender_gap_pct'] = countries_with_gender_gap['gender_gap_pct'].astype('float')

# survei tahun 2015
road_length_in_jakarta = pd.read_excel('dataset/panjang-jalan-di-dki-jakarta-mencapai-7000-km.xlsx')
get_road_length = round(road_length_in_jakarta['value'].sum(), 2)

# survei tahun 2017
# total responden = 62.224
# total perempuan yang mengalami pelecehan seksual = 36.766
# total laki-laki yang mengalami pelecehan seksual = 23.403
data_sex_harras_gender = {'jenis kelamin':['Laki-laki', 'Perempuan'], 'persentase':[11, 60]}
sexual_harrasment_by_gender = pd.DataFrame(data_sex_harras_gender)

# survei tahun 2018
sexual_harrasment_in_public_space = pd.read_excel('dataset/transportasi-umum-sarang-pelecehan-seksual-di-ruang-publik.xlsx')
sexual_harrasment_in_public_space = sexual_harrasment_in_public_space.rename(columns={'nama_data':'moda_transportasi_umum', 'value':'persentase'})

# survei tahun 2018
data_sex_harras_types = {'bentuk_pelecehan':['Verbal', 'Fisik', 'Visual'], 'persentase':[60, 24, 15]}
sexual_harrasment_types = pd.DataFrame(data_sex_harras_types)

# survei tahun 2022
world_rank_air_quality = pd.read_excel('dataset/kualitas-udara-jakarta-pagi-ini-terburuk-kedua-di-dunia-jumat-17-juni-2022.xlsx')
# AQI = Air Quality Index
world_rank_air_quality = world_rank_air_quality.rename(columns={'nama_data':'city', 'value':'AQI'})


# Data Visualization

st.set_page_config(layout="wide")

countries = countries_by_steps['country'].to_list()
countries.append('All')
countries.sort()

#visualisasi countries by steps
# with st.sidebar:
#     st.write('Dashboard')

st.title("Jakarta, the City Where Nobody Wants to Walk")
option = st.selectbox(
    'Select a country',
    countries)
if option != 'All':
    fig_countries_by_steps = px.choropleth(countries_by_steps[countries_by_steps['country'] == option], locations="country_code", color="steps",
                color_continuous_scale=px.colors.diverging.BrBG,
                color_continuous_midpoint=countries_by_steps['steps'].mean(),
                hover_name="country")
    fig_countries_by_steps.update_layout(
        # margin=dict(l=20, r=20, t=60, b=30),
        paper_bgcolor="white",
        annotations = [dict(
        x=0.5,
        y=0.2,
        xref='paper',
        yref='paper',
        text='Source: <a href="http://activityinequality.stanford.edu/">\
            Activity Inequality</a>',
        showarrow = False
    )])

else:
    # visualisasi specific country by steps
    fig_countries_by_steps = px.choropleth(countries_by_steps, locations="country_code", color="steps",
        color_continuous_scale=px.colors.diverging.BrBG,
        color_continuous_midpoint=countries_by_steps['steps'].mean(),
        hover_name="country")
    fig_countries_by_steps.update_layout(
    margin=dict(l=20, r=20, t=60, b=30),
    paper_bgcolor="white",
    annotations = [dict(
    x=0.5,
    y=0.2,
    xref='paper',
    yref='paper',
    text='Source: <a href="http://activityinequality.stanford.edu/">\
        Activity Inequality</a>',
    showarrow = False
    )])

st.markdown("<h2 style='text-align: center; color: black;'>World Average Steps Per Day Rankings</h2>", unsafe_allow_html=True)
st.plotly_chart(fig_countries_by_steps, use_container_width=True)

if option != "All":
    st.write(f"<h4 style='text-align: center;'>Average steps: {countries_by_steps[countries_by_steps['country'] == option]['steps'].values[0]}</h4>", unsafe_allow_html=True)
else:
    st.write(f"<h4 style='text-align: center;'>Average steps: {round(countries_by_steps['steps'].mean(), 2)}</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig_countries_by_steps_top10=px.bar(countries_by_steps.sort_values('steps').head(10),x='steps',y='country',
            orientation='h',
            color = 'steps',
            color_continuous_scale='Blackbody'
            )
    fig_countries_by_steps_top10.update_layout(title='<b>Top 10 Countries with the Lowest Average Steps per Day</b>', yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_countries_by_steps_top10)
with col2:
    fig_countries_by_steps_bot10=px.bar(countries_by_steps.head(10),x='steps',y='country',
            orientation='h',
            color = 'steps',
            color_continuous_scale='Viridis'
            )
    fig_countries_by_steps_bot10.update_layout(title='<b>Top 10 Countries with the Highest Average Steps per Day</b>', yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_countries_by_steps_bot10)
st.markdown("""Menurut penelitian yang dilakukan oleh para ilmuwan dari Stanford University pada tahun 2017, didapati bahwa Indonesia menempati posisi pertama
            sebagai negara yang **paling malas** berjalan kaki di dunia. Penelitian tersebut dilakukan terhadap 717.627 orang dari 111 negara dalam kurun waktu 95 hari dengan melakukan pelacakan pergerakan _smartphone_. Dari data yang diperoleh, rata-rata orang Indonesia hanya berjalan kaki 3.513 langkah per hari,
            sangat jauh jika dibandingkan dengan catatan rata-rata global, yaitu sekitar 5000 langkah per hari. Berdasarkan data tersebut dapat dilihat bahwa Hong Kong menempati urutan pertama dengan rata-rata 6.880 langkah per hari. Bisa dikatakan hampir dua kali rata-rata orang Indonesia berjalan kaki. Kemudian, China menempati uruta
            kedua dengan rata-rata 6.170 langkah setiap harinya. Lantas sebenarnya apa _sih_ yang membuat Indonesia mendapat predikat sebagai negara paling malas kaki se-dunia?""")

st.markdown("""menurut **cnbcindonesia.com**, **kompas.com**, **idntimes.com** dan **vice.com**, berikut saya rangkum alasan umum mengapa masyarakat Indonesia malas berjalan kaki:<br>
<or>
    <li>Infrastruktur yang kurang mendukung</li>
    <li>_Catcalling_</li>
    <li>Polusi</li>
</or>""", unsafe_allow_html=True)


# data panjang trotoar di Jakarta
sidewalk_length_in_jakarta = pd.read_excel('dataset/panjang_dan_luas_trotoar_dki_jakarta.xls')
headers = sidewalk_length_in_jakarta.iloc[2]
sidewalk_length_in_jakarta = pd.DataFrame(sidewalk_length_in_jakarta.values[3:], columns=headers)

sidewalk_length_in_jakarta = sidewalk_length_in_jakarta.rename(columns={'Panjang (Meter)':'Panjang (M)', 'Luas(M2)':'Luas (M2)'})
sidewalk_length_in_jakarta['Panjang (M)'] = sidewalk_length_in_jakarta['Panjang (M)'].str.replace(',', '.').str.replace(' ', '')
sidewalk_length_in_jakarta['Luas (M2)'] = sidewalk_length_in_jakarta['Luas (M2)'].str.replace(',', '.').str.replace(' ', '')

sidewalk_length_in_jakarta['Panjang (M)'] = sidewalk_length_in_jakarta['Panjang (M)'].astype('float')
sidewalk_length_in_jakarta['Luas (M2)'] = sidewalk_length_in_jakarta['Luas (M2)'].astype('float')

sidewalk_length_in_jakarta['Increase Percentage'] = round(sidewalk_length_in_jakarta['Panjang (M)'].pct_change(), 2)
sidewalk_length_in_jakarta = sidewalk_length_in_jakarta.fillna(0)
sidewalk_length_2020 = sidewalk_length_in_jakarta.iloc[-1]['Panjang (M)']
sidewalk_length_2020 = round(sidewalk_length_2020 / 1000, 2)

road_length_in_jakarta = pd.read_excel('dataset/panjang-jalan-di-dki-jakarta-mencapai-7000-km.xlsx')
get_road_length = round(road_length_in_jakarta['value'].sum(), 2)

mean_increase_sidewalk = round(sidewalk_length_in_jakarta['Increase Percentage'].mean(), 4)
reality_pct = round(sidewalk_length_2020 / get_road_length * 100, 2)

st.markdown('<h2>Infrastruktur yang Kurang Mendukung</h2>', unsafe_allow_html=True)
st.markdown('<h4>Perbandingan Panjang Trotoar dan Jalan di Jakarta</h4>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Panjang Trotoar", value=str(sidewalk_length_2020) + " km", delta="rata-rata bertambah "+str(mean_increase_sidewalk)+" %")
with col2:
    st.metric(label="Panjang Jalan", value=str(get_road_length) + " km")
with col3:
    st.metric(label="Pencapaian", value=f"{reality_pct} % dari {get_road_length} km")

fig_sidewalk_by_year = px.bar(sidewalk_length_in_jakarta, x='Tahun Anggaran', y='Panjang (M)',
                color='Panjang (M)',
                title='<b>Panjang Trotoar di Jakarta 2001-2020</b>',
                labels={'Panjang (M)':'Panjang', 'Tahun Anggaran':'Tahun'})
fig_sidewalk_by_year.update_layout(xaxis={'categoryorder':'total descending'})

col1, col2 = st.columns(2)
with col1:
    st.markdown("""Berdasarkan data tersebut, ternyata panjang total trotoar di Jakarta bahkan kurang dari 10% dari panjang total jalan di Jakarta. Ini sangat memprihatinkan mengingat Jakarta merupakan
metropolitan terbesar di Indonesia yang masih belum memenuhi hak pejalan kaki di berbagai belahan. Semakin mengecewakannya lagi, pembangunan untuk perpanjangan trotoar
cenderung stagnan dari tahun ke tahun. Katakan saja dari tahun 2016 sampai 2020, panjang trotoar di Jakarta tidak ada peningkatan. Sangat disayangkan dengan kondisi demikian, tentunya mengharuskan
para pejalan kaki memakai pinggir jalan sebagai jalur berjalan kaki. Ini sangat membahayakan para pejalan kaki.""")
with col2:
    st.plotly_chart(fig_sidewalk_by_year)

image = Image.open('foto/pedagang kaki lima masih berjualan di sekitar luar Tebet Eco Park tepatnya sisi Jalan Tebet Barat, Jakarta Selatan.jpg')
image2 = Image.open('foto/kondisi-trotoar-jl-pegangsaan-timur-jakpus-yang-diserobot-pemotor-17-mei-2022-sore-annisa-rfdetikcom-1.jpeg')


col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.image(image, 
        caption='Gambar 1: Sejumlah pedagang kaki lima (PKL) masih berjualan di sekitar luar Tebet Eco Park tepatnya sisi Jalan Tebet Barat, Jakarta Selatan, 13 Juni 2022 siang (Sumber: Kompas.com)')
with col2:
    st.image(image2, 
        caption='Gambar 2: Kondisi trotoar Jl Pegangsaan Timur, Jakpus, yang diserobot pemotor, 17 Mei 2022 sore (Sumber: detikNews)')
with col3:
    st.markdown("""Masalahnya bukan hanya masih kurangnya trotoar di Jakarta. Kalaupun ada, terkadang trotoar seperti benar-benar bukan dibuat untuk pejalan kaki.
    Dari gambar di samping (Gambar 1) dapat dilihat bahwa masih ada saja pedagang kaki lima (PKL) yang memakai trotoar untuk berdagang. Selain itu, pejalan kaki sering dibuat resah
    dengan adanya pengendara motor yang menggunakan trotoar (Gambar 2). Hal ini tentunya membuat orang Jakarta semakin malas berjalan kaki karena kesulitan mendapatkan akses.""")
    st.markdown("""<q>Kalau terus dibiarkan dan tidak ditindak tegas, takutnya makin banyak pengendara yang ngeyel. Mereka bakal nggak sadar kalau trotoar ini tuh punya pejalan kaki, haknya pejalan kaki</q>, ucap Irma, wanita 27 tahun
    yang setiap sorenya melewati Jl Pegangsaan Timur, Jakpus.""", unsafe_allow_html=True)

# visualisasi average all countries by gender
fig_average_steps_gender = px.bar(countries_with_gender_gap, x="country", y=["steps_male_mean", "steps_female_mean"], title="<b>Average Steps Per Day by Gender</b>", labels={'variable':'Gender', 'value':'Average Steps', 'country':'Country'})
newnames = newnames = {'steps_male_mean':'male', 'steps_female_mean': 'female'}
fig_average_steps_gender.for_each_trace(lambda t: t.update(name = newnames[t.name]))
fig_average_steps_gender.update_layout(xaxis={'categoryorder':'total descending'})

# visualisasi all countries by gender gap
fig_countries_gender_gap = px.bar(countries_with_gender_gap, x='country', y='gender_gap', 
                hover_data=['gender_gap', 'gender_gap_pct'], color='gender_gap', labels={'gender_gap':'Gender Gap', 'country': 'Country', 'gender_gap_pct':'Gender Gap (%)'},
                title='<b>Gender Gap in Average Steps Per Day</b>')
fig_countries_gender_gap.update_layout(xaxis={'categoryorder':'total descending'})

st.markdown('<h2><i>Catcalling</i></h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_average_steps_gender, use_container_width=True)
with col2:
    st.plotly_chart(fig_countries_gender_gap, use_container_width=True)
st.markdown("""Dari grafik tersebut terlihat bahwa Indonesia masih memiliki gap yang relatif besar, yakni 16%. Lalu apa sebenarnya yang membuat adanya gap tersebut? Apakah ada perlakuan yang berbeda bagi laki-laki dan perempuan saat berjalan kaki?""")


# visualisasi 3 dari 5 perempuan pernah mendapatkan pelecehan di ruang publik
data_waffle_public_woman = {'pernah':3, 'tidak pernah':2}
fig_waffle_public_woman = plt.figure(
    FigureClass=Waffle, 
    rows=1,
    values=data_waffle_public_woman,
    colors=("#ff4000", "#f7b801"),
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.2, 1)},
    icons='person-dress', icon_size=25, 
    icon_legend=True
)

# visualisasi 1 dari 10 laki-laki pernah mendapatkan pelecehan di ruang publik
data_waffle_public_man = {'pernah':1, 'tidak pernah':9}
fig_waffle_public_man = plt.figure(
    FigureClass=Waffle, 
    rows=2,
    values=data_waffle_public_man,
    colors=("#1C3879", "#EAE3D2"),
    legend={'loc': 'upper left','bbox_to_anchor': (1.2, 1)},
    icons='person', icon_size=25, 
    icon_legend=True
)

# fig_waffle_public_woman.suptitle('This is a somewhat long figure title', fontsize=10)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h3>3 dari 5 perempuan pernah mendapatkan pelecehan di ruang publik</h3>", unsafe_allow_html=True)
    # st.header("3 dari 5 perempuan pernah mendapatkan pelecehan di ruang publik")
    st.pyplot(fig_waffle_public_woman, use_container_width=True)
with col2:
    st.markdown("<h3>1 dari 10 laki-laki pernah mendapatkan pelecehan di ruang publik</h3>", unsafe_allow_html=True)
    # st.header("1 dari 10 laki-laki pernah mendapatkan pelecehan di ruang publik")
    st.pyplot(fig_waffle_public_man, use_container_width=True)

st.markdown("""Ternyata oh ternyata, berdasarkan survei yang dilakukan oleh Koalisi Ruang Publik Aman (KRPA) dan difasilitasi oleh Change.org dengan responden sebanyak 62.224 orang pada tahun 2018, didapati bahwa
3 dari 5 perempuan pernah mendapatkan pelecehan di ruang publik. Sementara itu, 1 dari 10 laki-laki pernah mendapatkan pelecehan di ruang publik. Statistik ini mengindikasikan
bahwa perempuan jauh lebih sering mendapatkan pelecehan di ruang publik dengan data yang mencapai di atas 50%. Lalu, bentuk pelecehan apa saja yang paling sering terjadi?""")

# visualisasi sexual harassment in public space
fig_sex_harras_public = px.pie(sexual_harrasment_in_public_space, values='persentase', names='moda_transportasi_umum', color_discrete_sequence=px.colors.sequential.RdBu, title='<b>Sexual Harassment by Public Transport in Jakarta</b>')
st.plotly_chart(fig_sex_harras_public, use_container_width=True)
st.markdown("""Pada survei yang sama, mayoritas mengatakan bahwa pelecehan yang paling sering didapati ketika sedang berada di bus dengan persentase 38,7%. Disusul dengan angkot, yakni 31,9%, KRL sebesar 19,6%, kemudian ada ojek online dan ojek konvensional yang masing-masing 4,79% dan  4,27%.
Dari data yang diperoleh dapat terlihat jelas bahwa transportasi umum, yakni bus, angkot dan KRL merupakan sarang terjadinya pelecehan. Tentunya pemerintah perlu memegang kendali penuh untuk mengatasi kasus ini. Keamanan dan kenyamanan masyarakat
dalam menggunakan transportasi umum perlu ditingkatkan, terkhusus bagi perempuan.""")


# visualisasi type of sexual harrasment
data_sex_harras_types = {'bentuk_pelecehan':['Verbal', 'Fisik', 'Visual', 'lainnya'], 'persentase':[60, 24, 15, 1]}
sexual_harrasment_types = pd.DataFrame(data_sex_harras_types)


# visualisasi jumlah pelecehan seksual di Jakarta
data_sex_harras_jkt = {'tahun':['2020', '2021', '2022'], 'jumlah_kasus':[8, 7, 15]}
sexual_harrasment_in_jakarta = pd.DataFrame(data_sex_harras_jkt)

fig_sex_harras_jkt = px.bar(sexual_harrasment_in_jakarta, x='tahun', y='jumlah_kasus', color='jumlah_kasus', labels={'tahun':'Tahun', 'jumlah_kasus': 'Jumlah Kasus'},
                title='<b>Female Sexual Harrasment Cases in Jakarta</b>', color_continuous_scale='Hot_r')
st.plotly_chart(fig_sex_harras_jkt, use_container_width=True)
st.markdown("""Mirisnya lagi, dari laporan Pusat Pelayanan Terpadu Pemberdayaan Perempuan dan Anak (P2TP2A), jumlah laporan kasus pelecehan seksual yang dilakukan terhadap perempuan meningkat pada tahun 2022.
Padahal baru pertengahan tahun, namun data tersebut sudah mencapai hampir dua kali lipat dari tahun sebelumnya, yakni 2021, dan 2021. Data ini didapati berdasarkan adanya laporan dari korban.
Lalu, bagaimana dengan yang tidak melapor? Mungkin ada puluhan, atau bahkan ratusan?""")


# visualisasi world rank air quality index
fig_world_aqi=px.bar(world_rank_air_quality,x='AQI',y='city',
           orientation='h',
           color = 'AQI',
           color_continuous_scale='Inferno_r'
           )
fig_world_aqi.update_layout(title='<b>World Air Quality Index Rankings</b>', yaxis=dict(autorange="reversed"))
st.markdown('<h2>Polusi</h2>', unsafe_allow_html=True)
st.plotly_chart(fig_world_aqi, use_container_width=True)
st.markdown("""Kemudian alasan terakhir tak lain dan tak bukan adalah polusi. Baru-baru ini **IQAir** mendapati dalam datanya bahwa Jakarta yang mana membawa perwakilan Indonesia, 
mendapatkan predikat sebagai kota kedua dengan kualitas udara terburuk di dunia. Bagaimana tidak, dengan Air Quality Index (AQI) yang mencapai angka 166 yang berarti angka tersebut sudah dalam kategori _unhealthy_ yang berarti tidak baik untuk kesehatan.""")

with st.container():
    st.markdown('<h3>Rekomendasi dan Saran</h3>', unsafe_allow_html=True)
    st.markdown("""
    <h6>Bagi pemerintah:</h6>
    <ul>
        <li>Lebih memperdulikan lagi hak pejalan kaki dengan melakukan pembangunan trotoar pada wilayah yang belum memiliki akses trotoar.</li>
        <li>Bertindak tegas bagi siapa saja yang sembarangan memakai trotoar selain pejalan kaki.</li>
        <li>Memberikan pendampingan, edukasi untuk pemulihan kesehatan mental korban.</li>
        <li>Bertindak tegas terhadap pelaku maupun untuk memberantas kasus pelecehan seksual.</li>
        <li>Memperbanyak alat ukur kualitas udara di berbagai titik agar bisa memantau dan mengevaluasi.</li>
        <li>Menanam lebih banyak pepohonan di pinggir jalan atau di tempat yang banyak dilalui oleh kendaraan.</li>
    </li>
    <br>
    <h6>Bagi masyarakat:</h6>
    <ul>
        <li>Jangan bertindak egois dan sembrono untuk memakai fasilitas secara sembarangan.</li>
        <li>Memakai alat pelindung diri, atau mempelajari bela diri dasar.</li>
        <li>Membekali diri dengan pendidikan seksual.</li>
        <li>Jika mengalami pelecehan, segera laporan ke pihak berwajib terdekat.</li>
        <li>Hindari membakar sampah.</li>
        <li>Ikut serta dalam penanaman pohon di sekitar rumah atau di tempat lainnya.</li>
    </li>
    """, unsafe_allow_html=True)

st.markdown("""&copy; 2022 Edbert Fernando""", unsafe_allow_html=True)