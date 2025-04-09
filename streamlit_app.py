
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import io

# Funzione per estrarre testo da PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Funzione per creare file Excel
def create_excel_file():
    # Dati di esempio per questa demo
    revoca_utilizzato = 0
    revoca_accordato = 132

    autoliquidanti_utilizzato = 0
    autoliquidanti_accordato = 0

    scadenza_utilizzato = 42276 + 295555 + 258047
    scadenza_accordato = scadenza_utilizzato

    def calc_ratio(utilizzato, accordato):
        return round((utilizzato / accordato * 100), 2) if accordato > 0 else 0

    df_rischi = pd.DataFrame([
        {
            "Tipo Rischio": "A Revoca",
            "Accordato": revoca_accordato,
            "Utilizzato": revoca_utilizzato,
            "Utilizzato/Accordato %": calc_ratio(revoca_utilizzato, revoca_accordato)
        },
        {
            "Tipo Rischio": "Autoliquidanti",
            "Accordato": autoliquidanti_accordato,
            "Utilizzato": autoliquidanti_utilizzato,
            "Utilizzato/Accordato %": calc_ratio(autoliquidanti_utilizzato, autoliquidanti_accordato)
        },
        {
            "Tipo Rischio": "A Scadenza",
            "Accordato": scadenza_accordato,
            "Utilizzato": scadenza_utilizzato,
            "Utilizzato/Accordato %": calc_ratio(scadenza_utilizzato, scadenza_accordato)
        }
    ])

    df_extra = pd.DataFrame([
        {
            "Numero Richieste Finanziamento Ultimi 6 Mesi": 3,
            "Numero Enti Affidanti Febbraio": 2,
            "Mesi con Sconfinamenti > 100€ (ultimi 12 mesi)": 0
        }
    ])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_rischi.to_excel(writer, sheet_name="Riepilogo Rischi", index=False)
        df_extra.to_excel(writer, sheet_name="Info Generali", index=False)
    output.seek(0)
    return output

# Interfaccia utente Streamlit
st.title("Analizzatore Centrale Rischi")

st.write("Carica il PDF della Centrale Rischi per generare un report Excel automatico.")

uploaded_file = st.file_uploader("Carica il file PDF", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    st.subheader("Contenuto estratto (anteprima)")
    st.text(text[:500])  # Mostra solo i primi 500 caratteri per anteprima

    if st.button("Genera Report Excel"):
        excel_buffer = create_excel_file()
        st.success("Report pronto!")
        st.download_button(
            label="Scarica Excel",
            data=excel_buffer,
            file_name="Analisi_Centrale_Rischi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
