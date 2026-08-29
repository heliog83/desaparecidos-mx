import pandas as pd
from datetime import datetime
from pathlib import Path
import unicodedata
import urllib.request
import json

def strip_accents(s: str) -> str:
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')

def normalize_state(state: str) -> str:
    """Normalize state name to RNPDNO format."""
    if pd.isna(state):
        return ""
    state = state.strip().upper()
    mapping = {
        "NUEVO LEÓN": "NUEVO LEON",
        "MICHOACÁN": "MICHOACAN DE OCAMPO",
        "ESTADO DE MÉXICO": "MEXICO",
        "VERACRUZ": "VERACRUZ DE IGNACIO DE LA LLAVE",
        "COAHUILA": "COAHUILA DE ZARAGOZA",
    }
    state_no_accents = strip_accents(state)
    return mapping.get(state, mapping.get(state_no_accents, state_no_accents))

def fetch_municipality_coords():
    """Fetch a mapping of Cve_geo (as int) to (lat, lon)."""
    url = "https://raw.githubusercontent.com/eduardoarandah/coordenadas-estados-municipios-localidades-de-mexico-json/master/data.csv"
    coords = {}
    try:
        df_geo = pd.read_csv(url, dtype={'CVE_ENT': str, 'CVE_MUN': str, 'CVE_LOC': str}, low_memory=False)
        # Use only cabeceras municipales (usually CVE_LOC == '0001')
        df_geo = df_geo[df_geo['CVE_LOC'] == '0001']
        for _, row in df_geo.iterrows():
            cve_ent = row['CVE_ENT'].zfill(2)
            cve_mun = row['CVE_MUN'].zfill(3)
            cve_geo = int(cve_ent + cve_mun)
            coords[cve_geo] = (float(row['LAT_DEC']), float(row['LON_DEC']))
    except Exception as e:
        print(f"Warning: Could not fetch municipality coordinates: {e}")
    return coords

def map_cnb_fosas_dataset(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    mapped = pd.DataFrame()
    
    # event_id: generated since there is none in the file
    mapped['event_id'] = [f"CNB-2023-{i:05d}" for i in range(1, len(df) + 1)]
    
    # date processing: if Fecha_hallazgo is not NA, use it. Else use Año + '-01-01'
    def parse_date(row):
        fh = str(row['Fecha_hallazgo'])
        if fh != 'NA' and fh != 'nan':
            return fh
        anio = str(row['Año'])
        if anio != 'NA' and anio != 'nan':
            # use float to int to str to remove .0 if exists
            try:
                a = int(float(anio))
                return f"{a}-01-01"
            except:
                pass
        return ""

    mapped['date'] = df.apply(parse_date, axis=1)
    
    def get_precision(row):
        fh = str(row['Fecha_hallazgo'])
        if fh != 'NA' and fh != 'nan':
            return 'day'
        anio = str(row['Año'])
        if anio != 'NA' and anio != 'nan':
            return 'year'
        return 'approx'

    mapped['date_precision'] = df.apply(get_precision, axis=1)
    mapped['state'] = df['Estado'].apply(normalize_state)
    mapped['municipality'] = df['Municipio']
    
    # Attribution missing in this dataset
    mapped['collective'] = 'unknown'
    mapped['led_by'] = 'state' # CNB is a state registry
    
    # Counts
    mapped['graves_found'] = pd.to_numeric(df['Total_fosas'], errors='coerce').astype('Int64')
    mapped['bodies_found'] = pd.NA
    mapped['remains_bags'] = pd.NA
    mapped['persons_identified'] = pd.NA
    
    # Source metadata
    mapped['source_outlet'] = 'CNB/Quinto Elemento Lab'
    mapped['source_url'] = 'https://quintoelab.org/project/fosas-clandestinas-nuevo-mapa-mexico'
    mapped['consulted'] = '2023-10-06'
    mapped['confidence'] = 'high'
    mapped['notes'] = 'Registro Fosas CNB Quinto Elemento'
    
    # Map Coordinates
    coords = fetch_municipality_coords()
    def get_lat(cve):
        try:
            return coords.get(int(cve), (None, None))[0]
        except:
            return None
    def get_lon(cve):
        try:
            return coords.get(int(cve), (None, None))[1]
        except:
            return None
            
    mapped['lat'] = df['Cve_geo'].apply(get_lat)
    mapped['lon'] = df['Cve_geo'].apply(get_lon)

    # Reorder columns as per schema + lat/lon
    columns = [
        'event_id', 'date', 'date_precision', 'state', 'municipality', 'collective', 
        'led_by', 'graves_found', 'bodies_found', 'remains_bags', 'persons_identified',
        'source_outlet', 'source_url', 'consulted', 'confidence', 'notes', 'lat', 'lon'
    ]
    mapped = mapped[columns]
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    mapped.to_csv(output_path, index=False)
    print(f"Successfully mapped {len(mapped)} events from {input_path} to {output_path}")

if __name__ == "__main__":
    input_file = "data/external/20231006-registro-fosas-cnb-quintoelab.csv"
    output_file = "data/stage2/clandestine_finds_imported.csv"
    map_cnb_fosas_dataset(input_file, output_file)
