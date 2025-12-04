# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 12:40:43 2025

@author: USACH
"""

# ===========================================================
# app_streamlit_perdidas.py
# ===========================================================



import streamlit as st
import pandas as pd
from pathlib import Path

CARPETA_SALIDA = Path("salida_perdidas")
CARPETA_TABLAS = CARPETA_SALIDA / "tablas"
CARPETA_FIGS = CARPETA_SALIDA / "figuras"

#%%

# ============================================================
# CARGAR DATOS PRECALCULADOS
# ============================================================
@st.cache_data
def cargar_institucional():
    df_final = pd.read_parquet(CARPETA_SALIDA / "df_final.parquet")
    resumen_inst = pd.read_excel(CARPETA_TABLAS / "resumen_institucional.xlsx")
    figura_inst = CARPETA_FIGS / "panel_institucional.png"
    return df_final, resumen_inst, figura_inst


@st.cache_data
def cargar_resumen_facultad(fac):
    path_tabla = CARPETA_TABLAS / f"resumen_{fac}.xlsx"
    path_fig = CARPETA_FIGS / f"panel_{fac.replace(' ', '_')}.png"
    return pd.read_excel(path_tabla), path_fig

#%%

#%%

# ============================================================
# SISTEMA DE AUTENTICACIÓN SIMPLE (Opción A)
# ============================================================


PASSWORD = "usach2025"

def autenticar():
    """Bloque de autenticación antes de cargar el dashboard."""
    if "logueado" not in st.session_state:
        st.session_state.logueado = False

    if not st.session_state.logueado:
        st.title("🔒 Acceso restringido")
        st.write("Ingrese la contraseña para acceder al panel institucional:")

        pwd = st.text_input("Contraseña:", type="password")

        if st.button("Ingresar"):
            if pwd == PASSWORD:
                st.session_state.logueado = True
                st.rerun()  # <<
            else:
                st.error("❌ Contraseña incorrecta")

        st.stop()



#%%

# ============================================================
# DASHBOARD
# ============================================================
def main():
    autenticar()  # protege toda la app

    st.set_page_config(page_title="Pérdidas por Matrícula — USACH", layout="wide")

    st.title("📊 Déficit $ por aranceles y matrículas — USACH")

    # --------------------------
    # PANEL INSTITUCIONAL
    # --------------------------
    st.header("🔵 Panel Institucional")

    df_final, resumen_inst, fig_inst = cargar_institucional()

    st.subheader("Tabla institucional")
    st.dataframe(resumen_inst)
    
    ############################################################

    st.subheader("Panel institucional")

    # Columnas: figura a la izquierda, descripcion a la derecha
    col_fig, col_desc = st.columns([3, 1])

    with col_fig:
        st.image(str(fig_inst))

        # Botón de descarga de la figura institucional
        with open(fig_inst, "rb") as f:
            st.download_button(
                label="📥 Descargar figura institucional (PNG)",
                data=f,
                file_name="panel_institucional.png",
                mime="image/png"
            )

    with col_desc:
        st.markdown("""
        <div style="
            padding: 15px;
            border-radius: 8px;
            background-color: #f0f7ff;
            border: 1px solid #cbdaf1;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            font-size: 0.92rem;
        ">
        <h4 style="margin-top:0;">📘 Descripción del Panel Institucional</h4>

        <b>1. Déficit total institucional</b><br>
        Corresponde a la suma de las pérdidas por concepto de <i>matrícula</i> y <i>arancel</i>.<br>
        • La curva negra muestra montos en pesos (CLP).<br>
        • La curva azul muestra los mismos valores expresados en UF.<br>
        Los valores destacados corresponden al valor de la UF vigente al <b>31 de diciembre</b> de cada año.<br><br>

        <b>2. Pérdidas por arancel y matrícula</b><br>
        La curva verde representa las pérdidas asociadas al arancel, mientras que la curva naranja corresponde a las pérdidas por matrícula.<br><br>

        <b>3. Pérdida de estudiantes</b><br>
        Se indica el porcentaje de disminución de estudiantes entre el segundo y primer semestre, junto con el número total de estudiantes menos registrados en el año.*
        </div>
        """, unsafe_allow_html=True)

    # Línea divisoria elegante
    st.markdown("<hr style='border:0.5px solid #999; margin-top:25px; margin-bottom:25px;'>",
                unsafe_allow_html=True)
        

#########################################################################################################

    st.write("---")

    # --------------------------
    # PANEL POR FACULTAD
    # --------------------------
    st.header("🏛️ Panel por Facultad")

    facultades = sorted(df_final["FACULTAD"].dropna().unique())
    facultades = [f for f in facultades if f != "999"]

    fac = st.selectbox("Selecciona una facultad:", facultades)

    if fac:
        tabla, fig = cargar_resumen_facultad(fac)

        st.subheader("Tabla")
        st.dataframe(tabla)

        st.subheader("Figura")
        st.image(str(fig))



#%%

if __name__ == "__main__":
    main()

















