import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

df_pekerja_tetap = pd.read_csv('Indeks Tahunan Pekerja Tetap Konstruksi.csv')
df_harian_pekerja = pd.read_csv('Indeks Tahunan Hari Orang Pekerja Harian Perusahaan Konstruksi.csv')
df_balas_jasa = pd.read_csv('Indeks Tahunan Balas Jasa Pekerja Tetap dan Upah Pekerja Harian Konstruksi.csv')
df_nilai_konstruksi = pd.read_csv('Indeks Tahunan Nilai Konstruksi yang Diselesaikan Perusahaan Konstruksi.csv')
df_covid = pd.read_csv('WHO-COVID-19-global-data.csv')

kepulauan_mapping = {
    'Sumatera': ['ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG', 'KEP. BANGKA BELITUNG', 'KEP. RIAU'],
    'Jawa': ['DKI JAKARTA', 'JAWA BARAT', 'JAWA TENGAH', 'DI YOGYAKARTA', 'JAWA TIMUR', 'BANTEN'],
    'Kalimantan': ['KALIMANTAN BARAT', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 'KALIMANTAN TIMUR', 'KALIMANTAN UTARA'],
    'Sulawesi': ['SULAWESI UTARA', 'SULAWESI TENGAH', 'SULAWESI SELATAN', 'SULAWESI TENGGARA', 'GORONTALO', 'SULAWESI BARAT'],
    'Bali & Nusa Tenggara': ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR'],
    'Maluku & Papua': ['MALUKU', 'MALUKU UTARA', 'PAPUA BARAT', 'PAPUA'],
}

def process_data(df, kepulauan_mapping):
    rata_rata = {}
    for kepulauan, provinsi_list in kepulauan_mapping.items():
        rata_rata[kepulauan] = df[df['Provinsi'].isin(provinsi_list)].iloc[:, 1:].mean()
    return pd.DataFrame(rata_rata)

df_rata_rata_pekerja_tetap = process_data(df_pekerja_tetap, kepulauan_mapping)
df_rata_rata_harian_pekerja = process_data(df_harian_pekerja, kepulauan_mapping)
df_rata_rata_balas_jasa = process_data(df_balas_jasa, kepulauan_mapping)
df_rata_rata_nilai_konstruksi = process_data(df_nilai_konstruksi, kepulauan_mapping)

