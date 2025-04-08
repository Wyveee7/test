        # Gerar Excel em memória
        from io import BytesIO

        def gerar_excel(df):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Quadro de Aço')
            buffer.seek(0)
            return buffer

        excel_buffer = gerar_excel(tabela)

        # Botão de download para Excel
        st.download_button(
            label="📊 Baixar Excel",
            data=excel_buffer,
            file_name="quadro_aco.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
