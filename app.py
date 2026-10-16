import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Riconoscitore Monete", page_icon="🪙", layout="centered")

st.title("🪙 Analizzatore di Monete")
st.write("Scatta o carica una foto della tua moneta per scoprirne la storia, il valore e la rarità.")

# Recupero della chiave API dai segreti di Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Chiave API non trovata! Inseriscila nei Secrets di Streamlit.")
    st.stop()

# Inizializzazione del client Gemini
client = genai.Client(api_key=api_key)

# Opzione per scattare foto o caricarla
scelta = st.radio("Come vuoi inserire l'immagine?", ("Usa la Fotocamera", "Carica una foto dalla Galleria"))

immagine_caricata = None

if scelta == "Usa la Fotocamera":
    foto = st.camera_input("Scatta una foto chiara della moneta")
    if foto:
        immagine_caricata = Image.open(foto)
else:
    file = st.file_uploader("Scegli un'immagine...", type=["jpg", "jpeg", "png"])
    if file:
        immagine_caricata = Image.open(file)

if immagine_caricata is not None:
    st.image(immagine_caricata, caption="Moneta acquisita", use_container_width=True)
    
    if st.button("🔍 Analizza Moneta", type="primary"):
        with st.spinner("Analisi in corso... L'AI sta esaminando i dettagli della moneta..."):
            try:
                # Prompt dettagliato per l'analisi numismatica
                prompt = """
                Sei un esperto numismatico professionista. Analizza l'immagine fornita ed estrai le seguenti informazioni in modo chiaro e strutturato in lingua italiana:

                1. **Identificazione Generale:** Paese di origine, Valore nominale, Anno di conio presunto.
                2. **Descrizione e Dettagli:** Cosa raffigura la moneta (fronte e retro se visibili) e dettagli particolari (es. segno di zecca).
                3. **Contesto Storico:** Breve storia o curiosità legata a questa specifica moneta o emissione.
                4. **Rarità:** Grado di rarità stimato (es. Comune, Non Comune, Rara, Molto Rara) e indicazione della tiratura se nota.
                5. **Stato di Conservazione Presunto:** Stima visiva dello stato (es. BB, SPL, FDC) con avvertenza sulla precisione da foto.
                6. **Valore di Mercato Attuale:** Stima del valore commerciale indicativo per i collezionisti (espresso in Euro), specificando la forbice di prezzo dal valore minimo a quello massimo.

                Sii preciso e professionale. Se l'immagine è sfuocata o non permette una certezza assoluta, segnalalo chiaramente.
                """
                
                # Chiamata al modello Gemini 1.5 Flash
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=[immagine_caricata, prompt]
                )
                
                st.success("Analisi Completata!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Si è verificato un errore durante l'analisi: {e}")
