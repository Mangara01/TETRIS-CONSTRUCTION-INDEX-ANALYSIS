import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

df_pekerja_tetap = pd.read_csv('Indeks Tahunan Pekerja Tetap Konstruksi.csv')
df_harian_pekerja = pd.read_csv('Indeks Tahunan Hari Orang Pekerja Harian Perusahaan Konstruksi.csv')
df_balas_jasa = pd.read_csv('Indeks Tahunan Balas Jasa Pekerja Tetap dan Upah Pekerja Harian Konstruksi.csv')
df_nilai_konstruksi = pd.read_csv('Indeks Tahunan Nilai Konstruksi yang Diselesaikan Perusahaan Konstruksi.csv')
df_covid = pd.read_csv('WHO-COVID-19-global-data.csv')

def process_data(df):
    unique_provinces = df['Provinsi'].str.upper().unique()
    unique_provinces = [province for province in unique_provinces if province != 'INDONESIA']
    rata_rata = {province: df[df['Provinsi'].str.upper() == province].iloc[:, 1:].mean() for province in unique_provinces}
    return pd.DataFrame(rata_rata)

df_rata_rata_pekerja_tetap = process_data(df_pekerja_tetap)
df_rata_rata_harian_pekerja = process_data(df_harian_pekerja)
df_rata_rata_balas_jasa = process_data(df_balas_jasa)
df_rata_rata_nilai_konstruksi = process_data(df_nilai_konstruksi)

kepulauan_mapping = {
    'Sumatera': ['ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG', 'KEP. BANGKA BELITUNG', 'KEP. RIAU'],
    'Jawa': ['DKI JAKARTA', 'JAWA BARAT', 'JAWA TENGAH', 'DI YOGYAKARTA', 'JAWA TIMUR', 'BANTEN'],
    'Kalimantan': ['KALIMANTAN BARAT', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 'KALIMANTAN TIMUR', 'KALIMANTAN UTARA'],
    'Sulawesi': ['SULAWESI UTARA', 'SULAWESI TENGAH', 'SULAWESI SELATAN', 'SULAWESI TENGGARA', 'GORONTALO', 'SULAWESI BARAT'],
    'Bali & Nusa Tenggara': ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR'],
    'Maluku & Papua': ['MALUKU', 'MALUKU UTARA', 'PAPUA BARAT', 'PAPUA'],
}

def process_datas(df, kepulauan_mapping):
    rata_rata = {}
    for kepulauan, provinsi_list in kepulauan_mapping.items():
        rata_rata[kepulauan] = df[df['Provinsi'].isin(provinsi_list)].iloc[:, 1:].mean()
    return pd.DataFrame(rata_rata)

df_rata_rata_pekerja_tetaps = process_datas(df_pekerja_tetap, kepulauan_mapping)
df_rata_rata_harian_pekerjas = process_datas(df_harian_pekerja, kepulauan_mapping)
df_rata_rata_balas_jasas = process_datas(df_balas_jasa, kepulauan_mapping)
df_rata_rata_nilai_konstruksis = process_datas(df_nilai_konstruksi, kepulauan_mapping)