def main():

    st.set_page_config(layout="wide")
    
    tdf = pd.concat([df_rata_rata_pekerja_tetap.T.mean(), df_rata_rata_harian_pekerja.T.mean(), df_rata_rata_balas_jasa.T.mean(), df_rata_rata_nilai_konstruksi.T.mean()], axis=1)
    tdf.columns = ['Rata-rata Pekerja Tetap', 'Rata-rata Harian Pekerja', 'Rata-rata Balas Jasa', 'Rata-rata Nilai Konstruksi']
    
    pdf = pd.concat([df_rata_rata_pekerja_tetap.mean(), df_rata_rata_harian_pekerja.mean(), df_rata_rata_balas_jasa.mean(), df_rata_rata_nilai_konstruksi.mean()], axis=1)
    pdf.columns = ['Rata-rata Pekerja Tetap', 'Rata-rata Harian Pekerja', 'Rata-rata Balas Jasa', 'Rata-rata Nilai Konstruksi']

    dfi = df_covid.loc[df_covid['Country'] == 'Indonesia', ['Date_reported', 'New_cases', 'New_deaths']]
    dfi.fillna(0, inplace=True)
    dfi['Date_reported'] = pd.to_datetime(dfi['Date_reported'])
    dfi['Year'] = dfi['Date_reported'].dt.year
    dfr = dfi.groupby('Year').mean()[['New_cases', 'New_deaths']]
    dfr = dfr.drop([2023, 2024])
    
    years = range(2013, 2020)
    dfn = pd.DataFrame(index=years, columns=['New_cases', 'New_deaths'])
    dfn['New_cases'] = 0
    dfn['New_deaths'] = 0
    
    dfnr = pd.concat([dfn, dfr])
    dfnr.index = dfnr.index.astype(str)
    tdfc = pd.concat([tdf, dfnr], axis=1)
    tdfc.columns = ['Rata-rata Pekerja Tetap', 'Rata-rata Harian Pekerja', 'Rata-rata Balas Jasa', 'Rata-rata Nilai Konstruksi', 'Rata-rata Kasus Covid', 'Rata-rata Korban Covid']
    
    st.title('Analisis Indeks Kinerja Sektor Konstruksi')
    page = st.sidebar.radio("Go to", ("Pendahuluan", "Analisis", "Hipotesa"))

    # Pendahuluan
    if page == "Pendahuluan":
        st.subheader('Dibuat Oleh: Mangara Haposan Immanuel Siagian')
        st.header('Latar Belakang')
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image('CEICON.jpg', width=300)
        st.markdown('''
        Sektor konstruksi merupakan salah satu sektor vital dalam perekonomian Indonesia yang memberikan kontribusi signifikan terhadap pertumbuhan ekonomi, penciptaan lapangan kerja, dan pengembangan infrastruktur. Kegiatan konstruksi meliputi pembangunan rumah, jalan, jembatan, gedung-gedung komersial dan industri, serta proyek-proyek infrastruktur lainnya yang mendukung pertumbuhan ekonomi dan kesejahteraan masyarakat.

        Analisis terhadap indeks kinerja sektor konstruksi menjadi penting untuk memahami dinamika, tren, dan perbandingan kinerja sektor tersebut dari waktu ke waktu serta antar wilayah di Indonesia. Perbandingan kinerja antar tahun memungkinkan untuk mengevaluasi kemajuan atau kemunduran sektor konstruksi dari satu periode ke periode berikutnya, sementara perbandingan antar pulau memungkinkan untuk mengidentifikasi perbedaan dalam faktor-faktor yang memengaruhi kinerja sektor konstruksi di berbagai wilayah geografis Indonesia.
    
        Beberapa faktor yang mungkin mempengaruhi kinerja sektor konstruksi antar tahun dan antar pulau meliputi:
        * **Pertumbuhan Ekonomi:** Tingkat pertumbuhan ekonomi suatu wilayah dapat berdampak langsung pada aktivitas konstruksi. Wilayah dengan pertumbuhan ekonomi yang tinggi cenderung memiliki aktivitas konstruksi yang lebih besar.
        * **Kebijakan Pemerintah:** Kebijakan pemerintah terkait dengan investasi infrastruktur dan regulasi sektor konstruksi juga dapat memengaruhi kinerja sektor tersebut dari waktu ke waktu dan dari satu wilayah ke wilayah lain.
        * **Infrastruktur Pendukung:** Ketersediaan infrastruktur pendukung seperti transportasi dan akses ke sumber daya serta pasokan material konstruksi dapat mempengaruhi kinerja sektor konstruksi di berbagai wilayah.
        * **Faktor Geografis dan Lingkungan:** Perbedaan geografis dan lingkungan antar pulau di Indonesia, termasuk topografi, iklim, dan kebutuhan infrastruktur lokal, juga dapat mempengaruhi kinerja sektor konstruksi.
    
        Dengan menganalisis indeks kinerja sektor konstruksi dari perspektif perbandingan antar tahun dan antar pulau, dapat memberikan wawasan yang berharga bagi pembuat kebijakan, pelaku industri, dan pemangku kepentingan lainnya untuk mengidentifikasi tantangan, peluang, serta strategi pengembangan sektor konstruksi yang lebih efektif dan berkelanjutan di Indonesia.
        ''')
        
    # Analisis
    elif page == "Analisis":
        plt.figure(figsize=(10, 6))
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Tren Kinerja Sektor Konstruksi Antar Tahun')
            st.write(tdf.describe())
            
            st.markdown('''
            Secara keseluruhan, statistik ini memberikan gambaran tentang kinerja sektor konstruksi selama periode 2013-2022. Meskipun rata-rata menunjukkan peningkatan dari tahun ke tahun, **variasi yang signifikan** terlihat dalam setiap variabel, menunjukkan kompleksitas dan dinamika yang ada dalam sektor ini.
            
            Analisis ini dapat digunakan oleh pembuat kebijakan, investor, dan praktisi industri konstruksi untuk memahami tren dan mengambil langkah-langkah yang tepat dalam mengembangkan sektor konstruksi di berbagai pulau. Hal ini mungkin meliputi:
            * Penyesuaian kebijakan,
            * Alokasi sumber daya, dan
            * Pengembangan strategi yang sesuai dengan setiap wilayah.
            ''')
            
            year_range = st.slider('Select a range of years', min_value=2013, max_value=2022, value=(2013, 2022))
            ftdf = tdf.loc[(tdf.index >= str(year_range[0])) & (tdf.index <= str(year_range[1]))]
            st.line_chart(ftdf)
            
            st.markdown('''
            Secara keseluruhan, dapat disimpulkan bahwa sektor konstruksi mengalami pertumbuhan yang signifikan selama periode yang diamati. 
            
            Pertumbuhan ini mungkin dipengaruhi oleh berbagai faktor seperti:
            * Pertumbuhan ekonomi, 
            * Investasi infrastruktur, 
            * Kebijakan pemerintah, dan 
            * Permintaan pasar.
            
            Analisis ini dapat memberikan wawasan penting bagi pembuat kebijakan, investor, dan praktisi industri konstruksi untuk mengambil langkah-langkah yang tepat dalam mengembangkan sektor ini di berbagai pulau. Hal ini termasuk mempertimbangkan:
            * Investasi lebih lanjut, 
            * Peningkatan regulasi, dan 
            * Pengembangan infrastruktur yang mendukung pertumbuhan sektor konstruksi di masa depan.
            ''')

        with col2:
            st.subheader('Tren Kinerja Sektor Konstruksi Antar Pulau')
            st.write(pdf.describe())
            
            st.markdown('''
            Secara keseluruhan, data menunjukkan bahwa sektor konstruksi memiliki kinerja yang relatif stabil di berbagai pulau yang diamati. Meskipun ada variasi antar-pulau, **variasi tersebut relatif kecil dan tidak signifikan**. 
            
            Hal ini dapat memberikan kepercayaan kepada pembuat kebijakan, investor, dan praktisi industri konstruksi bahwa sektor ini menunjukkan konsistensi dalam kinerjanya di berbagai wilayah. Upaya untuk mengembangkan sektor ini di berbagai pulau dapat difokuskan pada:
            * Peningkatan efisiensi, 
            * Peningkatan kualitas proyek, dan 
            * Pengelolaan sumber daya yang lebih baik.
            ''')

            categories = pdf.index.unique()
            selected_categories = st.multiselect('Select categories', categories)
            fpdf = pdf.loc[pdf.index.isin(selected_categories)]
            st.bar_chart(fpdf)

            st.markdown("")
            st.markdown('''
            Dari analisis ini, beberapa pola muncul:
            * Jawa memiliki kinerja yang relatif tinggi dalam semua kategori, menunjukkan potensi besar dalam sektor konstruksi.
            * Pulau Kalimantan juga menonjol dalam beberapa aspek, khususnya dalam jumlah pekerja harian dan balas jasa.
            * Sulawesi memiliki kinerja yang lebih rendah dibandingkan dengan pulau lain dalam hal pekerjaan harian dan nilai konstruksi.
            
            Analisis ini dapat memberikan wawasan bagi pembuat kebijakan, investor, dan praktisi industri konstruksi untuk mengidentifikasi area di mana perhatian lebih lanjut atau investasi mungkin diperlukan untuk mengembangkan sektor konstruksi di berbagai pulau di Indonesia sesuai dengan karakteristik dan kebutuhan masing-masing wilayah.
            ''')

    # Uji Hipotesa
    elif page == "Hipotesa":
        st.subheader('Uji Hipotesis: Korelasi antara Tren Konstruksi Antar Tahun dan Antar Pulau')

        include_covid_data = st.checkbox('Data COVID')
        st.markdown('**Note**: Data COVID hanya tersedia untuk Tren Kinerja Sektor Konstruksi Antar Tahun')
        selected_table = st.selectbox('Pilih Tabel', ['Tren Kinerja Sektor Konstruksi Antar Tahun', 'Tren Kinerja Sektor Konstruksi Antar Pulau'])
    
        if include_covid_data and selected_table == 'Tren Kinerja Sektor Konstruksi Antar Tahun':
            data = tdfc  
        elif selected_table == 'Tren Kinerja Sektor Konstruksi Antar Pulau':
            data = pdf
        else:
            data = tdf
    
        selected_column1 = st.selectbox('Pilih Kolom Pertama', data.columns)
        selected_column2 = st.selectbox('Pilih Kolom Kedua', data.columns)
    
        pearson_corr, p_value = pearsonr(data[selected_column1], data[selected_column2])
    
        st.subheader('Hasil Uji Hipotesis')
        st.write(f'Koefisien Korelasi Pearson: {pearson_corr}')
        st.write(f'Nilai p-value: {p_value}')
    
        if p_value < 0.05:
            st.write(f'Terdapat korelasi signifikan antara {selected_column1} dan {selected_column2}.')
        else:
            st.write(f'Tidak terdapat korelasi signifikan antara {selected_column1} dan {selected_column2}.')

if __name__ == '__main__':
    main()
