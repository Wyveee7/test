import streamlit as st
import ezdxf
import tempfile
import pandas as pd
from io import BytesIO
from dwg_reader import extrair_quadro_aco_formatado

st.set_page_config(page_title="Assistente de Aço", layout="centered")
st.title("🧱 Assistente de Leitura de Quadro de Aço")
st.markdown("Envie um arquivo `.dxf` com a tabela de aço no formato padrão.")

arquivo = st.file_uploader("📤 Envie um arquivo .dxf", type=["dxf"])

if arquivo is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
            tmp.write(arquivo.read())
            tmp_path = tmp.name

        tabela = extrair_quadro_aco_formatado(tmp_path)
        st.success("✅ Quadro de aço extraído com sucesso!")
        st.dataframe(tabela)

        # Botão de download CSV
        csv = tabela.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Baixar CSV",
            data=csv,
            file_name="quadro_aco.csv",
            mime="text/csv"
        )

        # Função para gerar o Excel em memória
        def gerar_excel(df):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Quadro de Aço')
            buffer.seek(0)
            return buffer

        excel_buffer = gerar_excel(tabela)

        # Botão de download Excel
        st.download_button(
            label="📊 Baixar Excel",
            data=excel_buffer,
            file_name="quadro_aco.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