def main():

    st.set_page_config(
        page_title="Analisis Indeks Kinerja Sektor Konstruksi",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    tdf = pd.concat([df_rata_rata_pekerja_tetap.T.mean(), df_rata_rata_harian_pekerja.T.mean(), df_rata_rata_balas_jasa.T.mean(), df_rata_rata_nilai_konstruksi.T.mean()], axis=1)
    tdf.columns = ['Pekerja Tetap', 'Harian Pekerja', 'Balas Jasa', 'Nilai Konstruksi']
    
    pudf = pd.concat([df_rata_rata_pekerja_tetaps.mean(), df_rata_rata_harian_pekerjas.mean(), df_rata_rata_balas_jasas.mean(), df_rata_rata_nilai_konstruksis.mean()], axis=1)
    pudf.columns = ['Pekerja Tetap', 'Harian Pekerja', 'Balas Jasa', 'Nilai Konstruksi']

    prdf = pd.concat([df_rata_rata_pekerja_tetap.mean(), df_rata_rata_harian_pekerja.mean(), df_rata_rata_balas_jasa.mean(), df_rata_rata_nilai_konstruksi.mean()], axis=1)
    prdf.columns = ['Pekerja Tetap', 'Harian Pekerja', 'Balas Jasa', 'Nilai Konstruksi']

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
    tdfc.columns = ['Pekerja Tetap', 'Harian Pekerja', 'Balas Jasa', 'Nilai Konstruksi', 'Kasus COVID', 'Korban COVID']
    
    st.title('Analisis Indeks Kinerja Sektor Konstruksi')
    page = st.sidebar.radio("**Go to:**", ("Pendahuluan :rocket:", "Analisis :bar_chart:", "Hipotesa :bulb:", "Kesimpulan & Saran :open_book:"))

    # Pendahuluan
    if page == "Pendahuluan :rocket:":
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
    elif page == "Analisis :bar_chart:":
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure(figsize=(10, 6))
        st.subheader('Tren Indeks Kinerja Sektor Konstruksi Antar Tahun')

        year_range = st.slider('Pilih Tahun', min_value=2013, max_value=2022, value=(2013, 2022))
        ftdf = tdf.loc[(tdf.index >= str(year_range[0])) & (tdf.index <= str(year_range[1]))]
        plt.figure(figsize=(12, 6))
        for column in ftdf.columns:
            plt.plot(ftdf[column], marker='o', label=column)
        plt.title('Tren Rata-rata Data Konstruksi per Tahun')
        plt.xlabel('Tahun')
        plt.ylabel('Index')
        plt.grid(True)
        plt.legend(title='Keterangan:', loc='lower right')
        plt.tight_layout()
        st.pyplot()
            
        selected_table = st.selectbox('Pilih Tabel', ['Pekerja Tetap', 'Harian Pekerja', 'Balas Jasa', 'Nilai Konstruksi'])
    
        if selected_table == 'Pekerja Tetap':
            data = df_rata_rata_pekerja_tetap  
        elif selected_table == 'Harian Pekerja':
            data = df_rata_rata_harian_pekerja
        elif selected_table == 'Balas Jasa':
            data = df_rata_rata_balas_jasa
        else:
            data = df_rata_rata_nilai_konstruksi
                
        year_ranges = st.slider('Pilih Tahun', min_value=2013, max_value=2022, value=(2013, 2022), key="year_slider")
        selected_columns = st.selectbox('Pilih Provinsi', data.columns)
        datas = data.loc[(data.index >= str(year_ranges[0])) & (data.index <= str(year_ranges[1]))]
        plt.figure(figsize=(12, 6))
        plt.plot(datas[selected_columns], marker='o', label=selected_table)
        plt.title(f'Tren Rata-rata Data Konstruksi {selected_columns} per Tahun')
        plt.xlabel('Tahun')
        plt.ylabel('Index')
        plt.grid(True)
        plt.legend(title='Keterangan:', loc='lower right')
        plt.tight_layout()
        st.pyplot()
            
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

        st.subheader('Tren Indeks Kinerja Sektor Konstruksi Antar Pulau')

        categories = pudf.index.unique()
        selected_categories = st.multiselect('Pilih Pulau', categories)
        if selected_categories:
            fpudf = pudf.loc[pudf.index.isin(selected_categories)]
            plt.figure(figsize=(12, 6))
            fpudf.sort_index(ascending=False).plot(kind='bar', rot=0, figsize=(12, 6))
            plt.title('Tren Rata-rata Data Konstruksi per Pulau')
            plt.xlabel('Pulau')
            plt.ylabel('Index')
            plt.grid(True)
            plt.legend(title='Keterangan:', loc='lower right')
            plt.tight_layout()
            st.pyplot()
        else:
            st.markdown("Untuk menampilkan grafik, **Pilih Pulau** terlebih dahulu !")

        categories = prdf.index.unique()
        selected_categories = st.multiselect('Pilih Provinsi', categories)
        if selected_categories:
            fprdf = prdf.loc[prdf.index.isin(selected_categories)]
            plt.figure(figsize=(12, 6))
            fprdf.sort_index(ascending=False).plot(kind='bar', rot=0, figsize=(12, 6))
            plt.title('Tren Rata-rata Data Konstruksi per Provinsi')
            plt.xlabel('Provinsi')
            plt.ylabel('Index')
            plt.grid(True)
            plt.legend(title='Keterangan:', loc='lower right')
            plt.tight_layout()
            st.pyplot()
        else:
            st.markdown("Untuk menampilkan grafik, **Pilih Provinsi** terlebih dahulu !")

        st.markdown('''
        Melalui analisis ini, terdapat beberapa pola yang muncul:
        * Jawa memiliki kinerja yang relatif tinggi dalam semua kategori, menunjukkan potensi besar dalam sektor konstruksi.
        * Pulau Kalimantan juga menonjol dalam beberapa aspek, khususnya dalam jumlah pekerja harian dan balas jasa.
        * Sulawesi memiliki kinerja yang lebih rendah dibandingkan dengan pulau lain dalam hal pekerjaan harian dan nilai konstruksi.
            
        Analisis ini dapat memberikan wawasan bagi pembuat kebijakan, investor, dan praktisi industri konstruksi untuk mengidentifikasi area di mana perhatian lebih lanjut atau investasi mungkin diperlukan untuk mengembangkan sektor konstruksi di berbagai pulau di Indonesia sesuai dengan karakteristik dan kebutuhan masing-masing wilayah.
        ''')

    # Uji Hipotesa
    elif page == "Hipotesa :bulb:":
        st.subheader('Uji Hipotesis: Korelasi antara Tren Konstruksi dengan COVID')

        st.markdown('**Note**: Data COVID hanya tersedia untuk Tren Kinerja Sektor Konstruksi Antar Tahun')
        selected_table = st.selectbox('Pilih Tabel', ['Tren Kinerja Sektor Konstruksi Antar Tahun', 'Tren Kinerja Sektor Konstruksi Antar Pulau'])
    
        if selected_table == 'Tren Kinerja Sektor Konstruksi Antar Tahun':
            data = tdfc
        else:
            data = pudf
    
        selected_column1 = st.selectbox('Pilih Kolom Pertama', data.columns)
        selected_column2 = st.selectbox('Pilih Kolom Kedua', data.columns)
    
        pearson_corr, p_value = pearsonr(data[selected_column1], data[selected_column2])
    
        st.subheader('Hasil Uji Hipotesis')
        st.write(f'Koefisien Korelasi Pearson: {pearson_corr}')
    
        if pearson_corr > 0.4:
            st.write(f'Terdapat korelasi antara {selected_column1} dan {selected_column2}.')
        else:
            st.write(f'Tidak terdapat korelasi antara {selected_column1} dan {selected_column2}.')

    # Kesimpulan & Saran
    if page == "Kesimpulan & Saran :open_book:":
        st.subheader('Kesimpulan')
        st.markdown('''
        * Tren positif dalam sektor konstruksi, ditandai dengan peningkatan indeks dari tahun ke tahun, menunjukkan stabilitas dan pertumbuhan yang berkelanjutan dalam industri ini.
        * Meskipun terjadi penurunan pada tahun 2020 karena dampak pandemi COVID, sektor konstruksi telah mampu pulih secara signifikan, menunjukkan ketangguhan dan adaptabilitas industri terhadap tantangan eksternal.
        * Adanya konsistensi dalam indeks antar pulau dan antar provinsi menunjukkan bahwa perubahan kondisi ekonomi atau faktor-faktor regional tidak secara signifikan mempengaruhi sektor konstruksi secara berbeda di berbagai wilayah.
        ''')
        st.subheader('Saran')
        st.markdown('''
        * Mengoptimalkan investasi dalam pelatihan dan pengembangan tenaga kerja untuk memastikan bahwa tenaga kerja dalam sektor konstruksi tetap relevan dan berkualitas tinggi dalam menghadapi perubahan teknologi dan tuntutan pasar yang terus berkembang.
        * Memperkuat infrastruktur komunikasi dan transportasi antar pulau dan antar provinsi untuk mendukung pertumbuhan sektor konstruksi dengan memastikan aksesibilitas yang lebih baik dan distribusi sumber daya yang lebih efisien.
        * Menetapkan kebijakan dan kerangka kerja yang mempromosikan kolaborasi antara pemerintah pusat, pemerintah daerah, dan sektor swasta untuk meningkatkan koordinasi dan efektivitas dalam pelaksanaan proyek konstruksi lintas wilayah.
        ''')

if __name__ == '__main__':
    main()
