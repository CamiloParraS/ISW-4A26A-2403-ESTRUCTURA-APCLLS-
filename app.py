"""
app.py — Healcia · Peciatech
Frontend Streamlit — interfaz en espanol
Run with:  streamlit run app.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from models.patient import Patient
from models.doctor import Doctor
from models.action import Action
from services.bed_service import BedService
from services.waiting_room_service import WaitingRoomService
from services.undo_service import UndoService
from services.staff_service import StaffService
from services.patient_history_service import PatientHistoryService

# ─── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Healcia · Peciatech",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Design tokens ────────────────────────────────────────────────────────────
# Military green palette — muted, professional, minimal rounding

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
}
.main .block-container {
    background: #ECEEE8;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}

/* ── Header ── */
.hc-header {
    background: #2B3625;
    padding: 1rem 1.8rem;
    border-radius: 4px;
    margin-bottom: 1.4rem;
    border-left: 4px solid #7A9B5E;
    box-shadow: 2px 2px 0 rgba(0,0,0,0.18);
}
.hc-header h1 {
    color: #D6DDD0;
    margin: 0 0 2px 0;
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.hc-header p {
    color: #7A9B5E;
    margin: 0;
    font-size: 0.78rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* ── KPI cards ── */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.4rem; }
.kpi-card {
    background: #F7F8F5;
    border: 1px solid #C4CAB8;
    border-top: 3px solid #4A5C3F;
    border-radius: 3px;
    padding: 0.9rem 1.1rem;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.10);
}
.kpi-card.danger  { border-top-color: #7A3030; }
.kpi-card.amber   { border-top-color: #7A6030; }
.kpi-card.neutral { border-top-color: #4A5468; }
.kpi-card h3 {
    margin: 0 0 2px 0;
    font-size: 2rem;
    font-weight: 700;
    color: #2B3625;
    line-height: 1;
}
.kpi-card p {
    margin: 0;
    font-size: 0.7rem;
    color: #6B7560;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
}

/* ── Section label ── */
.sec-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #6B7560;
    border-bottom: 1px solid #C4CAB8;
    padding-bottom: 5px;
    margin: 0 0 0.9rem 0;
}

/* ── Bed grid ── */
.bed-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-bottom: 1.2rem;
}
.bed-card {
    border: 1px solid #C4CAB8;
    border-radius: 3px;
    padding: 0.65rem 0.5rem;
    text-align: center;
    font-size: 0.72rem;
    font-weight: 600;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.08);
    line-height: 1.4;
}
.bed-free     { background: #EBF0E5; border-color: #8AAD72; color: #3A5028; }
.bed-occupied { background: #F0E8E8; border-color: #B07070; color: #6B2020; }
.bed-number   { font-size: 0.65rem; color: #8A9B7A; font-weight: 400; display: block; margin-bottom: 2px; }
.bed-status   { font-size: 0.7rem; font-weight: 700; }
.bed-name     { font-size: 0.65rem; color: #6B2020; font-weight: 400; }

/* ── Queue rows ── */
.queue-row {
    background: #F7F8F5;
    border: 1px solid #C4CAB8;
    border-left: 3px solid #4A5C3F;
    border-radius: 3px;
    padding: 0.55rem 0.9rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.85rem;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.07);
}
.queue-pos { color: #8A9B7A; font-size: 0.72rem; font-family: 'DM Mono', monospace; min-width: 24px; }
.queue-name { font-weight: 600; color: #2B3625; flex: 1; }
.queue-meta { color: #8A9B7A; font-size: 0.72rem; font-family: 'DM Mono', monospace; }

/* ── Priority badge ── */
.badge {
    display: inline-block;
    padding: 1px 7px;
    border-radius: 2px;
    font-size: 0.68rem;
    font-weight: 700;
    color: #F7F8F5;
    letter-spacing: 0.3px;
    font-family: 'DM Mono', monospace;
}

/* ── Action log ── */
.log-row {
    background: #F7F8F5;
    border: 1px solid #C4CAB8;
    border-left: 3px solid #6B7560;
    border-radius: 3px;
    padding: 0.45rem 0.85rem;
    margin-bottom: 5px;
    font-size: 0.82rem;
    color: #2B3625;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.log-type {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #8A9B7A;
    background: #E5E8DF;
    border-radius: 2px;
    padding: 1px 6px;
}
.log-time {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #A0AB90;
}

/* ── Intervention chain ── */
.chain-wrap { display: flex; flex-wrap: wrap; align-items: center; gap: 5px; margin: 0.6rem 0 1rem; }
.chain-step {
    background: #E5EAE0;
    color: #2B3625;
    border: 1px solid #B0BCA5;
    border-radius: 2px;
    padding: 3px 9px;
    font-size: 0.76rem;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
}
.chain-arrow { color: #8A9B7A; font-size: 0.75rem; font-weight: 700; }

/* ── Doctor card ── */
.doc-card {
    background: #F7F8F5;
    border: 1px solid #C4CAB8;
    border-top: 3px solid #4A5C3F;
    border-radius: 3px;
    padding: 0.85rem;
    margin-bottom: 8px;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.08);
}
.doc-name { font-weight: 700; color: #2B3625; font-size: 0.9rem; }
.doc-spec { color: #6B7560; font-size: 0.78rem; margin: 2px 0; }
.doc-id   { color: #A0AB90; font-size: 0.68rem; font-family: 'DM Mono', monospace; }

/* ── Action buttons ── */
.stButton > button {
    background: #3D4F33 !important;
    color: #D6DDD0 !important;
    border: 1px solid #2B3625 !important;
    border-radius: 3px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 1.1rem !important;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.20) !important;
    letter-spacing: 0.2px;
    transition: background 0.15s;
}
.stButton > button:hover {
    background: #2B3625 !important;
    color: #C8D5B0 !important;
}
.stButton > button:active {
    box-shadow: none !important;
    transform: translateY(1px);
}

/* ── Inputs ── */
.stTextInput input, .stSelectbox > div > div, .stNumberInput input {
    border-radius: 3px !important;
    border-color: #B0BCA5 !important;
    background: #F7F8F5 !important;
    color: #2B3625 !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus, .stSelectbox > div > div:focus-within {
    border-color: #4A5C3F !important;
    box-shadow: 0 0 0 2px rgba(74,92,63,0.15) !important;
}

/* ── Tabs ── */
div[data-testid="stTabs"] button {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
    color: #6B7560 !important;
    border-radius: 0 !important;
    padding: 0.5rem 1rem !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2B3625 !important;
    border-bottom: 2px solid #4A5C3F !important;
}

/* ── Alerts ── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 3px !important;
    font-size: 0.83rem !important;
    box-shadow: 1px 1px 0 rgba(0,0,0,0.08) !important;
}

/* ── Sidebar collapse ── */
div[data-testid="collapsedControl"] { display: none !important; }

/* ── Divider ── */
hr { border-color: #C4CAB8 !important; margin: 1rem 0 !important; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ─── Session state init ───────────────────────────────────────────────────────

def _init_state() -> None:
    defaults = {
        "bed_svc":     BedService(15),
        "wait_svc":    WaitingRoomService(),
        "undo_svc":    UndoService(),
        "staff_svc":   StaffService(),
        "history_svc": PatientHistoryService(),
        "pid_counter": 1,
        "did_counter": 1,
        "toast":       None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_state()

bed_svc:     BedService            = st.session_state.bed_svc
wait_svc:    WaitingRoomService    = st.session_state.wait_svc
undo_svc:    UndoService           = st.session_state.undo_svc
staff_svc:   StaffService          = st.session_state.staff_svc
history_svc: PatientHistoryService = st.session_state.history_svc


def _next_pid() -> str:
    pid = f"P{st.session_state.pid_counter:04d}"
    st.session_state.pid_counter += 1
    return pid


def _next_did() -> str:
    did = f"D{st.session_state.did_counter:04d}"
    st.session_state.did_counter += 1
    return did


def _toast(kind: str, msg: str) -> None:
    st.session_state.toast = (kind, msg)


def _priority_color(level: int) -> str:
    return {1: "#7A3030", 2: "#9B5A20", 3: "#7A7020", 4: "#3A5C30", 5: "#2E4A68"}.get(level, "#6B7560")


# ─── Modals ───────────────────────────────────────────────────────────────────

@st.dialog("Registrar nuevo paciente")
def modal_add_patient() -> None:
    p_name = st.text_input("Nombre completo")
    col1, col2 = st.columns(2)
    with col1:
        p_age = st.number_input("Edad", 0, 120, 30)
    with col2:
        p_priority = st.selectbox(
            "Nivel de triage",
            [1, 2, 3, 4, 5],
            format_func=lambda x: {
                1: "N1 - Resucitacion",
                2: "N2 - Emergencia",
                3: "N3 - Urgente",
                4: "N4 - Menos urgente",
                5: "N5 - No urgente",
            }[x],
        )
    p_dest = st.radio(
        "Destino",
        ["Cola de espera (Nivel 4-5)", "UCI (asignar cama)"],
        horizontal=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Registrar", use_container_width=True):
            if not p_name.strip():
                st.error("El nombre es obligatorio.")
            else:
                pid     = _next_pid()
                patient = Patient(pid, p_name.strip(), int(p_age), p_priority)
                if "Cola" in p_dest:
                    if p_priority not in (4, 5):
                        st.error("La cola general es para niveles 4 y 5 unicamente.")
                    else:
                        wait_svc.add_patient(patient)
                        history_svc.add_intervention(pid, "Triage")
                        undo_svc.record(Action("ADD_QUEUE", f"Paciente {p_name} anadido a cola",
                                               restore_data={"patient_id": pid}))
                        _toast("success", f"Paciente {p_name} registrado en cola (ID: {pid}).")
                        st.rerun()
                else:
                    idx = bed_svc.first_free_index()
                    if idx is None:
                        st.error("No hay camas libres en la UCI.")
                    else:
                        bed_svc.admit_to_bed(idx, patient)
                        history_svc.add_intervention(pid, "Triage")
                        undo_svc.record(Action("ADMIT_BED", f"Paciente {p_name} admitido en cama {idx + 1}",
                                               restore_data={"bed_index": idx, "patient_id": pid}))
                        _toast("success", f"Paciente {p_name} asignado a cama UCI #{idx + 1} (ID: {pid}).")
                        st.rerun()
    with col_b:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()


@st.dialog("Agregar doctor al turno")
def modal_add_doctor() -> None:
    d_name      = st.text_input("Nombre completo")
    d_specialty = st.text_input("Especialidad")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Agregar", use_container_width=True):
            if not d_name.strip():
                st.error("El nombre es obligatorio.")
            else:
                doc = Doctor(_next_did(), d_name.strip(), d_specialty.strip() or "General")
                if staff_svc.add_doctor(doc):
                    _toast("success", f"Dr(a). {d_name} anadido al turno.")
                    st.rerun()
                else:
                    st.error("El doctor ya se encuentra en el sistema.")
    with col_b:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()


@st.dialog("Registrar intervencion")
def modal_add_intervention() -> None:
    all_pids = history_svc.all_patient_ids()
    if not all_pids:
        st.warning("No hay pacientes con historial registrado.")
        if st.button("Cerrar"):
            st.rerun()
        return

    pid_sel = st.selectbox("ID de paciente", all_pids)
    procedure = st.selectbox("Procedimiento", [
        "Triage", "Examen de sangre", "Rayos X", "Ecografia",
        "Electrocardiograma", "Diagnostico", "Prescripcion",
        "Cirugia menor", "Alta medica",
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Registrar", use_container_width=True):
            history_svc.add_intervention(pid_sel, procedure)
            undo_svc.record(Action("ADD_INTERVENTION", f"Intervencion '{procedure}' a {pid_sel}",
                                   restore_data={"patient_id": pid_sel, "procedure": procedure}))
            _toast("success", f"Intervencion '{procedure}' registrada para {pid_sel}.")
            st.rerun()
    with col_b:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()


# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hc-header">
  <h1>Healcia</h1>
  <p>Sistema de Triage y Flujo de Sala de Urgencias &nbsp;·&nbsp; Peciatech</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.toast:
    kind, msg = st.session_state.toast
    {"success": st.success, "error": st.error, "warning": st.warning, "info": st.info}[kind](msg)
    st.session_state.toast = None

# ─── KPI row ──────────────────────────────────────────────────────────────────

st.markdown(
    f"""<div class="kpi-row">
      <div class="kpi-card"><h3>{bed_svc.free_count()}</h3><p>Camas libres UCI</p></div>
      <div class="kpi-card danger"><h3>{bed_svc.occupied_count()}</h3><p>Camas ocupadas UCI</p></div>
      <div class="kpi-card amber"><h3>{wait_svc.count()}</h3><p>Pacientes en espera</p></div>
      <div class="kpi-card neutral"><h3>{staff_svc.count()}</h3><p>Personal de turno</p></div>
    </div>""",
    unsafe_allow_html=True,
)

# ─── Main action bar ──────────────────────────────────────────────────────────

bar_c1, bar_c2, bar_c3, bar_c4 = st.columns([1, 1, 1, 3])
with bar_c1:
    if st.button("Nuevo paciente", use_container_width=True):
        modal_add_patient()
with bar_c2:
    if st.button("Agregar doctor", use_container_width=True):
        modal_add_doctor()
with bar_c3:
    if st.button("Nueva intervencion", use_container_width=True):
        modal_add_intervention()

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Camas UCI",
    "Cola de Espera",
    "Historial Paciente",
    "Personal Medico",
    "Registro de Acciones",
])


# ── Tab 1: UCI Beds ───────────────────────────────────────────────────────────

with tab1:
    st.markdown('<div class="sec-label">Unidad de Cuidados Intensivos — Array de 15 camas</div>', unsafe_allow_html=True)

    beds     = bed_svc.all_beds()
    bed_html = '<div class="bed-grid">'
    for i, patient in enumerate(beds):
        if patient is None:
            bed_html += (
                f'<div class="bed-card bed-free">'
                f'<span class="bed-number">CAMA {i + 1}</span>'
                f'<span class="bed-status">Libre</span>'
                f'</div>'
            )
        else:
            bed_html += (
                f'<div class="bed-card bed-occupied">'
                f'<span class="bed-number">CAMA {i + 1}</span>'
                f'<span class="bed-name">{patient.name[:13]}</span>'
                f'<span class="bed-status">N{patient.priority_level}</span>'
                f'</div>'
            )
    bed_html += '</div>'
    st.markdown(bed_html, unsafe_allow_html=True)

    st.markdown('<div class="sec-label" style="margin-top:1.2rem">Dar de alta</div>', unsafe_allow_html=True)

    occupied = [(i, b) for i, b in enumerate(beds) if b is not None]
    if occupied:
        opts    = {f"Cama {i + 1}  —  {b.name}  ({b.patient_id})": i for i, b in occupied}
        col_sel, col_btn = st.columns([3, 1])
        with col_sel:
            sel = st.selectbox("Seleccionar cama ocupada", list(opts.keys()), label_visibility="collapsed")
        with col_btn:
            if st.button("Dar de alta", use_container_width=True):
                idx     = opts[sel]
                patient = bed_svc.discharge_from_bed(idx)
                undo_svc.record(Action("DISCHARGE", f"Alta de {patient.name} cama {idx + 1}",
                                       restore_data={"bed_index": idx}))
                _toast("success", f"Paciente {patient.name} dado de alta de cama #{idx + 1}.")
                st.rerun()
    else:
        st.info("No hay pacientes en UCI actualmente.")


# ── Tab 2: Waiting Queue ──────────────────────────────────────────────────────

with tab2:
    col_hdr, col_btn = st.columns([4, 1])
    with col_hdr:
        st.markdown('<div class="sec-label">Sala de Espera — Cola FIFO, niveles 4 y 5</div>', unsafe_allow_html=True)
    with col_btn:
        if st.button("Llamar siguiente", use_container_width=True):
            patient = wait_svc.call_next_patient()
            if patient:
                history_svc.add_intervention(patient.patient_id, "Consulta medica")
                undo_svc.record(Action("CALL_PATIENT", f"Paciente {patient.name} llamado",
                                       restore_data={"patient_id": patient.patient_id}))
                _toast("success", f"Llamando a {patient.name} ({patient.patient_id}).")
            else:
                _toast("warning", "La sala de espera esta vacia.")
            st.rerun()

    queue_list = wait_svc.queue_list()
    if not queue_list:
        st.info("La sala de espera esta vacia.")
    else:
        for pos, p in enumerate(queue_list):
            color = _priority_color(p.priority_level)
            st.markdown(
                f'<div class="queue-row">'
                f'<span class="queue-pos">{pos + 1:02d}</span>'
                f'<span class="badge" style="background:{color}">N{p.priority_level}</span>'
                f'<span class="queue-name">{p.name}</span>'
                f'<span class="queue-meta">{p.patient_id} &nbsp;|&nbsp; {p.age} anos &nbsp;|&nbsp; {p.arrival_time}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Tab 3: Patient History ────────────────────────────────────────────────────

with tab3:
    col_hdr3, col_btn3 = st.columns([4, 1])
    with col_hdr3:
        st.markdown('<div class="sec-label">Historial de Intervenciones — Lista Simple Enlazada</div>', unsafe_allow_html=True)
    with col_btn3:
        if st.button("Nueva intervencion ", use_container_width=True):
            modal_add_intervention()

    all_pids = history_svc.all_patient_ids()

    if not all_pids:
        st.info("No hay historiales registrados todavia.")
    else:
        sel_pid = st.selectbox("Seleccionar paciente", all_pids, key="hist_pid_sel")

        all_bed_patients   = [b for b in bed_svc.all_beds() if b is not None]
        all_queue_patients = wait_svc.queue_list()
        all_patients       = {p.patient_id: p for p in all_bed_patients + all_queue_patients}

        if sel_pid in all_patients:
            p = all_patients[sel_pid]
            cols_p = st.columns(3)
            with cols_p[0]:
                st.markdown(f"**Paciente**<br><span style='color:#4A5C3F;font-weight:700'>{p.name}</span>", unsafe_allow_html=True)
            with cols_p[1]:
                st.markdown(f"**Edad**<br>{p.age} anos", unsafe_allow_html=True)
            with cols_p[2]:
                st.markdown(f"**Triage**<br>{p.priority_label()}", unsafe_allow_html=True)

        history = history_svc.get_history(sel_pid)
        if history:
            chain_html = '<div class="chain-wrap">'
            for i, step in enumerate(history):
                chain_html += f'<span class="chain-step">{step}</span>'
                if i < len(history) - 1:
                    chain_html += '<span class="chain-arrow">&#8594;</span>'
            chain_html += '</div>'
            st.markdown(chain_html, unsafe_allow_html=True)
        else:
            st.info("Sin intervenciones registradas para este paciente.")


# ── Tab 4: Medical Staff ──────────────────────────────────────────────────────

with tab4:
    col_hdr4, col_srch, col_btn4 = st.columns([2, 2, 1])
    with col_hdr4:
        st.markdown('<div class="sec-label">Personal Medico de Turno — Lista nativa</div>', unsafe_allow_html=True)
    with col_srch:
        search_q = st.text_input("Buscar por nombre o especialidad", key="staff_search", label_visibility="collapsed",
                                 placeholder="Buscar doctor o especialidad...")
    with col_btn4:
        if st.button("Agregar doctor ", use_container_width=True):
            modal_add_doctor()

    doctors = staff_svc.find_doctor(search_q) if search_q else staff_svc.all_doctors()

    if not doctors:
        st.info("No hay personal registrado." if not search_q else "Sin resultados.")
    else:
        cols = st.columns(3)
        for i, doc in enumerate(doctors):
            with cols[i % 3]:
                st.markdown(
                    f'<div class="doc-card">'
                    f'<div class="doc-name">Dr(a). {doc.name}</div>'
                    f'<div class="doc-spec">{doc.specialty}</div>'
                    f'<div class="doc-id">{doc.doctor_id}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    if staff_svc.all_doctors():
        st.markdown('<div class="sec-label" style="margin-top:1.2rem">Retirar del turno</div>', unsafe_allow_html=True)
        all_docs = staff_svc.all_doctors()
        doc_opts = {f"Dr(a). {d.name}  ({d.doctor_id})  —  {d.specialty}": d.doctor_id for d in all_docs}
        col_dsel, col_dbtn = st.columns([3, 1])
        with col_dsel:
            sel_doc = st.selectbox("Doctor a retirar", list(doc_opts.keys()), label_visibility="collapsed")
        with col_dbtn:
            if st.button("Retirar", use_container_width=True):
                did = doc_opts[sel_doc]
                staff_svc.remove_doctor(did)
                undo_svc.record(Action("REMOVE_DOCTOR", f"Doctor {sel_doc} retirado",
                                       restore_data={"doctor_id": did}))
                _toast("info", f"{sel_doc} retirado del turno.")
                st.rerun()


# ── Tab 5: Action Log / Undo Stack ────────────────────────────────────────────

with tab5:
    col_hdr5, col_undo = st.columns([4, 1])
    with col_hdr5:
        st.markdown(
            f'<div class="sec-label">Registro de Acciones — Pila LIFO &nbsp;·&nbsp; {undo_svc.count()} entradas</div>',
            unsafe_allow_html=True,
        )
    with col_undo:
        if st.button("Deshacer ultima", use_container_width=True):
            action = undo_svc.undo()
            if action:
                if action.action_type == "ADMIT_BED":
                    idx = action.restore_data.get("bed_index")
                    if idx is not None:
                        bed_svc.discharge_from_bed(idx)
                _toast("info", f"Accion revertida: {action.description}")
            else:
                _toast("warning", "No hay acciones para deshacer.")
            st.rerun()

    actions = undo_svc.history()
    if not actions:
        st.info("No hay acciones registradas aun.")
    else:
        for action in actions:
            st.markdown(
                f'<div class="log-row">'
                f'<span>{action.description}</span>'
                f'<span style="display:flex;gap:6px;align-items:center">'
                f'<span class="log-time">{action.timestamp}</span>'
                f'<span class="log-type">{action.action_type}</span>'
                f'</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import subprocess
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            raise RuntimeError
    except (ImportError, RuntimeError):
        sys.exit(subprocess.call([sys.executable, "-m", "streamlit", "run", __file__]))