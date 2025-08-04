import streamlit as st
from main import generate_pdf

def show_page():
    st.markdown("---")
    
    required_charts = [
        'odp_img_av', 'infra_img_av', 'oaf_img_av',
        'odp_img_co', 'infra_img_co', 'oaf_img_co',
        'razao_chart', 'percent_chart', 'curso_op', 'municipio_op'
    ]

    if all(key in st.session_state for key in required_charts):
            st.subheader(f"📄 Gerando relatório completo de {st.session_state['curso_op']} - {st.session_state['municipio_op']}")
        # if st.button("Gerar PDF"):
            pdf_path = generate_pdf()
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Baixar PDF",
                    data=f,
                    file_name= f"Relaório Análise dos Microdados Enade 2023 {st.session_state['curso_op']} - {st.session_state['municipio_op']} .pdf",
                    mime="application/pdf"
                )
    else:
        st.info("Os gráficos ainda não foram carregados completamente. Certifique-se de ter navegado pelas páginas anteriores para que todos os gráficos sejam carregados.")
